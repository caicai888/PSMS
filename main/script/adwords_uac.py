from __future__ import division
from flask import Blueprint, request
from datetime import datetime, timedelta
from googleads import adwords
import threading
import MySQLdb
import os, sys, string
import time
import csv
import tempfile
import re

adwordsuac = Blueprint('adwordsuac', __name__)
conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='12345',
    db='psms')


class PSMSOffer(object):

    def __init__(self):
        pass

    def get_campaigns(self):
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        query_string = "select offer_id, advertise_series, advertise_groups from advertisers where type = 'adwords'"
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
        data_string = 'insert into adwords values %s' % str(args)
        cursor.execute(data_string)
        conn.commit()
        cursor.close()

    def select_campaign_geo(self, campaign_name):
        selected_msg = re.findall(r'\[(.*)\]', campaign_name)[0]
        selected_geo = re.findall(r'-(.*)', selected_msg)[0].split('_')[0][:2]
        return selected_msg, selected_geo


class AdwordsUac(AdwordsSQL):

    def __init__(self, **kw):
        super(AdwordsUac, self).__init__()
        self.client = adwords.AdWordsClient.LoadFromStorage()
        self.tempf = tempfile.NamedTemporaryFile(delete=True)
        self.is_uac = kw.get('is_UAC')
        self.REPORT = 'CAMPAIGN_LOCATION_TARGET_REPORT' if self.is_uac else 'CAMPAIGN_LOCATION_TARGET_REPORT'
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
                for read in reader:
                    if read['Campaign ID'] != 'Total':
                        self.insert_sql(int(offer_id), customer_id, self.is_uac, read['Campaign ID'], read['Campaign'], read['Impressions'], read['Clicks'],
                                        round(float(read['Cost'])/(10**6), 2), read['Conversions'], read['Day'])
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
        today = datetime.now().strftime("%Y-%m-%d")
        a_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        fields = ['CampaignId', 'CampaignName', 'Impressions', 'Clicks', 'Cost', 'Conversions', 'Date']
        ad = AdwordsUac(fields=fields, start=a_month_ago, end=today, is_UAC=is_UAC)
        ad.query(account_id, offer_id)
        return

def main():
    p = PSMSOffer()
    offer_msg = p.get_campaigns()
    account_dict = { ele['offer_id']: { 'NotUAC': ele['advertise_series'].split(','),
                                        'UAC': ele['advertise_groups'].split(',') }
                    for ele in offer_msg }
    my_process = MyProcess(account_dict)
    my_process.build_thread_task()
    print 'finished'

if __name__ == '__main__':
     main()
     #a = AdwordsSQL()
     #a.create_table()
