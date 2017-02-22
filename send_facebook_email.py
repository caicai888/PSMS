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
import requests
import base64

time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
time_now_hour=time_now.strftime('%H:%M')
db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()
sql = "select * from offer where email_time='%s' and status != 'deleted'"%(time_now_hour)
cursor.execute(sql)
results = cursor.fetchall()

startTime = ((datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=168)).strftime("%Y-%m-%d")
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
for i in results:
    mail_to = i[31].split(",")
    offerId = i[0]
    contract_type = i[4]
    contract_scale = i[6]
    offer_startTime = i[14]
    offer_price = i[18]
    customer_id = i[2]
    app_name = i[9]
    #获取对应的campaign Id
    sql_advertisers = "select advertise_series from advertisers where type='facebook' and offer_id='%d'"%(offerId)
    cursor.execute(sql_advertisers)
    result = cursor.fetchone()
    if result is not None:
        try:
            advertise_series_all = result[0].split(",")
            advertise_groups = []
            for j in advertise_series_all:
                campaign_name_id_sql = "select campaignId from campaignRelations where campaignName like '%s'"%(j+"%")
                cursor.execute(campaign_name_id_sql)
                campaign_name_id_results = cursor.fetchall()
                for r in campaign_name_id_results:
                    advertise_groups.append(r[0])
            impressions_list = []
            cost_list = []
            clicks_list = []
            conversions_list = []
            ctr_list = []
            cpc_list = []
            cvr_list = []
            cpi_list = []
            revenue_list = []
            profit_list = []
            for i in advertise_groups:
                url = "https://graph.facebook.com/v2.8/" + str(i) + "/insights"
                params = {
                    "access_token": accessToken,
                    "level": "campaign",
                    "fields": ["impressions"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    impressions_list.append(j)
                    params = {
                        "access_token": accessToken,
                        "level": "campaign",
                        "fields": ["spend"],
                        "breakdowns": ["country"],
                        "time_ranges": str(time_ranges)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()["data"]
                    for j in data:
                        cost_list.append(j)

                    params = {
                        "access_token": accessToken,
                        "level": "campaign",
                        "fields": ["clicks"],
                        "breakdowns": ["country"],
                        "time_ranges": str(time_ranges)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()["data"]
                    for j in data:
                        clicks_list.append(j)

                    params = {
                        "access_token": accessToken,
                        "level": "campaign",
                        "fields": ["actions"],
                        "breakdowns": ["country"],
                        "time_ranges": str(time_ranges)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()["data"]
                    for j in data:
                        actions = j.get("actions", [])
                        for action in actions:
                            if "mobile_app_install" in action["action_type"]:
                                conversions = int(action["value"])

                        conver_data = {
                            "country": j["country"],
                            "date_stop": j["date_stop"],
                            "date_start": j["date_start"],
                            "conversions": conversions
                        }
                        conversions_list += [conver_data]

                    params = {
                        "access_token": accessToken,
                        "level": "campaign",
                        "fields": ["ctr"],
                        "breakdowns": ["country"],
                        "time_ranges": str(time_ranges)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()["data"]
                    for j in data:
                        ctr_list.append(j)

                    params = {
                        "access_token": accessToken,
                        "level": "campaign",
                        "fields": ["cpc"],
                        "breakdowns": ["country"],
                        "time_ranges": str(time_ranges)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()["data"]
                    for j in data:
                        data_cpc = {
                            "cpc": '%0.2f' % (float(j["cpc"])),
                            "country": j["country"],
                            "date_start": j["date_start"],
                            "date_stop": j["date_stop"]
                        }
                        cpc_list += [data_cpc]
            impressions_list_unique = []
            for j in impressions_list:
                if j not in impressions_list_unique:
                    impressions_list_unique.append(j)
                else:
                    pass
            tempList = []
            impressions_list = []
            for ele in impressions_list_unique:
                key = ele['date_start'] + ele['country']
                if key in tempList:
                    for x in impressions_list:
                        if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                            x['impressions'] += int(ele['impressions'])
                else:
                    ele['impressions'] = int(ele['impressions'])
                    tempList.append(key)
                    impressions_list.append(ele)

            cost_list_unique = []
            for j in cost_list:
                if j not in cost_list_unique:
                    cost_list_unique.append(j)
                else:
                    pass

            tempList = []
            cost_list = []
            for ele in cost_list_unique:
                key = ele['date_start'] + ele['country']
                if key in tempList:
                    for x in cost_list:
                        if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                            x['spend'] += float(ele['spend'])
                else:
                    ele['spend'] = float(ele['spend'])
                    tempList.append(key)
                    cost_list.append(ele)

            clicks_list_unique = []
            for j in clicks_list:
                if j not in clicks_list_unique:
                    clicks_list_unique.append(j)
                else:
                    pass
            tempList = []
            clicks_list = []
            for ele in clicks_list_unique:
                key = ele['date_start'] + ele['country']
                if key in tempList:
                    for x in clicks_list:
                        if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                            x['clicks'] += float(ele['clicks'])
                else:
                    ele['clicks'] = float(ele['clicks'])
                    tempList.append(key)
                    clicks_list.append(ele)

            conversions_list_unique = []
            for j in conversions_list:
                if j not in conversions_list_unique:
                    conversions_list_unique.append(j)
                else:
                    pass
            tempList = []
            conversions_list = []
            for ele in conversions_list_unique:
                key = ele['date_start'] + ele['country']
                if key in tempList:
                    for x in conversions_list:
                        if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                            x['conversions'] += int(ele['conversions'])
                else:
                    ele['conversions'] = int(ele['conversions'])
                    tempList.append(key)
                    conversions_list.append(ele)

            ctr_list_unique = []
            for j in ctr_list:
                if j not in ctr_list_unique:
                    ctr_list_unique.append(j)
                else:
                    pass
            tempList = []
            ctr_list = []
            for ele in ctr_list_unique:
                key = ele['date_start'] + ele['country']
                if key in tempList:
                    for x in ctr_list:
                        if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                            x['ctr'] += float(ele['ctr'])
                else:
                    ele['ctr'] = float(ele['ctr'])
                    tempList.append(key)
                    ctr_list.append(ele)

            cpc_list_unique = []
            for j in cpc_list:
                if j not in cpc_list_unique:
                    cpc_list_unique.append(j)
                else:
                    pass
            tempList = []
            cpc_list = []
            for ele in cpc_list_unique:
                key = ele['date_start'] + ele['country']
                if key in tempList:
                    for x in cpc_list:
                        if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                            x['cpc'] += float(ele['cpc'])
                else:
                    ele['cpc'] = float(ele['cpc'])
                    tempList.append(key)
                    cpc_list.append(ele)

            if len(conversions_list) >= len(clicks_list):
                count = len(clicks_list)
                len_difference = len(conversions_list) - len(clicks_list)
                for i in range(len_difference):
                    clicks_list += [
                        {
                            "country": conversions_list[count + i].get("country"),
                            "clicks": 0,
                            "date_start": conversions_list[count + i].get("date_start"),
                            "date_stop": conversions_list[count + i].get("date_stop")
                        }
                    ]
            else:
                count = len(conversions_list)
                len_difference = len(clicks_list) - len(conversions_list)
                for i in range(len_difference):
                    conversions_list += [
                        {
                            "country": clicks_list[count + i].get("country"),
                            "conversions": 0,
                            "date_start": clicks_list[count + i].get("date_start"),
                            "date_stop": clicks_list[count + i].get("date_stop")
                        }
                    ]
            for l in conversions_list:
                date_start = l["date_start"]
                country = l["country"]
                for i in clicks_list:
                    if date_start == i["date_start"] and country == i["country"]:
                        cvr = '%0.2f' % (float(l["conversions"]) / float(i["clicks"]) * 100) if float(i["clicks"]) != 0 else 0
                        cvr_list += [
                            {
                                "cvr": cvr,
                                "date_start": date_start,
                                "country": l["country"],
                                "date_stop": date_start
                            }
                        ]
            for l in conversions_list:
                date_start = l["date_start"]
                country = l["country"]
                for i in cost_list:
                    if date_start == i["date_start"] and country == i["country"]:
                        cpi = '%0.2f' % (float(i["spend"]) / float(l["conversions"])) if float(l["conversions"]) != 0 else 0
                        cpi_list += [
                            {
                                "cpi": cpi,
                                "date_start": date_start,
                                "country": l["country"],
                                "date_stop": date_start
                            }
                        ]

            if contract_type == "1":
                for r in range(len(cost_list)):
                    country = cost_list[r].get("country")
                    date = cost_list[r].get("date_start")
                    cost = float(cost_list[r].get("spend"))
                    revenue_list += [
                        {
                            "country": country,
                            "revenue": '%0.2f' % (cost * (1 + float(contract_scale) / 100)),
                            "date_start": date,
                            "date_stop": date
                        }
                    ]
            else:
                for r in range(len(conversions_list)):
                    country = conversions_list[r].get("country")
                    date = conversions_list[r].get("date_start")
                    conversion = float(conversions_list[r].get("conversions"))
                    sql_country = "select id from country where shorthand='%s'"%(country)
                    cursor.execute(sql_country)
                    countries = cursor.fetchone()
                    country_id = countries[0]

                    sql_timePrice = "select price from timePrice where country_id='%d' and offer_id='%d' and date<='%s' and date >='%s' order by date"%(country_id,offerId,date,offer_startTime)
                    cursor.execute(sql_timePrice)
                    time_price = cursor.fetchone()
                    if time_price:
                        price = time_price[0]
                    else:
                        sql_history = "select country_price from history where country='%s' and offer_id='%d'order by createdTime"%(country,offerId)
                        cursor.execute(sql_history)
                        prices_history = cursor.fetchone()
                        if not prices_history:
                            price = offer_price
                        else:
                            price = prices_history[0]

                    revenue_list += [
                        {
                            "country": country,
                            "revenue": '%0.2f' % (float(conversion * price)),
                            "date_start": date,
                            "date_stop": date
                        }
                    ]

            for r in cost_list:
                date_start = r["date_start"]
                country = r["country"]
                for j in revenue_list:
                    if date_start == j["date_start"] and country == j["country"]:
                        profit = '%0.2f' % (float(j["revenue"]) - float(r["spend"]))
                        profit_list += [
                            {
                                "profit": profit,
                                "date_start": date_start,
                                "country": r["country"],
                                "date_stop": date_start
                            }
                        ]
            #发送邮件
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet(app_name.encode("utf8")+u"数据详情")
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
            count = len(conversions_list)
            for j in range(count):
                sheet.write(j+1, 0, impressions_list[j].get("date_start"))
                sheet.write(j+1, 1, impressions_list[j].get("country"))
                sheet.write(j+1, 2, '%0.2f'%(float(revenue_list[j].get("revenue"))))
                sheet.write(j+1, 3, profit_list[j].get("profit"))
                sheet.write(j+1, 4, '%0.2f'%(float(cost_list[j].get("spend"))))
                sheet.write(j+1, 5, impressions_list[j].get("impressions"))
                sheet.write(j+1, 6, clicks_list[j].get("clicks"))
                sheet.write(j+1, 7, conversions_list[j].get("conversions"))
                sheet.write(j+1, 8, '%0.2f'%(float(ctr_list[j].get("ctr"))))
                sheet.write(j+1, 9, '%0.2f'%(float(cvr_list[j].get("cvr"))))
                sheet.write(j+1, 10, '%0.2f'%(float(cpc_list[j].get("cpc"))))
                sheet.write(j+1, 11, '%0.2f'%(float(cpi_list[j].get("cpi"))))
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
