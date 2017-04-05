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
startTime = "2017-02-10"
db = MySQLdb.connect("localhost","root","123456","psms",charset='utf8')
cursor = db.cursor()

role_sql = "select user_id from user_role where role_id=4"
cursor.execute(role_sql)
role_result = cursor.fetchall()
for i in role_result:
    all_data = []
    mail_to = []
    user_sql = "select email,name from user where id='%d'"%(int(i[0]))
    cursor.execute(user_sql)
    user_result = cursor.fetchone()
    if user_result[0] == "Solo@newborntown.com":
        mail_to.append("pm@newborn-town.com")
    else:
        mail_to.append(user_result[0])
    BD = user_result[1]

    offer_sql = "select app_name,id from offer where user_id= '%d' and status !='deleted'" %(int(i[0]))
    cursor.execute(offer_sql)
    offer_result = cursor.fetchall()

    for j in offer_result:
        fb_ap_sql = "select offer_id,date,sum(profit) profit,sum(rebate)rebate from datas where date='%s' and offer_id='%d' group by date,offer_id" %(startTime,j[1])
        cursor.execute(fb_ap_sql)
        fb_ap_result = cursor.fetchall()

        for d in fb_ap_result:
            if d[3] == None:
                rebate = 0
            else:
                rebate = d[3]
            all_data += [
                {
                    "Date": startTime,
                    "BD": BD,
                    "appName": j[0],
                    "CountProfit": d[2] + rebate
                }
            ]

        ad_sql = "select offer_id,date,sum(profit) profit,sum(rebate) rebate from adwords where date='%s' and offer_id='%d' group by date,offer_id" % (startTime,j[1])
        cursor.execute(ad_sql)
        ad_result = cursor.fetchall()
        for d in ad_result:
            if d[3] == None:
                rebate = 0
            else:
                rebate = d[3]

            all_data += [
                {
                    "Date": startTime,
                    "BD": BD,
                    "appName": j[0],
                    "CountProfit": d[2]+rebate
                }
            ]

    tempList = []
    all_data_list_unique = []
    for ele in all_data:
        key = ele['Date'] + ele['BD'] + ele['appName']
        if key in tempList:
            for x in all_data_list_unique:
                if x['Date'] == ele['Date'] and x['BD'] == ele['BD'] and x['appName'] == ele['appName']:
                    x['CountProfit'] += float('%0.2f' % (float(ele['CountProfit'])))

        else:
            ele['CountProfit'] = float('%0.2f' % (float(ele['CountProfit'])))

            tempList.append(key)
            all_data_list_unique.append(ele)

    all_data_list = []
    for l in all_data_list_unique:
        l["CountProfit"] = float('%0.2f' % (l['CountProfit']))
        all_data_list.append(l)
    if len(all_data_list) == 0:
        pass
    else:
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("PM_BD_Data")
        sheet.write(0, 0, "Date")
        sheet.write(0, 1, "BD")
        sheet.write(0, 2, "appName")
        sheet.write(0, 3, "CountProfit")
        totalProfit = 0
        count = len(all_data_list)
        for j in range(count):
            totalProfit += float(all_data_list[j].get("CountProfit"))
            sheet.write(j + 1, 0, all_data_list[j].get("Date"))
            sheet.write(j + 1, 1, all_data_list[j].get("BD"))
            sheet.write(j + 1, 2, all_data_list[j].get("appName"))
            sheet.write(j + 1, 3, all_data_list[j].get("CountProfit"))
            continue
        sheet.write(count+1, 0, 'Total')
        sheet.write(count+1, 3, totalProfit)
        file_name = "PSMS_BD_Profit.xls"
        file_dir = "/home/ubuntu/code"
        wbk.save(file_name)
        mail_body = u"今日收益汇总"
        mail_from = "ads_reporting@newborntown.com"
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
        msg['Subject'] = "PSMS_BD_Profit"
        smtp = smtplib.SMTP()
        smtp.connect('smtp.exmail.qq.com', 25)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('ads_reporting@newborntown.com', '5igmKD3F0cLScrS5')
        smtp.sendmail(mail_from, mailTo, msg.as_string())
        smtp.quit()
print("ok")
