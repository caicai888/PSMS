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

detail_sql = "select date,account_id,sum(cost) cost from dataDetail where date='%s' and type='facebook' group by date,account_id" % (startTime)
cursor.execute(detail_sql)
detail_result = cursor.fetchall()
for i in detail_result:
    account_sql = "select "