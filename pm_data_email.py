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

startTime = (datetime.datetime.now()+datetime.timedelta(hours=8)-datetime.timedelta(hours=24)).strftime("%Y-%m-%d")
db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()

all_data = []

fb_sql = "select offer_id,date,sum(conversions)conversions,sum(cost)cost,sum(revenue)revenue,sum(profit)profit,sum(rebate)rebate from datas where type='facebook' and date='%s' and offer_id in (select id from offer where status != 'deleted') group by offer_id,date" %(startTime)
cursor.execute(fb_sql)
fb_result = cursor.fetchall()
for i in fb_result:
    offer_sql = "select app_name from offer where id='%d'" % (i[0])
    cursor.execute(offer_sql)
    offer_result = cursor.fetchone()
    appName = offer_result[0]
    if i[6] == None:
        rebate = 0
    else:
        rebate = i[6]
    all_data += [
        {
            "appName": appName+"_FB",
            "Date": i[1],
            "Conversions": int(i[2]),
            "Cost": i[3],
            "Revenue": i[4],
            "Profit": i[5],
            "Rebate": rebate,
            "CountProfit": i[5]+rebate
        }
    ]

ap_sql = "select offer_id,date,sum(conversions)conversions,sum(cost)cost,sum(revenue)revenue,sum(profit)profit,sum(rebate)rebate from datas where type='apple' and date='%s' and offer_id in (select id from offer where status != 'deleted') group by offer_id,date" %(startTime)
cursor.execute(ap_sql)
ap_result = cursor.fetchall()
for i in ap_result:
    offer_sql = "select app_name from offer where id='%d'" % (i[0])
    cursor.execute(offer_sql)
    offer_result = cursor.fetchone()
    appName = offer_result[0]
    if i[6] == None:
        rebate = 0
    else:
        rebate = i[6]
    all_data += [
        {
            "appName": appName+"_AP",
            "Date": i[1],
            "Conversions": int(i[2]),
            "Cost": i[3],
            "Revenue": i[4],
            "Profit": i[5],
            "Rebate": rebate,
            "CountProfit": i[5] + rebate
        }
    ]

ad_sql = "select offer_id,date,sum(conversions)conversions,sum(cost)cost,sum(revenue)revenue,sum(profit)profit,sum(rebate)rebate from adwords where date='%s' and offer_id in (select id from offer where status != 'deleted') group by offer_id,date" %(startTime)
cursor.execute(ad_sql)
ad_result = cursor.fetchall()
for i in ad_result:
    offer_sql = "select app_name from offer where id='%d'" % (i[0])
    cursor.execute(offer_sql)
    offer_result = cursor.fetchone()
    appName = offer_result[0]
    if i[6] == None:
        rebate = 0
    else:
        rebate = i[6]
    all_data += [
        {
            "appName": appName+"_ADW",
            "Date": i[1],
            "Conversions": int(i[2]),
            "Cost": i[3],
            "Revenue": i[4],
            "Profit": i[5],
            "Rebate": rebate,
            "CountProfit": i[5] + rebate
        }
    ]

tempList = []
all_data_list_unique = []
for ele in all_data:
    key = ele['Date'] + ele['appName']
    if key in tempList:
        for x in all_data_list_unique:
            if x['Date'] == ele['Date'] and x['appName'] == ele['appName']:
                x['Conversions'] += int(ele['Conversions'])
                x['Revenue'] += float('%0.2f' % (float(ele['Revenue'])))
                x['Cost'] += float('%0.2f' % (float(ele['Cost'])))
                x['Profit'] += float('%0.2f' % (float(ele['Profit'])))
                x['Rebate'] += float('%0.2f' % (float(ele['Rebate'])))
                x['CountProfit'] += float('%0.2f' % (float(ele['CountProfit'])))

    else:
        ele['Conversions'] = int(ele['Conversions'])
        ele['Revenue'] = float(ele['Revenue'])
        ele['Cost'] = float('%0.2f' % (float(ele['Cost'])))
        ele['Profit'] = float('%0.2f' % (float(ele['Profit'])))
        ele['Rebate'] = float('%0.2f' % (float(ele['Rebate'])))
        ele['CountProfit'] = float('%0.2f' % (float(ele['CountProfit'])))

        tempList.append(key)
        all_data_list_unique.append(ele)
all_data_list = []
for l in all_data_list_unique:
    if float(l['Conversions']) != 0:
        cpi = float('%0.2f' % (float(l['Cost'])/float(l['Conversions'])))
    if float(l["Cost"]) != 0:
        ROI = float('%0.2f' % (float(l["Profit"])/float(l["Cost"])))

    l['CPI'] = cpi
    l['Revenue'] = float('%0.2f' % (l["Revenue"]))
    l['Cost'] = float('%0.2f' % (l["Cost"]))
    l["Profit"] = float('%0.2f' % (l['Profit']))
    l["Rebate"] = float('%0.2f' % (l['Rebate']))
    l["CountProfit"] = float('%0.2f' % (l['CountProfit']))
    l["ROI"] = ROI

newlist = sorted(all_data_list, key=lambda k: k['appName'])

wbk = xlwt.Workbook()
sheet = wbk.add_sheet("PM_Data")
sheet.write(0, 0, "Date")
sheet.write(0, 1, "appName")
sheet.write(0, 2, "Conversions")
sheet.write(0, 3, "CPI")
sheet.write(0, 4, "Cost")
sheet.write(0, 5, "Revenue")
sheet.write(0, 6, "Profit")
sheet.write(0, 7, "Rebate")
sheet.write(0, 8, "CountProfit")
sheet.write(0, 9, "ROI")

count = len(all_data_list)
for j in range(count):
    sheet.write(j+1, 0, all_data_list[j].get("Date"))
    sheet.write(j+1, 1, all_data_list[j].get("appName"))
    sheet.write(j+1, 2, all_data_list[j].get("Conversions"))
    sheet.write(j+1, 3, all_data_list[j].get("CPI"))
    sheet.write(j+1, 4, all_data_list[j].get("Cost"))
    sheet.write(j+1, 5, all_data_list[j].get("Revenue"))
    sheet.write(j+1, 6, all_data_list[j].get("Profit"))
    sheet.write(j+1, 7, all_data_list[j].get("Rebate"))
    sheet.write(j+1, 8, all_data_list[j].get("CountProfit"))
    sheet.write(j+1, 9, all_data_list[j].get("ROI"))
    continue

file_name = "PSMS_Date.xls"
file_dir = "/home/ubuntu/code"
wbk.save(file_name)
mail_body="data"
mail_from="liyin@newborntown.com"
mail_to = "liyin@newborntown.com"
msg = MIMEMultipart()
body = MIMEText(mail_body)
msg.attach(body)
part = MIMEBase('application', 'octet-stream')
part.set_payload(open(file_name, 'rb').read())
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="' + file_name.encode("utf8") + '"')
msg.attach(part)

msg['From'] = mail_from
msg['To'] = mail_to
msg['date'] = time.strftime('%Y-%m-%d')
msg['Subject'] = "pspm_Data"
smtp = smtplib.SMTP()
smtp.connect('smtp.exmail.qq.com',25)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login('liyin@newborn-town.com', '920130LiY')
smtp.sendmail(mail_from, mail_to, msg.as_string())
smtp.quit()
print("ok")