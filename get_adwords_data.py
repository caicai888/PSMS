#!/usr/bin/env python
#coding: utf-8
from googleads import adwords
import csv
import tempfile

client = adwords.AdWordsClient.LoadFromStorage()
client.SetClientCustomerId("932-670-7990")
tempf = tempfile.NamedTemporaryFile(delete=True)
REPORT = 'GEO_PERFORMANCE_REPORT'
start = "2017-03-06"
end = "2017-03-06"
DATE_RANGE = ','.join((start.replace('-', ''), end.replace('-', '')))
fields = ['CampaignId', 'CampaignName','CountryCriteriaId', 'Impressions', 'Clicks', 'Cost', 'Conversions', 'Date']
column_list = ','.join(fields)

report_downloader = client.GetReportDownloader(version='v201609')
report_query_string = ('SELECT %s FROM %s DURING %s' % (column_list, REPORT, DATE_RANGE))
report_downloader.DownloadReportWithAwql(report_query_string, 'CSV', tempf, skip_report_header=True,skip_column_header=False, skip_report_summary=False)
tempf.seek(0)
with open(tempf.name, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for read in reader:
        if read['Campaign ID'] != 'Total':
            if ',' in read['Conversions']:
                conversions = read['Conversions'].replace(',', '')
            else:
                conversions = read['Conversions']
            countryNumber = read["Country/Territory"]
            cost = round(float(read['Cost']) / (10 ** 6), 2)

            print conversions,cost, countryNumber
            print "+++++"*10