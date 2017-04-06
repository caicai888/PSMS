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
    offer_sql = "select app_name,customer_id from offer where id='%d'" % (i[0])
    cursor.execute(offer_sql)
    offer_result = cursor.fetchone()
    appName = offer_result[0]
    customerId = offer_result[1]
    customer_sql = "select company_name from customers where id='%d'" %(customerId)
    cursor.execute(customer_sql)
    customer_result = cursor.fetchone()
    Company = customer_result[0]
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
            "CountProfit": i[5]+rebate,
            "Company": Company
        }
    ]

ap_sql = "select offer_id,date,sum(conversions)conversions,sum(cost)cost,sum(revenue)revenue,sum(profit)profit,sum(rebate)rebate from datas where type='apple' and date='%s' and offer_id in (select id from offer where status != 'deleted') group by offer_id,date" %(startTime)
cursor.execute(ap_sql)
ap_result = cursor.fetchall()
for i in ap_result:
    offer_sql = "select app_name,customer_id from offer where id='%d'" % (i[0])
    cursor.execute(offer_sql)
    offer_result = cursor.fetchone()
    appName = offer_result[0]
    customerId = offer_result[1]
    customer_sql = "select company_name from customers where id='%d'" % (customerId)
    cursor.execute(customer_sql)
    customer_result = cursor.fetchone()
    company = customer_result[0]
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
            "CountProfit": i[5] + rebate,
            "Company": company
        }
    ]

ad_sql = "select offer_id,date,sum(conversions)conversions,sum(cost)cost,sum(revenue)revenue,sum(profit)profit,sum(rebate)rebate from adwords where date='%s' and offer_id in (select id from offer where status != 'deleted') group by offer_id,date" %(startTime)
cursor.execute(ad_sql)
ad_result = cursor.fetchall()
for i in ad_result:
    offer_sql = "select app_name,customer_id from offer where id='%d'" % (i[0])
    cursor.execute(offer_sql)
    offer_result = cursor.fetchone()
    appName = offer_result[0]
    customerId = offer_result[1]
    customer_sql = "select company_name from customers where id='%d'" % (customerId)
    cursor.execute(customer_sql)
    customer_result = cursor.fetchone()
    company = customer_result[0]
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
            "CountProfit": i[5] + rebate,
            "Company": company
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
        ROI = float('%0.4f' % (float(l["Profit"])/float(l["Cost"])))

    l['CPI'] = cpi
    l['Revenue'] = float('%0.2f' % (l["Revenue"]))
    l['Cost'] = float('%0.2f' % (l["Cost"]))
    l["Profit"] = float('%0.2f' % (l['Profit']))
    l["Rebate"] = float('%0.2f' % (l['Rebate']))
    l["CountProfit"] = float('%0.2f' % (l['CountProfit']))
    l["ROI"] = ROI
    all_data_list.append(l)

newlist = sorted(all_data_list, key=lambda k: k['appName'])

wbk = xlwt.Workbook()
sheet = wbk.add_sheet("PM_Data")
sheet.write(0, 0, "Date")
sheet.write(0, 1, "appName")
sheet.write(0, 2, "Company")
sheet.write(0, 3, "Conversions")
sheet.write(0, 4, "CPI")
sheet.write(0, 5, "Cost")
sheet.write(0, 6, "Revenue")
sheet.write(0, 7, "Profit")
sheet.write(0, 8, "Rebate")
sheet.write(0, 9, "CountProfit")
sheet.write(0, 10, "ROI")

total_conversions = 0
total_cpi = 0
total_cost = 0
total_revenue = 0
total_profit = 0
total_rebate = 0
total_countProfit = 0
total_roi = 0

solo_conversions = 0
solo_cpi = 0
solo_cost = 0
solo_revenue = 0
solo_profit = 0
solo_rebate = 0
solo_countProfit = 0
solo_roi = 0

mico_conversions = 0
mico_cpi = 0
mico_cost = 0
mico_revenue = 0
mico_profit = 0
mico_rebate = 0
mico_countProfit = 0
mico_roi = 0

kitty_conversions = 0
kitty_cpi = 0
kitty_cost = 0
kitty_revenue = 0
kitty_profit = 0
kitty_rebate = 0
kitty_countProfit = 0
kitty_roi = 0

count = len(newlist)
for j in range(count):
    total_conversions += int(newlist[j].get("Conversions"))
    total_cost += float(newlist[j].get("Cost"))
    total_revenue += float(newlist[j].get("Revenue"))
    total_profit += float(newlist[j].get("Profit"))
    total_rebate += float(newlist[j].get("Rebate"))
    total_countProfit += float(newlist[j].get("CountProfit"))

    if 'Mico' in newlist[j].get("appName"):
        solo_conversions += int(newlist[j].get("Conversions"))
        solo_cost += float(newlist[j].get("Cost"))
        solo_revenue += float(newlist[j].get("Revenue"))
        solo_profit += float(newlist[j].get("Profit"))
        solo_rebate += float(newlist[j].get("Rebate"))
        solo_countProfit += float(newlist[j].get("CountProfit"))

        mico_conversions += int(newlist[j].get("Conversions"))
        mico_cost += float(newlist[j].get("Cost"))
        mico_revenue += float(newlist[j].get("Revenue"))
        mico_profit += float(newlist[j].get("Profit"))
        mico_rebate += float(newlist[j].get("Rebate"))
        mico_countProfit += float(newlist[j].get("CountProfit"))

    if 'Kitty' in newlist[j].get("appName"):
        solo_conversions += int(newlist[j].get("Conversions"))
        solo_cost += float(newlist[j].get("Cost"))
        solo_revenue += float(newlist[j].get("Revenue"))
        solo_profit += float(newlist[j].get("Profit"))
        solo_rebate += float(newlist[j].get("Rebate"))
        solo_countProfit += float(newlist[j].get("CountProfit"))

        kitty_conversions += int(newlist[j].get("Conversions"))
        kitty_cost += float(newlist[j].get("Cost"))
        kitty_revenue += float(newlist[j].get("Revenue"))
        kitty_profit += float(newlist[j].get("Profit"))
        kitty_rebate += float(newlist[j].get("Rebate"))
        kitty_countProfit += float(newlist[j].get("CountProfit"))

    sheet.write(j+1, 0, newlist[j].get("Date"))
    sheet.write(j+1, 1, newlist[j].get("appName"))
    sheet.write(j+1, 2, newlist[j].get("Company"))
    sheet.write(j+1, 3, newlist[j].get("Conversions"))
    sheet.write(j+1, 4, newlist[j].get("CPI"))
    sheet.write(j+1, 5, newlist[j].get("Cost"))
    sheet.write(j+1, 6, newlist[j].get("Revenue"))
    sheet.write(j+1, 7, newlist[j].get("Profit"))
    sheet.write(j+1, 8, newlist[j].get("Rebate"))
    sheet.write(j+1, 9, newlist[j].get("CountProfit"))
    sheet.write(j+1, 10, newlist[j].get("ROI"))
    continue
if float(total_conversions) != 0:
    total_cpi = float('%0.2f' % (float(total_cost)/float(total_conversions)))
if float(total_cost) != 0:
    total_roi = float('%0.4f' % (float(total_profit)/float(total_cost)))

if float(solo_conversions) != 0:
    solo_cpi = float('%0.2f' % (float(solo_cost)/float(solo_conversions)))
if float(solo_cost) != 0:
    solo_roi = float('%0.4f' % (float(solo_profit)/float(solo_cost)))

if float(mico_conversions) != 0:
    mico_cpi = float('%0.2f' % (float(mico_cost)/float(mico_conversions)))
if float(mico_cost) != 0:
    mico_roi = float('%0.4f' % (float(mico_profit)/float(mico_cost)))

if float(kitty_conversions) != 0:
    kitty_cpi = float('%0.2f' % (float(kitty_cost)/float(kitty_conversions)))
if float(kitty_cost) != 0:
    kitty_roi = float('%0.4f' % (float(kitty_profit)/float(kitty_cost)))

sheet.write(count+1, 0, "Total")
sheet.write(count+1, 3, total_conversions)
sheet.write(count+1, 4, total_cpi)
sheet.write(count+1, 5, float('%0.2f'%(total_cost)))
sheet.write(count+1, 6, float('%0.2f'%(total_revenue)))
sheet.write(count+1, 7, float('%0.2f'%(total_profit)))
sheet.write(count+1, 8, float('%0.2f'%(total_rebate)))
sheet.write(count+1, 9, float('%0.2f'%(total_countProfit)))
sheet.write(count+1, 10, total_roi)

sheet.write(count+2, 0, "SoloTotal")
sheet.write(count+2, 3, solo_conversions)
sheet.write(count+2, 4, solo_cpi)
sheet.write(count+2, 5, float('%0.2f'%(solo_cost)))
sheet.write(count+2, 6, float('%0.2f'%(solo_revenue)))
sheet.write(count+2, 7, float('%0.2f'%(solo_profit)))
sheet.write(count+2, 8, float('%0.2f'%(solo_rebate)))
sheet.write(count+2, 9, float('%0.2f'%(solo_countProfit)))
sheet.write(count+2, 10, solo_roi)

sheet.write(count+3, 0, "MicoTotal")
sheet.write(count+3, 3, mico_conversions)
sheet.write(count+3, 4, mico_cpi)
sheet.write(count+3, 5, float('%0.2f'%(mico_cost)))
sheet.write(count+3, 6, float('%0.2f'%(mico_revenue)))
sheet.write(count+3, 7, float('%0.2f'%(mico_profit)))
sheet.write(count+3, 8, float('%0.2f'%(mico_rebate)))
sheet.write(count+3, 9, float('%0.2f'%(mico_countProfit)))
sheet.write(count+3, 10, mico_roi)

sheet.write(count+4, 0, "KittyTotal")
sheet.write(count+4, 3, kitty_conversions)
sheet.write(count+4, 4, kitty_cpi)
sheet.write(count+4, 5, float('%0.2f'%(kitty_cost)))
sheet.write(count+4, 6, float('%0.2f'%(kitty_revenue)))
sheet.write(count+4, 7, float('%0.2f'%(kitty_profit)))
sheet.write(count+4, 8, float('%0.2f'%(kitty_rebate)))
sheet.write(count+4, 9, float('%0.2f'%(kitty_countProfit)))
sheet.write(count+4, 10, kitty_roi)

file_name = "PSMS_Date.xls"
file_dir = "/home/ubuntu/code"
wbk.save(file_name)
mail_body="PSMS Daliy profit"
mail_from="ads_reporting@newborntown.com"
mail_to = ["greater@newborntown.com","yolanda@newborntown.com","alice@newborntown.com","liping@newborntown.com","salina@newborntown.com"]
mail_cc = ["pm@newborn-town.com","victoria@newborntown.com","zhangchen@newborntown.com","kangyingxin@newborntown.com","liyin@newborntown.com"]
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
msg['Cc'] = ";".join(mail_cc)
msg['date'] = time.strftime('%Y-%m-%d')
msg['Subject'] = u"每日数据预算"+startTime
smtp = smtplib.SMTP()
smtp.connect('smtp.exmail.qq.com',25)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()

smtp.login('ads_reporting@newborntown.com', '5igmKD3F0cLScrS5')
mailTo = mail_to+mail_cc
smtp.sendmail(mail_from, mailTo, msg.as_string())

smtp.quit()
print("ok")