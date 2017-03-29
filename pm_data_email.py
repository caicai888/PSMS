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

startTime = (datetime.datetime.now()+datetime.timedelta(hours=8)-datetime.timedelta(hours=24)).strftime("%Y-%m-%d")
print startTime
startTime = "2017-02-10"
db = MySQLdb.connect("localhost","root","123456","psms",charset='utf8')
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
                x['Revenue'] += float('%0.3f' % (float(ele['Revenue'])))
                x['Cost'] += float('%0.3f' % (float(ele['Cost'])))
                x['Profit'] += float('%0.3f' % (float(ele['Profit'])))
                x['Rebate'] += float('%0.3f' % (float(ele['Rebate'])))
                x['CountProfit'] += float('%0.3f' % (float(ele['CountProfit'])))

    else:
        ele['Conversions'] = int(ele['Conversions'])
        ele['Revenue'] = float(ele['Revenue'])
        ele['Cost'] = float('%0.3f' % (float(ele['Cost'])))
        ele['Profit'] = float('%0.3f' % (float(ele['Profit'])))
        ele['Rebate'] = float('%0.3f' % (float(ele['Rebate'])))
        ele['CountProfit'] = float('%0.3f' % (float(ele['CountProfit'])))

        tempList.append(key)
        all_data_list_unique.append(ele)
newlist = sorted(all_data_list_unique, key=lambda k: k['appName'])

wbk = xlwt.Workbook()
sheet = wbk.add_sheet("PM_Data")