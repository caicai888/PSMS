# coding: utf-8
from __future__ import division
from flask import Blueprint, request
import csv
import sys
import json
import tempfile
from datetime import datetime, timedelta
from main import db
from models import Advertisers, Offer, TimePrice, Country, History
from Geo import geoDict_key_code 
from googleads import adwords


adwordsData = Blueprint('adwordsData', __name__)


class GoogleAdsUtils(object):

    def __init__(self, customer_id, start_date, end_date, offer_id):
        self.adwords_client = adwords.AdWordsClient.LoadFromStorage()
        self.adwords_client.SetClientCustomerId(customer_id)
        self.tempf = tempfile.NamedTemporaryFile(delete=True)
        self.offerId = int(offer_id)
        self.day_price = dict()
        self.fields = ['CountryCriteriaId', 'Impressions', 'Clicks', 'Cost', 'Conversions', 'Date']
        self.REPORT = 'GEO_PERFORMANCE_REPORT'
        self.DATE_RANGE = ','.join((start_date.replace('-', ''), end_date.replace('-', '')))
        self.DateList = self.get_DateList(start_date, end_date)
        self.report_data = dict(impressions=dict(), clicks=dict(), conversions=dict(), profit=dict(),
                                revenue=dict(),cpc=dict(), ctr=dict(), cost=dict(),
                                cpi=dict(), cvr=dict(),)

    def __repr__(self):
        return self.__dict__.__repr__() 

    @staticmethod
    def date_range(start, stop, step):
        while start <= stop:
            yield start
            start += step

    def get_DateList(self, start, end):
        date_list = []
        start = datetime.strptime(start, '%Y-%m-%d')
        stop = datetime.strptime(end, '%Y-%m-%d')
        for d in self.date_range(start, stop, timedelta(days=1)):
            date_list.append(datetime.strftime(d, '%Y-%m-%d'))
        return date_list

    def get_DayPrice(self, geo, day):
        key = '-'.join([day, geo])
        try:
            return self.day_price[key]
        except KeyError:
            country = Country.query.filter_by(shorthand=geo).first()
            offer = Offer.query.filter_by(id=self.offerId).first()
            country_id = country.id
            Price = TimePrice.query.filter(
                TimePrice.country_id==country_id, offer.startTime<=TimePrice.date, TimePrice.date<=day).order_by(TimePrice.date.desc()).first()
            if Price is not None:
                self.day_price[key] = Price.price
                return Price.price
            Price = History.query.filter(
                History.country==geo, History.offer_id==self.offerId).order_by(History.createdTime.desc()).first()
            if Price is not None:
                self.day_price[key] = Price.country_price
                return Price.country_price
            Price = Offer.query.filter(Offer.id==self.offerId).first()
            if Price is not None:
                self.day_price[key] = Price.price
                return Price.price
            return 0

    def generate_report(self, _data):
        if _data['Country/Territory'] == 'Total':
            del _data['Country/Territory']; del _data['Day']
            _data['Conversions'] = float(_data['Conversions'].replace(',', ''))
            _data['Clicks'] = float(_data['Clicks'].replace(',', ''))
            _data['Impressions'] = float(_data['Impressions'].replace(',', ''))
            _data['Cost'] = '%.2f' % (float(_data['Cost'].replace(',', ''))/(10**6))
            _data['Cost'] = float(_data['Cost'])
            _conversion = _data['Conversions']; _clicks = _data['Clicks']
            _cost = _data['Cost']; _impression = _data['Impressions']
            _data['cvr'] = round(_conversion*100.0/_clicks, 2) if _clicks else 0
            _data['ctr'] = round(_conversion*100.0/_impression, 2) if _impression else 0
            _data['cpi'] = round(_cost*100.0/_conversion, 2) if _conversion else 0
            _data['cpc'] = round(_cost*100.0/_clicks, 2) if _clicks else 0
            self.report_data['Total'] = _data
        else:
            day = _data['Day']
            _geo = geoDict_key_code.get(_data['Country/Territory'], '')
            _imp = float(_data['Impressions'].replace(',', ''))
            _cli = float(_data['Clicks'].replace(',', ''))
            _conv = float(_data['Conversions'].replace(',', ''))
            _cost = '%.2f' % (float(_data['Cost'].replace(',', ''))/(10**6))
            _cost = float(_cost)
            geo_key = ''.join(['geo', day])
            try:
                self.report_data['impressions'][geo_key][_geo] += _imp
                self.report_data['clicks'][geo_key][_geo] += _cli
                self.report_data['conversions'][geo_key][_geo] += _conv
                self.report_data['cost'][geo_key][_geo] += _cost

            except KeyError:
                self.report_data['impressions'][geo_key] = {_geo: _imp}
                self.report_data['clicks'][geo_key] = {_geo: _cli}
                self.report_data['conversions'][geo_key] = {_geo: _conv}
                self.report_data['cost'][geo_key] = {_geo: _cost}

            try:
                self.report_data['impressions'][day] += _imp
                self.report_data['clicks'][day] += _cli
                self.report_data['conversions'][day] += _conv
                self.report_data['cost'][day] += _cost
            except KeyError:
                self.report_data['impressions'][day] = _imp                
                self.report_data['clicks'][day] = _cli 
                self.report_data['conversions'][day] = _conv 
                self.report_data['cost'][day] = _cost 
        
    def calculate_report(self):
        _conv_dic = {k.strip('geo'): v for k, v in self.report_data['conversions'].iteritems() if 'geo' in k}
        _cli_dic = {k.strip('geo'): v for k, v in self.report_data['clicks'].iteritems() if 'geo' in k}
        _cost_dic = {k.strip('geo'): v for k, v in self.report_data['cost'].iteritems() if 'geo' in k}
        _imp_dic = {k.strip('geo'): v for k, v in self.report_data['impressions'].iteritems() if 'geo' in k}
        for date in self.DateList:
            _imp = _imp_dic[date]
            for country, _imp in _imp.iteritems():
                _conv = _conv_dic[date].get(country, 0)
                _cli = _cli_dic[date].get(country, 0)
                _cost = _cost_dic[date].get(country, 0)
                _price = self.get_DayPrice(country, date)
                _revenue = _price * _conv
                _profit = _revenue - _cost
                day_key = ''.join(['geo', date])
                try:
                    self.report_data['cvr'][day_key] = { country: round(_conv*100.0/_cli, 2) }
                except ZeroDivisionError:
                    self.report_data['cvr'][day_key] = { country: 0 }
                try:
                    self.report_data['ctr'][day_key] = { country: round(_conv*100.0/_imp, 2) }
                except ZeroDivisionError:
                    self.report_data['ctr'][day_key] = { country: 0 }
                try:
                    self.report_data['cpi'][day_key] = { country: round(_cost*100.0/_conv, 2) }
                except ZeroDivisionError:
                    self.report_data['cpi'][day_key] = { country: 0 }
                try:
                    self.report_data['cpc'][day_key] = { country: round(_cost*100.0/_cli, 2) }
                except ZeroDivisionError:
                    self.report_data['cpc'][day_key] = { country: 0 }
                self.report_data['revenue'][day_key] = { country: _revenue }
                self.report_data['profit'][day_key] = { country: _profit }
            d_conv = self.report_data['conversions'][date]; d_cli = self.report_data['clicks'][date]
            d_cost = self.report_data['cost'][date]; d_imp = self.report_data['impressions'][date]
            try:
                self.report_data['cvr'][date] = round(d_conv*100.0/d_cli, 2)
            except ZeroDivisionError:
                self.report_data['cvr'][date] = 0
            try:
                self.report_data['ctr'][date] = round(d_conv*100.0/d_imp, 2)
            except ZeroDivisionError:
                self.report_data['ctr'][date] = 0
            try:
                self.report_data['cpi'][date] = round(d_cost*100.0/d_conv, 2)
            except ZeroDivisionError:
                self.report_data['cpi'][date] = 0
            try:
                self.report_data['cpc'][date] = round(d_cost*100.0/d_cli, 2)
            except ZeroDivisionError:
                self.report_data['cpc'][date] = 0
            self.report_data['revenue'][date] = sum(self.report_data['revenue'][day_key].values()) 
            self.report_data['profit'][date] = sum(self.report_data['profit'][day_key].values()) 
        self.report_data['Total']['Revenue'] = sum([v for k, v in self.report_data['revenue'].iteritems() if 'geo' not in k])
        self.report_data['Total']['Profit'] = sum([v for k, v in self.report_data['profit'].iteritems() if 'geo' not in k])

    @staticmethod
    def format_list(dic, dimension):
        temp_list = []
        for k, v in dic.iteritems():
            if 'geo' in k:
                day = k.strip('geo')
                for _k, _v in v.iteritems():
                    temp_list.append({
                        "country": _k,
                        "date_stop": day,
                        "date_start": day,
                        dimension: _v,})
        return temp_list

    def GetDashboard(self):
        self.query()
        dashboard_data = {}
        for key, value in self.report_data.iteritems():
            for k, v in value.iteritems():
                if 'geo' not in k:
                    if k.lower() == 'cost':
                        dashboard_data['spend'] = v
                    else:
                        dashboard_data[key.lower()] = v
        return dashboard_data
       
    def GetDataFromGads(self, key):
        self.statistics_key = key
        self.query()
        _data = self.report_data['Total']

        total_data = {
            "revenue": _data['Revenue'],
            "count_cpc": _data['cpc'],
            "count_impressions": _data['Impressions'],
            "count_cvr": _data['cvr'],
            "count_clicks": _data['Clicks'],
            "profit": '%.2f' % _data['Profit'],
            "count_conversions": _data['Conversions'],
            "count_cpi": _data['cpi'],
            "count_ctr": _data['ctr'],
            "count_cost": _data['Cost'],}

        chart_data = {
            "date": self.DateList,
            "conversions": [self.report_data['conversions'].get(day, 0) for day in self.DateList],
            "revenue": [self.report_data['revenue'].get(day, 0) for day in self.DateList],
            "impressions": [self.report_data['impressions'].get(day, 0) for day in self.DateList],
            "costs": [self.report_data['cost'].get(day, 0) for day in self.DateList],
            "clicks": [self.report_data['clicks'].get(day, 0) for day in self.DateList],
            "profit": [self.report_data['profit'].get(day, 0) for day in self.DateList],
            "cpi": [self.report_data['cpi'].get(day, 0) for day in self.DateList],
            "ctr": [self.report_data['ctr'].get(day, 0) for day in self.DateList],
            "cpc": [self.report_data['cpc'].get(day, 0) for day in self.DateList],
            "cvr": [self.report_data['cvr'].get(day, 0) for day in self.DateList],}

        if key:
            _cost_list = self.format_list(self.report_data['cost'], "spend")
            for _c in _cost_list:
                _c['spend'] = '%.2f' % _c['spend']
                     
            table_data = {
                "impressions_list":
                    self.format_list(self.report_data['impressions'], "impressions"),
                "conversions_list":
                    self.format_list(self.report_data['conversions'], "conversions"),
                "cost_list": _cost_list,
                "clicks_list":
                    self.format_list(self.report_data['clicks'], "clicks"),
                "profit_list":
                    self.format_list(self.report_data['profit'], "profit"),
                "revenue_list":
                    self.format_list(self.report_data['revenue'], "revenue"),
                "cpc_list":
                    self.format_list(self.report_data['cpc'], "cpc"),
                "ctr_list":
                    self.format_list(self.report_data['ctr'], "ctr"),
                "cpi_list":
                    self.format_list(self.report_data['cpi'], "cpi"),
                "cvr_list":
                    self.format_list(self.report_data['cvr'], "cvr"),}
            for key, _list in table_data.items():
                table_data[key] = sorted(_list, key=lambda ele: ele['date_start'], reverse=True)

                table_data.update(
                    {"head": ["Date","Geo", "Revenue", "Profit", "Cost", "Impressions", "Clicks", "Conversions", "CTR", "CVR", "CPC", "CPI"],})

        else:
            for key, value in self.report_data.iteritems():
                self.report_data[key] = { k: v for k, v in value.iteritems() if 'geo' not in k } if key is not 'Total' else value

            _cost_list = [{'date_start': k, 'spend': v} for k, v in self.report_data['cost'].iteritems()]
            for _c in _cost_list:
                _c['spend'] = '%.2f' % _c['spend']

            table_data = {
                "clicks_list":
                    [{'date_start': k, 'clicks': v} for k, v in self.report_data['clicks'].iteritems()],
                "impressions_list":
                    [{'date_start': k, 'impressions': v} for k, v in self.report_data['impressions'].iteritems()],
                "cost_list": _cost_list,
                "conversions_list":
                    [{'date_start': k, 'conversions': v} for k, v in self.report_data['conversions'].iteritems()],
                "profit_list":
                    [{'date_start': k, 'profit': v} for k, v in self.report_data['profit'].iteritems()],
                "revenue_list":
                    [{'date_start': k, 'revenue': v} for k, v in self.report_data['revenue'].iteritems()],
                "cvr_list":
                    [{'date_start': k, 'cvr': v} for k, v in self.report_data['cvr'].iteritems()],
                "cpi_list":
                    [{'date_start': k, 'cpi': v} for k, v in self.report_data['cpi'].iteritems()],
                "ctr_list":
                    [{'date_start': k, 'ctr': v} for k, v in self.report_data['ctr'].iteritems()],
                "cpc_list":
                    [{'date_start': k, 'cpc': v} for k, v in self.report_data['cpc'].iteritems()],}
            for key, _list in table_data.iteritems():
                table_data[key] = sorted(_list, key=lambda ele: ele['date_start'], reverse=True)
            table_data.update(
                {"head": ["Date", "Revenue", "Profit", "Cost", "Impressions", "Clicks", "Conversions", "CTR", "CVR", "CPC", "CPI"],})

        return total_data, table_data, chart_data

    def query(self):
        # fields = ['CampaignId', 'CampaignName', 'Ctr', 'ConversionRate', 'CostPerConversion', 'AverageCpc',]
        # ColumnList = ','.join(fields + self.fields)
        ColumnList = ','.join(self.fields)
        report_downloader = self.adwords_client.GetReportDownloader(version='v201609')
        report_query = ('SELECT %s FROM %s DURING %s' % (ColumnList, self.REPORT, self.DATE_RANGE))
 
        try:
            report_downloader.DownloadReportWithAwql(
                report_query, 'CSV', self.tempf, skip_report_header=True,
                skip_column_header=False, skip_report_summary=False)
            self.tempf.seek(0)
            with open(self.tempf.name, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                map(self.generate_report, reader)

            self.calculate_report()

        finally:
            self.tempf.close()


    def export_csv(self, path):
        report_downloader = self.adwords_client.GetReportDownloader(version='v201609')
    
        report_query = ('SELECT CampaignId, CampaignName, CountryCriteriaId, Impressions, Clicks, Cost '
                        'FROM GEO_PERFORMANCE_REPORT '
                        # 'WHERE Status IN [ENABLED] '
                        'DURING LAST_7_DAYS')
    
        with open(path, 'w') as output_file:
          report_downloader.DownloadReportWithAwql(
              report_query, 'CSV', output_file, skip_report_header=False,
              skip_column_header=False, skip_report_summary=False)
    
        print 'Report was downloaded to \'%s\'.' % path


class AdwordsRoutes(GoogleAdsUtils): 

    @adwordsData.route('/api/googleads', methods=['POST', 'GET'])
    def get_report():
        if request.method == 'POST':
            _args = request.get_json(force=True)
            dimen = 'geo' in _args.get("dimension")  # date: 0, geo: 1
            offer_id = _args.get('offer_id')
            start = _args.get('start_date')
            end = _args.get('end_date')

            ads = GoogleAdsUtils('296-153-6464', start, end, offer_id)
            total, table_data, chart_data = ads.GetDataFromGads(dimen)
            if dimen:
                response = {'code': 200, 'data_geo': total, 'data_geo_table': table_data, 'message': "success",
                            "data_date_table": {}, 'data_range': chart_data}
            else:
                response = {'code': 200, 'data_geo': total, 'data_date_table': table_data, 'message': "success",
                            "data_geo_table": {}, 'data_range': chart_data}
            return json.dumps(response)

    @adwordsData.route('/api/adwords/dashboard')
    def get_dashboard():
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        result = {
            "impressions": 0, "spend": 0, "clicks": 0, "conversions": 0, "cpc": 0, "ctr": 0, "cpi": 0,
            "cvr": 0, "revenue": 0, "profit": 0,}
        offer_msg = Advertisers.query.filter(Advertisers.type=='facebook').all() 
        for offer in offer_msg:
            offer.advertise_series = '296-153-6464'
            ads = GoogleAdsUtils(offer.advertise_series, yesterday, yesterday, offer.offer_id)
            dashboard_data = ads.GetDashboard()
            for k, v in result.iteritems():
                result[k] += dashboard_data[k]

        for key, value in result.iteritems():
            result[key] = '%.2f' % value

        response = {
            "code": 200,
            "message": "success",
            "result": result,}
        return json.dumps(response)

if __name__ == '__main__':
    ads = GoogleAdsUtils('296-153-6464', '2016-12-30', '2017-01-03')
    # PATH = '/tmp/report_download.csv'
    # ads.export_csv(PATH)
    # ads.query()
