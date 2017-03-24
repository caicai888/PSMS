#!/usr/bin/env python
#coding: utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import xlwt
import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import datetime,time
import base64

time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
time_now=time_now.strftime('%H:%M')
time_now = "08:30"
db = MySQLdb.connect("localhost","root","123456","psms",charset='utf8')
cursor = db.cursor()
# sql = "select id,email_users,app_name,email_template from offer where email_time='%s' and status != 'deleted'"%(time_now)
appName_sql = "select app_name from offer where email_time='%s' and status != 'deleted'"%(time_now)
cursor.execute(appName_sql)
appName_results = cursor.fetchall()
app_names = []
for i in appName_results:
    app_names.append(i[0])

app_names = list(set(app_names))
print app_names

# startTime = ((datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=120)).strftime("%Y-%m-%d")
# today = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
startTime = "2017-02-10"
today = "2017-02-13"
date1 = datetime.datetime.strptime(startTime, '%Y-%m-%d')
date2 = datetime.datetime.strptime(today, '%Y-%m-%d')
date_timelta = datetime.timedelta(days=1)
all_date = []
all_date.append(startTime)
while date_timelta < (date2 - date1):
    all_date.append((date1 + date_timelta).strftime("%Y-%m-%d"))
    date_timelta += datetime.timedelta(days=1)
all_date.append(today)

time_ranges = []
for day in all_date[::-1]:
    time_ranges.append("{'since': " + "'" + str(day) + "'" + ", 'until': " + "'" + str(day) + "'" + "}")

accessToken = "EAAHgEYXO0BABABt1QAdnb4kDVpgDv0RcA873EqcNbHFeN8IZANMyXZAU736VKOj1JjSdOPk2WuZC7KwJZBBD76CUbA09tyWETQpOd5OCRSctIo6fuj7cMthZCH6pZA6PZAFmrMgGZChehXreDa3caIZBkBwkyakDAGA4exqgy2sI7JwZDZD"
try:
    for j in app_names:
        sql = "select id,email_users,app_name,email_template from offer where status != 'deleted'"
        cursor.execute(sql)
        results = cursor.fetchall()
        all_data = []
        revenue_count = 0
        profit_count = 0
        cost_count = 0
        impressions_count = 0
        clicks_count = 0
        conversions_count = 0
        ctr_count = 0
        cvr_count = 0
        cpc_count = 0
        cpi_count = 0
        for i in results:
            print i
            offerId = i[0]
            fb_ap_sql = "select id from datas where date='%s' and offer_id='%d'" % (startTime, i[0])
            # mail_to = i[1].split(",")
            # offerId = i[0]
            # app_name = i[2]
            # email_template = i[3].split(",")
            # revenue_count = 0
            # profit_count = 0
            # cost_count = 0
            # impressions_count = 0
            # clicks_count = 0
            # conversions_count = 0
            # ctr_count = 0
            # cvr_count = 0
            # cpc_count = 0
            # cpi_count = 0
            # fb_ap_sql = "select id from datas where date='%s' and offer_id='%d'" %(startTime,offerId)
            # cursor.execute(fb_ap_sql)
            # fb_ap_result = cursor.fetchone()
            # ad_sql = "select id from adwords where date='%s' and offer_id='%d'" %(startTime,offerId)
            # cursor.execute(ad_sql)
            # ad_result = cursor.fetchone()
            # if not fb_ap_result and not ad_result:
            #     pass
            # else:
            #     if u"全部维度" in email_template:
            #         fb_data_sql = "select date,type,country,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi from datas where date>='%s' and date <= '%s' and type='facebook' and offer_id='%d' order by date ASC"%(startTime,today,offerId)
            #         cursor.execute(fb_data_sql)
            #         fb_data_result = cursor.fetchall()
            #         all_data += fb_data_result
            #         ap_data_sql = "select date,type,country,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi from datas where date>='%s' and date <= '%s' and type='apple' and offer_id='%d' order by date ASC"%(startTime,today,offerId)
            #         cursor.execute(ap_data_sql)
            #         ap_data_result = cursor.fetchall()
            #         all_data+=ap_data_result
            #         ad_data_sql = "select date,'adwords',country,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi from datas where date>='%s' and date <= '%s' and offer_id='%d' order by date ASC"%(startTime,today,offerId)
            #         cursor.execute(ad_data_sql)
            #         ad_data_result = cursor.fetchall()
            #         all_data+=ad_data_result
            #
            #     wbk = xlwt.Workbook()
            #     sheet = wbk.add_sheet(app_name.encode("utf8") + u"数据详情")
            #     sheet.write(0, 0, "Date")
            #     sheet.write(0, 1, "Geo")
            #     sheet.write(0, 2, "source")
            #     sheet.write(0, 3, "Revenue")
            #     sheet.write(0, 4, "Profit")
            #     sheet.write(0, 5, "Cost")
            #     sheet.write(0, 6, "Impressions")
            #     sheet.write(0, 7, "Clicks")
            #     sheet.write(0, 8, "Conversions")
            #     sheet.write(0, 9, "CTR")
            #     sheet.write(0, 10, "CVR")
            #     sheet.write(0, 11, "CPC")
            #     sheet.write(0, 12, "CPI")
            #     count = 0
            #
            #     for data in all_data:
            #         count += 1
            #         revenue_count += float('%0.2f'%float(data[3]))
            #         profit_count += float('%0.2f'%float(data[4]))
            #         cost_count += float('%0.2f'%float(data[5]))
            #         impressions_count += int(data[6])
            #         clicks_count += int(data[7])
            #         conversions_count += int(data[8])
            #         sheet.write(count, 0, data[0])
            #         sheet.write(count, 1, data[2])
            #         sheet.write(count, 2, data[1])
            #         sheet.write(count, 3, float('%0.2f'%float(data[3])))
            #         sheet.write(count, 4, float('%0.2f'%float(data[4])))
            #         sheet.write(count, 5, float('%0.2f'%float(data[5])))
            #         sheet.write(count, 6, data[6])
            #         sheet.write(count, 7, data[7])
            #         sheet.write(count, 8, data[8])
            #         sheet.write(count, 9, float('%0.2f'%float(data[9])))
            #         sheet.write(count, 10, float('%0.2f'%float(data[10])))
            #         sheet.write(count, 11, float('%0.2f'%float(data[11])))
            #         sheet.write(count, 12, float('%0.2f'%float(data[12])))
            #         continue
            #
            #     sheet.write(count+1, 0, 'Total')
            #     sheet.write(count+1, 3, revenue_count)
            #     sheet.write(count+1, 4, profit_count)
            #     sheet.write(count+1, 5, cost_count)
            #     sheet.write(count+1, 6, impressions_count)
            #     sheet.write(count+1, 7, clicks_count)
            #     sheet.write(count+1, 8, conversions_count)
            #     if clicks_count !=0:
            #         cvr_count = conversions_count/clicks_count * 100
            #         cpc_count = cost_count/clicks_count
            #     if conversions_count != 0:
            #         cpi_count = cost_count/conversions_count
            #     if impressions_count != 0:
            #         ctr_count = clicks_count/impressions_count * 100
            #     sheet.write(count+1, 9, ctr_count)
            #     sheet.write(count+1, 10, cvr_count)
            #     sheet.write(count+1, 11, cpc_count)
            #     sheet.write(count+1, 12, cpi_count)

                # file_name = '=?UTF-8?B?' +base64.b64encode(app_name)+'?='+ "_data.xls"
                # file_dir = '/home/ubuntu/code'
                # wbk.save(file_name)
                # mail_body="data"
                # mail_from="ads_reporting@newborntown.com"
                # msg = MIMEMultipart()
                # body = MIMEText(mail_body)
                # msg.attach(body)
                # part = MIMEBase('application', 'octet-stream')
                # part.set_payload(open(file_name, 'rb').read())
                # Encoders.encode_base64(part)
                # part.add_header('Content-Disposition', 'attachment; filename="' + file_name.encode("utf8") + '"')
                # msg.attach(part)
                # msg['From'] = mail_from
                # msg['To'] = ';'.join(mail_to)
                # msg['date'] = time.strftime('%Y-%m-%d')
                # msg['Subject'] = '=?UTF-8?B?' + base64.b64encode(app_name) + '?='+"_report Data"
                # smtp = smtplib.SMTP()
                # smtp.connect('smtp.exmail.qq.com',25)
                # smtp.ehlo()
                # smtp.starttls()
                # smtp.ehlo()
                # smtp.login('ads_reporting@newborntown.com', '5igmKD3F0cLScrS5')
                # smtp.sendmail(mail_from, mail_to, msg.as_string())
                # smtp.quit()

except Exception as e:
    print e
