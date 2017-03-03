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
db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()
sql = "select id,email_users,app_name,email_template from offer where email_time='%s' and status != 'deleted'"%(time_now)
cursor.execute(sql)
results = cursor.fetchall()
startTime = ((datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=120)).strftime("%Y-%m-%d")
today = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
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
    for i in results:
        mail_to = i[1].split(",")
        offerId = i[0]
        app_name = i[2]
        email_template = i[3].split(",")
        if u"全部维度" in email_template:
            data_sql = "select date,country,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi from datas where date >= '%s' and date <= '%s' and offer_id='%d' order by date ASC " %(startTime,today,offerId)
            cursor.execute(data_sql)
            data_result = cursor.fetchall()
        # 发送邮件
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet(app_name.encode("utf8") + u"数据详情")
        sheet.write(0, 0, "Date")
        sheet.write(0, 1, "Geo")
        sheet.write(0, 2, "Revenue")
        sheet.write(0, 3, "Profit")
        sheet.write(0, 4, "Cost")
        sheet.write(0, 5, "Impressions")
        sheet.write(0, 6, "Clicks")
        sheet.write(0, 7, "Conversions")
        sheet.write(0, 8, "CTR")
        sheet.write(0, 9, "CVR")
        sheet.write(0, 10, "CPC")
        sheet.write(0, 11, "CPI")
        count = 0
        for data in data_result:
            count += 1
            sheet.write(count, 0, data[0])
            sheet.write(count, 1, data[1])
            sheet.write(count, 2, '%0.2f'%float(data[2]))
            sheet.write(count, 3, '%0.2f'%float(data[3]))
            sheet.write(count, 4, '%0.2f'%float(data[4]))
            sheet.write(count, 5, data[5])
            sheet.write(count, 6, data[6])
            sheet.write(count, 7, data[7])
            sheet.write(count, 8, '%0.2f'%float(data[8]))
            sheet.write(count, 9, data[9])
            sheet.write(count, 10, data[10])
            sheet.write(count, 11, data[11])
            continue

        file_name = '=?UTF-8?B?' +base64.b64encode(app_name)+'?='+ "_data.xls"
        file_dir = '/home/ubuntu/code'
        wbk.save(file_name)
        mail_body="data"
        mail_from="ads_reporting@newborntown.com"
        msg = MIMEMultipart()
        body = MIMEText(mail_body)
        msg.attach(body)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file_name, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="' + file_name.encode("utf8") + '"')
        msg.attach(part)
        msg['From'] = mail_from
        msg['To'] = ';'.join(mail_to)
        msg['date'] = time.strftime('%Y-%m-%d')
        msg['Subject'] = '=?UTF-8?B?' + base64.b64encode(app_name) + '?='+"_report Data"
        smtp = smtplib.SMTP()
        smtp.connect('smtp.exmail.qq.com',25)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('ads_reporting@newborntown.com', '5igmKD3F0cLScrS5')
        smtp.sendmail(mail_from, mail_to, msg.as_string())
        smtp.quit()
        print("ok")
except Exception as e:
    print e
