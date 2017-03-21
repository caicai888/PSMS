#!/usr/bin/env python
#coding: utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import requests
import datetime,time
import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
import json

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()

time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
time_now = datetime.datetime.strftime(time_now, '%Y-%m-%d')
start_date = (datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=720)
start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')
# start_date = "2017-02-02"

sql_token = "select accessToken from token where account='rongchangzhang@gmail.com'"
cursor.execute(sql_token)
token_result = cursor.fetchone()
accessToken = token_result[0]

impressions_list = []
cost_list = []
revenue_list = []
clicks_list = []
conversions_list = []
profit_list = []
ctr_list = []
cpc_list = []
keywords_sql = "select offer_id,facebook_keywords from advertisers where type='facebook' and offer_id in (select id from offer where status != 'deleted')"
# keywords_sql = "select offer_id,facebook_keywords from advertisers where type='facebook' and offer_id=10"
cursor.execute(keywords_sql)
keywords_result = cursor.fetchall()
for i in keywords_result:
    all_date = []
    offer_id = i[0]
    keywords = i[1].split(',')
    sql_offer = "select startTime,endTime,contract_type,contract_scale,price from platformOffer where offer_id='%d' and platform='facebook'" % offer_id
    cursor.execute(sql_offer)
    runtime = cursor.fetchone()
    startTime = str(runtime[0])  # 投放的开始时间
    endTime = str(runtime[1])  # 投放的结束时间
    contract_type = runtime[2]
    contract_scale = runtime[3]
    offer_price = runtime[4]
    if time_now <= endTime:
        if start_date >= startTime:
            # 获取时间段中的每一天
            date1 = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            date2 = datetime.datetime.strptime(time_now, '%Y-%m-%d')
            date_timelta = datetime.timedelta(days=1)
            all_date.append(start_date)
            while date_timelta < (date2 - date1):
                all_date.append((date1 + date_timelta).strftime("%Y-%m-%d"))
                date_timelta += datetime.timedelta(days=1)
            all_date.append(time_now)

            time_ranges = []
            for day in all_date[::-1]:
                time_ranges.append("{'since': " + "'" + str(day) + "'" + ", 'until': " + "'" + str(day) + "'" + "}")
        else:
            date1 = datetime.datetime.strptime(startTime, '%Y-%m-%d')
            date2 = datetime.datetime.strptime(time_now, '%Y-%m-%d')
            date_timelta = datetime.timedelta(days=1)
            all_date.append(startTime)
            while date_timelta < (date2 - date1):
                all_date.append((date1 + date_timelta).strftime("%Y-%m-%d"))
                date_timelta += datetime.timedelta(days=1)
            all_date.append(time_now)

            time_ranges = []
            for day in all_date[::-1]:
                time_ranges.append("{'since': " + "'" + str(day) + "'" + ", 'until': " + "'" + str(day) + "'" + "}")
    else:
        if start_date <= endTime:
            date1 = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            date2 = datetime.datetime.strptime(endTime, '%Y-%m-%d')
            date_timelta = datetime.timedelta(days=1)
            all_date.append(start_date)
            while date_timelta < (date2 - date1):
                all_date.append((date1 + date_timelta).strftime("%Y-%m-%d"))
                date_timelta += datetime.timedelta(days=1)
            all_date.append(endTime)

            time_ranges = []
            for day in all_date[::-1]:
                time_ranges.append("{'since': " + "'" + str(day) + "'" + ", 'until': " + "'" + str(day) + "'" + "}")
        else:
            time_ranges = []
    for j in keywords:
        relations_sql = "select campaignId from campaignRelations where campaignName like '%s'" % (j+"%")
        cursor.execute(relations_sql)
        relations_result = cursor.fetchall()
        for campaignId in relations_result:
            print campaignId[0],offer_id
            url = "https://graph.facebook.com/v2.8/"+str(campaignId[0])+"/insights"
            params = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["impressions"],
                "breakdowns": ["country"],
                "time_ranges": str(time_ranges)
            }
            result = requests.get(url=url, params=params)
            data = result.json()["data"]
            for d in data:
                d["offer_id"] = offer_id
                d["campaignId"] = campaignId[0]
                impressions_list.append(d)

            params = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["spend"],
                "breakdowns": ["country"],
                "time_ranges": str(time_ranges)
            }
            result = requests.get(url=url, params=params)
            data = result.json()["data"]
            for d in data:
                d["offer_id"] = offer_id
                d["campaignId"] = campaignId[0]
                cost_list.append(d)

            params = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["clicks"],
                "breakdowns": ["country"],
                "time_ranges": str(time_ranges)
            }
            result = requests.get(url=url, params=params)
            data = result.json()["data"]
            for d in data:
                d["offer_id"] = offer_id
                d["campaignId"] = campaignId[0]
                clicks_list.append(d)

            params = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["actions"],
                "breakdowns": ["country"],
                "time_ranges": str(time_ranges)
            }
            result = requests.get(url=url, params=params)
            data = result.json()["data"]
            for d in data:
                actions = d.get("actions", [])
                conversions = 0
                for action in actions:
                    if "mobile_app_install" in action["action_type"]:
                        conversions = int(action["value"])

                conver_data = {
                    "country": d["country"],
                    "date_start": d["date_start"],
                    "conversions": conversions,
                    "offer_id": offer_id,
                    "campaignId": campaignId[0]
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
            for d in data:
                d["offer_id"] = offer_id
                d["campaignId"] = campaignId[0]
                ctr_list.append(d)

            params = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["cpc"],
                "breakdowns": ["country"],
                "time_ranges": str(time_ranges)
            }
            result = requests.get(url=url, params=params)
            data = result.json()["data"]
            for d in data:
                data_cpc = {
                    "cpc": float('%0.2f' % (float(d["cpc"]))),
                    "country": d["country"],
                    "date_start": d["date_start"],
                    "offer_id": offer_id,
                    "campaignId": campaignId[0]
                }
                cpc_list += [data_cpc]

    if contract_type == "1":
        for r in range(len(cost_list)):
            country = cost_list[r].get("country")
            date = cost_list[r].get("date_start")
            cost = float(cost_list[r].get("spend"))
            cooperation_sql = "select contract_scale from cooperationPer where offer_id='%d' and platform='facebook' and date<='%s' and date>='%s' order by date" % (cost_list[r].get("offer_id"), date, startTime)
            cursor.execute(cooperation_sql)
            cooperation_result = cursor.fetchone()
            if cooperation_result:
                contract_scale = cooperation_result[0]
            else:
                history_scale_sql = "select contract_scale from history where platform='facebook' and offer_id='%d' order by createdTime desc" % (cost_list[r].get("offer_id"))
                cursor.execute(history_scale_sql)
                history_scale_result = cursor.fetchone()
                if history_scale_result:
                    contract_scale = history_scale_result[0]
            revenue_list += [
                {
                    "country": country,
                    "revenue": float('%0.2f' % (cost * (1 + float(contract_scale) / 100))),
                    "date_start": date,
                    "date_stop": date
                }
            ]
    else:
        for r in range(len(conversions_list)):
            country = conversions_list[r].get("country")
            date = conversions_list[r].get("date_start")
            conversion = float(conversions_list[r].get("conversions"))

            country_sql = "select id from country where shorthand='%s'" % country
            cursor.execute(country_sql)
            country_result = cursor.fetchone()
            countryId = country_result[0]
            timePrice_sql = "select price from timePrice where country_id='%d' and platform='facebook' and offer_id='%d' and date<='%s' and date>='%s' order by date desc" % (countryId, conversions_list[r].get("offer_id"), date, startTime)
            cursor.execute(timePrice_sql)
            timePrice_result = cursor.fetchone()
            if timePrice_result:
                price = timePrice_result[0]
            else:
                history_sql = "select country_price from history where country='%s' and platform='facebook' and offer_id='%d'order by createdTime desc" % (country, conversions_list[r].get("offer_id"))
                cursor.execute(history_sql)
                history_result = cursor.fetchone()
                if not history_result:
                    price = offer_price
                else:
                    price = history_result[0]

            revenue_list += [
                {
                    "country": country,
                    "revenue": float('%0.2f' % (float(conversion * price))),
                    "date_start": date,
                    "date_stop": date
                }
            ]

    for r in cost_list:
        date_start = r["date_start"]
        country = r["country"]
        for j in revenue_list:
            if date_start == j["date_start"] and country == j["country"]:
                profit = float('%0.2f' % (float(j["revenue"]) - float(r["spend"])))
                profit_list += [
                    {
                        "profit": profit,
                        "date_start": date_start,
                        "country": r["country"],
                        "date_stop": date_start
                    }
                ]

updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
for l in range(len(impressions_list)):
    cpi_fb = 0
    cvr_fb = 0
    rebate_fb = 0
    offer_id = impressions_list[l].get("offer_id")
    campaignId = impressions_list[l].get("campaignId")
    country_fb = impressions_list[l].get("country")
    date_fb = impressions_list[l].get("date_start")
    revenue_fb = float(revenue_list[l].get("revenue"))
    profit_fb = float(profit_list[l].get("profit"))
    cost_fb = float(cost_list[l].get("spend"))
    impressions_fb = int(impressions_list[l].get("impressions"))
    clicks_fb = int(clicks_list[l].get("clicks"))
    ctr_fb = float(ctr_list[l].get("ctr"))
    cpc_fb = float(cpc_list[l].get("cpc"))
    conversions_fb = int(conversions_list[l].get("conversions"))
    if float(conversions_fb) != 0:
        cpi_fb = float('%0.2f' % (float(cost_fb) / float(conversions_fb)))
    if float(clicks_fb) != 0:
        cvr_count = float('%0.2f' % (float(conversions_fb) / float(clicks_fb) * 100))

    account_sql = "select account_id,optName from campaignRelations where campaignId='%s'" %campaignId
    cursor.execute(account_sql)
    account_result = cursor.fetchone()
    accountId = account_result[0]
    optName = account_result[1]
    print optName
    rebate_sql = "select scale from rebate where accountId='%s'" % (accountId)
    cursor.execute(rebate_sql)
    rebate_result = cursor.fetchone()
    rebate_fb = float('%0.2f' % (float(cost_fb) * float(rebate_result[0]) / 100))

    datadetail_sql = "select id from dataDetail where offer_id='%d' and country='%s' and date='%s' and campaignId='%s' and type='facebook'"%(offer_id,country_fb,date_fb,campaignId)
    cursor.execute(datadetail_sql)
    datadetail_result = cursor.fetchone()
    if datadetail_result:
        update_sql = "update dataDetail set revenue=%s,profit=%s,cost=%s,impressions=%s,clicks=%s,conversions=%s,ctr=%s,cvr=%s,cpc=%s,cpi=%s,rebate=%s,optName=%s,updateTime=%s where id=%s"
        cursor.execute(update_sql,(revenue_fb,profit_fb,cost_fb,impressions_fb,clicks_fb,conversions_fb,ctr_fb,cvr_fb,cpc_fb,cpi_fb,rebate_fb,optName,updateTime,datadetail_result[0]))
        db.commit()
    else:
        insert_sql = "insert into dataDetail(offer_id,account_id,campaignId,type,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi,date,country,rebate,optName,updateTime) values('%d','%s','%s','%s','%f','%f','%f','%d','%d','%d','%f','%f','%f','%f','%s','%s','%f','%s','%s')" % (offer_id,accountId,campaignId,'facebook',revenue_fb,profit_fb,cost_fb,impressions_fb,clicks_fb,conversions_fb,ctr_fb,cvr_fb,cpc_fb,cpi_fb,date_fb,country_fb,rebate_fb,optName,updateTime)
        cursor.execute(insert_sql)
        db.commit()

print "ok"