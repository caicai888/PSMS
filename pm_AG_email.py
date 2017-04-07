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

detail_sql = "select accountId,accountName,sum(cost) cost,sum(rebate) rebate from accountRebate where date >= '%s' and date <= '%s' group by accountId,accountName" %(startTime,endTime)
cursor.execute(detail_sql)
detail_result = cursor.fetchall()

all_data = []

MadCost = 0
PinzhongCost = 0
FeishuCost = 0
LanbiaoCost = 0
MuguaCost = 0
ChangleCost = 0

MadRebate = 0
PinzhongRebate = 0
FeishuRebate = 0
LanbiaoRebate = 0
MuguaRebate = 0
ChangleRebate = 0

CostCount = 0
RebateCount = 0

for i in detail_result:
    rebate_sql = "select companyName from rebate where accountName='%s'" %(i[1])
    cursor.execute(rebate_sql)
    rebate_result = cursor.fetchone()
    CostCount += float(i[2])
    RebateCount += float(i[3])
    if rebate_result:
        company = rebate_result[0]
    else:
        company = u"广告主"
    if i[1] == "Madhouse":
        MadCost += float(i[2])
        MadRebate += float(i[3])
    if i[1] == u"品众":
        PinzhongCost += float(i[2])
        PinzhongRebate += float(i[3])
    if i[1] == u"飞书":
        FeishuCost += float(i[2])
        FeishuRebate += float(i[3])
    if i[1] == u"蓝标":
        LanbiaoCost += float(i[2])
        LanbiaoRebate += float(i[3])
    if i[1] == u"木瓜":
        MuguaCost += float(i[2])
        MuguaRebate += float(i[3])
    if i[1] == u"常乐":
        ChangleCost += float(i[2])
        ChangleRebate += float(i[3])
    all_data += [
        {
            "AccountName": i[1],
            "AccountId": i[0],
            "Cost": float('%0.2f' % (float(i[2]))),
            "Rebate": float('%0.2f' % (float(i[3]))),
            "CompanyName": company
        }
    ]
all_data_list = sorted(all_data, key=lambda k: k['AccountName'])
wbk = xlwt.Workbook()
sheet = wbk.add_sheet("PM_AG_Data")
sheet.write(0, 0, "AccountId")
sheet.write(0, 1, "AccountName")
sheet.write(0, 2, "CompanyName")
sheet.write(0, 3, "Cost")
sheet.write(0, 4, "Rebate")

count = len(all_data_list)
for j in range(count):
    sheet.write(j + 1, 0, all_data_list[j].get("AccountId"))
    sheet.write(j + 1, 1, all_data_list[j].get("AccountName"))
    sheet.write(j + 1, 2, all_data_list[j].get("CompanyName"))
    sheet.write(j + 1, 3, all_data_list[j].get("Cost"))
    sheet.write(j + 1, 4, all_data_list[j].get("Rebate"))
    continue

sheet.write(count + 1, 0, "Total")
sheet.write(count + 1, 3, float('%0.2f'%(CostCount)))
sheet.write(count + 1, 4, float('%0.2f'%(RebateCount)))

sheet.write(count + 2, 0, "Madhouse")
sheet.write(count + 2, 3, float('%0.2f'%(MadCost)))
sheet.write(count + 2, 4, float('%0.2f'%(MadCost)))

sheet.write(count + 3, 0, u"品众")
sheet.write(count + 3, 3, float('%0.2f'%(PinzhongCost)))
sheet.write(count + 3, 4, float('%0.2f'%(PinzhongRebate)))

sheet.write(count + 4, 0, u"飞书")
sheet.write(count + 4, 3, float('%0.2f'%(FeishuCost)))
sheet.write(count + 4, 4, float('%0.2f'%(FeishuRebate)))

sheet.write(count + 5, 0, u"蓝标")
sheet.write(count + 5, 3, float('%0.2f'%(LanbiaoCost)))
sheet.write(count + 5, 4, float('%0.2f'%(LanbiaoRebate)))

sheet.write(count + 6, 0, u"木瓜")
sheet.write(count + 6, 3, float('%0.2f'%(MuguaCost)))
sheet.write(count + 6, 4, float('%0.2f'%(MuguaRebate)))

sheet.write(count + 7, 0, u"常乐")
sheet.write(count + 7, 3, float('%0.2f'%(ChangleCost)))
sheet.write(count + 7, 4, float('%0.2f'%(ChangleRebate)))

file_name = "PSMS_AG_Rebate.xls"
file_dir = "/home/ubuntu/code"
wbk.save(file_name)
mail_body = "AG Rebate"
mail_from = "ads_reporting@newborntown.com"
mail_to = ["zhangchen@newborntown.com"]
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
msg['Subject'] = u"一个月内的代理预估返点"
smtp = smtplib.SMTP()
smtp.connect('smtp.exmail.qq.com', 25)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login('ads_reporting@newborntown.com', '5igmKD3F0cLScrS5')
smtp.sendmail(mail_from, mailTo, msg.as_string())
smtp.quit()