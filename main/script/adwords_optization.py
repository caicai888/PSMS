#!/usr/bin/env python
#coding: utf-8
import MySQLdb
from googleads import adwords
import csv
import tempfile
import datetime

time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
time_now = datetime.datetime.strftime(time_now, '%Y-%m-%d')
start_date = (datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=72)
# start_date = datetime.datetime.now()-datetime.timedelta(hours=240)
start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()

adwords_sql = "select account_id,id from adwords where date >= '%s' and date <= '%s'" % (start_date,time_now)
# adwords_sql = "select account_id,id from adwords where date = '2017-02-15'"
cursor.execute(adwords_sql)
apple_results = cursor.fetchall()

client = adwords.AdWordsClient.LoadFromStorage()
for i in apple_results:
    print i[0]
    client.SetClientCustomerId(i[0])
    tempf = tempfile.NamedTemporaryFile(delete=True)
    REPORT = 'ACCOUNT_PERFORMANCE_REPORT'
    fields = ['AccountDescriptiveName']
    column_list = ','.join(fields)
    report_downloader = client.GetReportDownloader(version='v201609')
    report_query_string = ('SELECT %s FROM %s' % (column_list, REPORT))
    report_downloader.DownloadReportWithAwql(report_query_string, 'CSV', tempf, skip_report_header=True, skip_column_header=False,
                                             skip_report_summary=False)
    tempf.seek(0)
    with open(tempf.name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for read in reader:
            if read['Account'] != "Total":
                print read['Account']
                print "+++"*10
                account_name = read['Account'].split('_')
                for j in account_name:
                    if "66" in j:
                        update_opt = "update adwords set optName='%s' where id='%d'" % (j, i[1])
                        cursor.execute(update_opt)
                        db.commit()

print "ok"