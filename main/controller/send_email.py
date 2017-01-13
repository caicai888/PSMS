#!/usr/bin/env python
#coding: utf-8
from __future__ import division
import _env  # noqa
import csv
import smtplib
import os
import sys
import tempfile
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
from Geo import geoDict_key_code
from googleads import adwords


class SimpleGoogleAds(object):

    adwords_client = adwords.AdWordsClient.LoadFromStorage()
    temp_path = '/tmp/report_download.csv'
    columns = ['Date', 'Country', 'Impressions', 'Clicks', 'Cost', 'Conversions', 'CTR', 'CPI', 'CVR', 'CPC', 'CustomerId']
    with open(temp_path, 'wb') as report_file:
        header_line = ','.join(columns) + '\n'
        report_file.writelines(header_line)
        report_file.close()

    def setCientCustomer(self, **kwds):
        return self.adwords_client.SetClientCustomerId(kwds.get('customer_id'))

    def get_report_from_google(self, customer_id):
        self.setCientCustomer(customer_id=customer_id)
        fields = ['Date', 'CountryCriteriaId', 'Impressions', 'Clicks', 'Cost', 'Conversions',  'Ctr', 'CostPerConversion', 'ConversionRate', 'AverageCpc']
        COLUMN = ['Day', 'Country/Territory', 'Impressions', 'Clicks', 'Cost', 'Conversions', 'CTR', 'Cost / conv.', 'Conv. rate', 'Avg. CPC']
        REPORT = 'GEO_PERFORMANCE_REPORT'
        DATE_RANGE = 'TODAY'
        report_downloader = self.adwords_client.GetReportDownloader(version='v201609')
        ColumnList = ','.join(fields)
        report_query = ('SELECT %s FROM %s DURING %s' % (ColumnList, REPORT, DATE_RANGE))

        try:
            tempf = tempfile.NamedTemporaryFile(delete=True)
            report_downloader.DownloadReportWithAwql(
                report_query, 'CSV', tempf, skip_report_header=True,
                skip_column_header=False, skip_report_summary=True)
            tempf.seek(0)
            
            fields_map_column = { COLUMN[_index]: self.columns[_index] for _index, v in enumerate(COLUMN) }
            def write_2_ReportDownFile(row):
                country_code = row.get('Country/Territory')
                country = geoDict_key_code.get(country_code, '')
                row_dict = { fields_map_column[key]: value for key, value in row.iteritems() if key not in ['Country/Territory', 'Cost'] }
                row_dict['Country'] = country
                row_dict['Cost'] = '%.2f' % (float(row.get('Cost')) / (10**6)) if row.get('Cost') else '0'
                row_dict['CustomerId'] = customer_id
                content_list = map(lambda e: row_dict[e], self.columns)
                return content_list 

            with open(tempf.name, 'rb') as f:
                reader = csv.DictReader(f)
                content_lines = map(lambda ele: ','.join(write_2_ReportDownFile(ele))+'\n', reader)
                with open(self.temp_path, 'ab') as report_file:
                    report_file.writelines(content_lines)

        except Exception as e:
            print e
        finally:
            tempf.close()

class VirtualEmail(SimpleGoogleAds):
    
    def __init__(self, **kwds):
        day = kwds.get('day', datetime.now().strftime('%Y-%m-%d')) 
        self.title = kwds.get('title', '_'.join(['Report', day]))
        self.sender = kwds.get('sender', '645201357@qq.com')
        self.receiver = kwds.get('receiver', 'susie@newborn-town.com')
        self.host = "smtp.qq.com"
        self.port = 25
        self.user = '645201357@qq.com'
        self.password = 'zzwpshfvllpvbeee'
        super(VirtualEmail, self).__init__()

    def __repr__(self):
        return self.__dict__.__repr__()

    def _send(self):
        log_path = 'sendemail_error_log'
        send_text = "Google Adwords Report Data"        
        try:
            msg = MIMEMultipart()
            msg.attach(MIMEText(send_text))
            msg.Subject = Header(self.title, 'utf-8')
            att = MIMEText(open(self.temp_path, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename=' + self.title + '.csv'
             
            msg.attach(att)
            smtp = smtplib.SMTP()
            smtp.connect(self.host, self.port)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.user, self.password)
            smtp.sendmail(self.sender, self.receiver, msg.as_string())
            smtp.quit()

        except Exception, e:
            with open(log_path, 'ab') as f:
                log = "%s-->%s\n" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(e))
                f.write(log)
        finally:
            _commend = 'rm %s' % self.temp_path
            return os.system(_commend)
