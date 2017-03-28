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
db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()

all_data = []

fb_sql = "select offer_id,date,sum(conversions)conversions,sum(cost)cost,sum(revenue)revenue,sum(profit)profit,sum(rebate)rebate from datas where type='facebook' and date='%s' and offer_id in (select id from offer where status != 'deleted')" %(startTime)
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
            "appName": appName,
            "Date": i[1],
            "Conversions": int(i[2]),
            "Cost": i[3],
            "Revenue": i[4],
            "Profit": i[5],
            "Rebate": rebate,
            "CountProfit": i[5]+rebate
        }
    ]

ap_sql = "select offer_id,date,sum(conversions)conversions,sum(cost)cost,sum(revenue)revenue,sum(profit)profit,sum(rebate)rebate from datas where type='facebook' and date='%s' and offer_id in (select id from offer where status != 'deleted')" %(startTime)
cursor.execute(ap_sql)