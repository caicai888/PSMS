#!/usr/bin/env python
#coding: utf-8
from __future__ import division
from flask import Blueprint
from datetime import datetime, timedelta
from googleads import adwords
import threading
import MySQLdb
import csv
import tempfile
import re

adwordsuac = Blueprint('adwordsuac', __name__)
conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='chizicheng521',
    db='psms')


class PSMSOffer(object):

    def __init__(self):
        pass

    def get_campaigns(self):
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        # query_string = "select offer_id, adwords_notuac, adwords_uac from advertisers where type = 'adwords' and offer_id in (select id from offer where status != 'deleted')"
        query_string = "select offer_id, adwords_notuac, adwords_uac from advertisers where type = 'adwords' and offer_id=32"
        try:
            cursor.execute(query_string)
        finally:
            cursor.close()
        return cursor 


class AdwordsSQL(object):

    def keyword_query_sql(self, kw):
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        query_string = "select *from adwords where campaignName like '%{0}%'".format(kw)
        try:
            cursor.execute(query_string)
        finally:
            cursor.close()
        return cursor 

    def create_table(self):
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("create table adwords (offer_id int, account_id char(20), is_UAC bool, campaignId int, campaignName char(50),\
        impressions char(20), clicks int, cost float, conversion char(20), date char(12))")
        cursor.close()

    def insert_sql(self, *args):
        cursor = conn.cursor()
        data_string = 'insert into adwords (offer_id,account_id,is_UAC,campaignId,campaignName,impressions,clicks,revenue,cost,profit,conversions,cpc,cvr,cpi,ctr,date,country) values %s' % str(args)
        cursor.execute(data_string)
        conn.commit()
        cursor.close()

    def select_campaign_geo(self, campaign_name):
        selected_msg = re.findall(r'\[(.*)\]', campaign_name)[0]
        selected_geo = re.findall(r'-(.*)', selected_msg)[0].split('_')[0][:2]
        # return selected_msg, selected_geo
        return selected_geo


class AdwordsUac(AdwordsSQL):

    def __init__(self, **kw):
        super(AdwordsUac, self).__init__()
        self.client = adwords.AdWordsClient.LoadFromStorage()
        self.tempf = tempfile.NamedTemporaryFile(delete=True)
        self.is_uac = kw.get('is_UAC')
        self.REPORT = 'CAMPAIGN_LOCATION_TARGET_REPORT' if self.is_uac else 'GEO_PERFORMANCE_REPORT'
        self.fields = kw.get('fields', [])
        start = kw.get('start', '2017-01-01')
        end = kw.get('end', '2017-01-01')
        self.DATE_RANGE = ','.join((start.replace('-', ''), end.replace('-', '')))
        self.date_list = self.get_date_list(start, end)

    def __repr__(self):
        return self.__dict__.__repr__()

    def set_customerId(self, customer_id):
        """
            param: customer_id = account_id.
        """
        self.client.SetClientCustomerId(customer_id)

    def get_date_list(self, start, end):
        date_list = []
        s = datetime.strptime(start, '%Y-%m-%d')
        e = datetime.strptime(end, '%Y-%m-%d')
        for date in self.date_range(s, e, timedelta(days=1)):
            date_list.append(datetime.strftime(date, "%Y-%m-%d"))
        return date_list

    @staticmethod
    def date_range(start, stop, step):
        while start <= stop:
            yield start
            start += step

    def query(self, customer_id, offer_id):
        self.set_customerId(customer_id)
        column_list = ','.join(self.fields)
        report_downloader = self.client.GetReportDownloader(version='v201609')
        report_query_string = ('SELECT %s FROM %s DURING %s' % (column_list, self.REPORT, self.DATE_RANGE))

        try:
            report_downloader.DownloadReportWithAwql(
                report_query_string, 'CSV', self.tempf, skip_report_header=True,
                skip_column_header=False, skip_report_summary=False)
            self.tempf.seek(0)
            with open(self.tempf.name, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                for read in reader:
                    if read['Campaign ID'] != 'Total':
                        if self.is_uac == False:
                            countryNumber = read["Country/Territory"]
                            country_sql = "select countryName from adwordsGeo where countryNumber='%s'"%(countryNumber)
                            cursor.execute(country_sql)
                            country_result = cursor.fetchone()
                            countryName = country_result["countryName"]
                            country_sql_notadwords = "select id from country where shorthand='%s'"%(countryName)
                            cursor.execute(country_sql_notadwords)
                            country_notadwords_result = cursor.fetchone()
                            countryId = country_notadwords_result["id"]
                        else:
                            countryName = self.select_campaign_geo(read["Campaign"])
                            country_sql_notadwords = "select id from country where shorthand='%s'" % (countryName)
                            cursor.execute(country_sql_notadwords)
                            country_notadwords_result = cursor.fetchone()
                            if country_notadwords_result is None:
                                pass
                            else:
                                countryId = country_notadwords_result["id"]
                        offer_sql = "select startTime,endTime,contract_type,contract_scale,price from platformOffer where offer_id='%d' and platform='adwords'"%(int(offer_id))
                        cursor.execute(offer_sql)
                        offer_result = cursor.fetchone()
                        offer_price = offer_result["price"]
                        contract_type = offer_result["contract_type"]
                        contract_scale = offer_result['contract_scale']
                        if ',' in read['Conversions']:
                            conversions = read['Conversions'].replace(',','')
                        else:
                            conversions = read['Conversions']
                        if contract_type == "1":
                            cooperation_sql = "select contract_scale from cooperationPer where offer_id='%d' and platform='adwords' and date<='%s' and date>='%s' order by date" % (int(offer_id), read['Day'], offer_result["startTime"])
                            cursor.execute(cooperation_sql)
                            cooperation_result = cursor.fetchone()
                            if cooperation_result:
                                contract_scale = cooperation_result["contract_scale"]
                            else:
                                history_scale_sql = "select contract_scale from history where platform='adwords' and offer_id='%d' order by createdTime desc" % (int(offer_id))
                                cursor.execute(history_scale_sql)
                                history_scale_result = cursor.fetchone()
                                if history_scale_result:
                                    contract_scale = history_scale_result["contract_scale"]
                            revenue = '%0.2f' % (round(float(read['Cost']) / (10 ** 6), 2) * (1 + float(contract_scale) / 100))
                        else:
                            timePrice_sql = "select price from timePrice where country_id='%d' and platform='adwords' and offer_id='%d' and date<='%s' and date>='%s' order by date" % (countryId, int(offer_id), read['Day'], offer_result["startTime"])
                            cursor.execute(timePrice_sql)
                            timePrice_result = cursor.fetchone()
                            if timePrice_result:
                                price = timePrice_result["price"]
                            else:
                                history_sql = "select country_price from history where country='%s' and platform='adwords' and offer_id='%d'order by createdTime desc" % (countryName, int(offer_id))
                                cursor.execute(history_sql)
                                history_result = cursor.fetchone()
                                if not history_result:
                                    price = offer_price
                                else:
                                    price = history_result["country_price"]
                            revenue = '%0.2f' % (float(price) * float(conversions))

                        if self.is_uac == False:
                            is_uac = 0
                        else:
                            is_uac = 1
                        cpc = '%0.2f'%(round(float(read['Cost'])/(10**6), 2)/float(read['Clicks'])) if float(read['Clicks']) != 0 else 0
                        cvr = '%0.2f'%(float(conversions)/float(read['Clicks'])*100) if float(read['Clicks']) != 0 else 0
                        cpi = '%0.2f'%(round(float(read['Cost'])/(10**6), 2)/float(conversions)) if float(conversions) != 0 else 0
                        ctr = '%0.2f'%(float(read['Clicks'])/float(read['Impressions'])*100) if float(read['Impressions']) != 0 else 0
                        profit = '%0.2f'%(float(revenue)-(round(float(read['Cost'])/(10**6), 2)))
                        sql_ad = "select id from adwords where offer_id='%d' and account_id='%s' and date='%s' and campaignId='%d'" % (int(offer_id), str(customer_id), str(read['Day']),int(read['Campaign ID']))
                        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                        cursor.execute(sql_ad)
                        result_ad = cursor.fetchone()
                        if not result_ad:
                            self.insert_sql(int(offer_id), str(customer_id), int(is_uac), int(read['Campaign ID']), str(read['Campaign']),str(read['Impressions']), int(read['Clicks']), float(revenue), round(float(read['Cost']) / (10 ** 6), 2),float(profit), str(conversions), cpc, cvr, cpi, ctr, str(read['Day']),countryName)
                        else:
                            update_sql = "update adwords set account_id='%s',is_UAC='%d',campaignId='%d',campaignName='%s',impressions='%s',clicks='%d',revenue='%f',cost='%f',profit='%f',conversions='%s',cpc='%s',cvr='%s',cpi='%s',ctr='%s',date='%s',country='%s' where id='%d'" % (str(customer_id), int(is_uac), int(read['Campaign ID']), str(read['Campaign']), str(read['Impressions']),int(read['Clicks']), float(revenue), round(float(read['Cost']) / (10 ** 6), 2), float(profit), str(conversions), cpc, cvr,cpi, ctr, str(read['Day']),str(countryName),result_ad["id"])
                            cursor.execute(update_sql)
                            conn.commit()

        finally:
            self.tempf.close()


class MyProcess(object):

    def __init__(self, task_list):
        self.task = task_list
        self.lock = threading.Lock()
        self.task_num = len(self.task)

    def build_thread_task(self):
        for offer_id, account_msg in self.task.iteritems():
            for account_type, account_ids in account_msg.items():
                if account_type == 'UAC':
                    for account_id in account_ids:
                        if account_id:
                            self.get_uac_account_msg(self, account_id, offer_id, True)
                else:
                    assert account_type == 'NotUAC'
                    for account_id in account_ids:
                        if account_id:
                            self.get_uac_account_msg(self, account_id, offer_id)
        return

    @staticmethod
    def get_uac_account_msg(self, account_id, offer_id, is_UAC=False):
        today = (datetime.now()+timedelta(hours=8)).strftime("%Y-%m-%d")
        a_month_ago = ((datetime.now()+timedelta(hours=8)) - timedelta(days=30)).strftime("%Y-%m-%d")
        if is_UAC == False:
            fields = ['CampaignId', 'CampaignName', 'CountryCriteriaId', 'Impressions', 'Clicks', 'Cost', 'Conversions', 'Date']
        else:
            fields = ['CampaignId', 'CampaignName', 'Impressions', 'Clicks', 'Cost', 'Conversions', 'Date']
        ad = AdwordsUac(fields=fields, start=a_month_ago, end=today, is_UAC=is_UAC)
        ad.query(account_id, offer_id)
        return

def main():
    p = PSMSOffer()
    offer_msg = p.get_campaigns()
    account_dict = { ele['offer_id']: { 'NotUAC': ele['adwords_notuac'].split(','),
                                        'UAC': ele['adwords_uac'].split(',') }
                    for ele in offer_msg }
    my_process = MyProcess(account_dict)
    my_process.build_thread_task()
    print 'finished'

if __name__ == '__main__':
     main()