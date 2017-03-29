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

endTime = (datetime.datetime.now()+datetime.timedelta(hours=8)-datetime.timedelta(hours=24)).strftime("%Y-%m-%d")
startTime = (datetime.datetime.now()+datetime.timedelta(hours=8)-datetime.timedelta(hours=768)).strftime("%Y-%m-%d")
db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()

detail_sql = "select date,account_id,sum(cost) cost from dataDetail where date >= '%s' and date <='%s' and type='facebook' group by date,account_id" % (startTime,endTime)
cursor.execute(detail_sql)
detail_result = cursor.fetchall()

all_data = []

for i in detail_result:
    account_sql = "select account_name from campaignRelations where account_id='%s'"%(i[1])
    cursor.execute(account_sql)
    account_result = cursor.fetchone()
    accountName = account_result[0]

    rebate_sql = "select scale from rebate where accountName='%s'" %(accountName)
    cursor.execute(rebate_sql)
    rebate_result = cursor.fetchone()
    if rebate_result:
        rebate = rebate_result[0]
    else:
        rebate = 0

    all_data += [
        {
            "Date": i[0],
            "AccountName": accountName,
            "AccountId": i[1],
            "Cost": float('%0.2f' % (float(i[2]))),
            "Rebate": float('%0.2f' % (float(i[2]) * rebate / 100))
        }
    ]
all_data_list = sorted(all_data, key=lambda k: k['AccountName'])
wbk = xlwt.Workbook()
sheet = wbk.add_sheet("PM_AG_Data")
sheet.write(0, 0, "Date")
sheet.write(0, 1, "AccountId")
sheet.write(0, 2, "AccountName")
sheet.write(0, 3, "Cost")
sheet.write(0, 4, "Rebate")

count = len(all_data_list)
for j in range(count):
    sheet.write(j + 1, 0, all_data_list[j].get("Date"))
    sheet.write(j + 1, 1, all_data_list[j].get("AccountId"))
    sheet.write(j + 1, 2, all_data_list[j].get("AccountName"))
    sheet.write(j + 1, 3, all_data_list[j].get("Cost"))
    sheet.write(j + 1, 4, all_data_list[j].get("Rebate"))
    continue

file_name = "PSMS_AG_Rebate.xls"
file_dir = "/home/ubuntu/code"
wbk.save(file_name)
mail_body = u"一个月内的总代理返点"
mail_from = "ads_reporting@newborntown.com"
mail_to = "liyin@newborntown.com"
mailTo = ";".join(mail_to)
msg = MIMEMultipart()
body = MIMEText(mail_body.encode("utf8"))
msg.attach(body)
part = MIMEBase('application', 'octet-stream')
part.set_payload(open(file_name, 'rb').read())
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="' + file_name.encode("utf8") + '"')
msg.attach(part)
msg['From'] = mail_from
msg['To'] = ';'.join(mail_to)
msg['date'] = time.strftime('%Y-%m-%d')
msg['Subject'] = "PSMS_AG_Rebate"
smtp = smtplib.SMTP()
smtp.connect('smtp.exmail.qq.com', 25)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login('ads_reporting@newborntown.com', '5igmKD3F0cLScrS5')
smtp.sendmail(mail_from, mailTo, msg.as_string())
smtp.quit()