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

# time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
# time_now = datetime.datetime.strftime(time_now, '%Y-%m-%d')
# start_date = (datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=240)
# start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')
start_date = "2017-02-01"
time_now = "2017-02-11"

apple_sql = sql = "select offer_id,apple_appname from advertisers where type='apple' and offer_id in (select id from offer where status != 'deleted')"
cursor.execute(sql)
apple_results = cursor.fetchall()
headers = {}
headers["Authorization"] = "orgId=152120"
headers["Content-Type"] = "application/json"
all_result = []

for i in apple_results:
    all_date = []
    revenue_list = []
    profit_list = []
    offerId = i[0]
    applename = i[1].split(",")
    appleCampaigns = []
    for name in applename:
        campaign_app_name_sql = "select campaignId from campaignAppName where appName='%s'" % (name)
        cursor.execute(campaign_app_name_sql)
        apple_appNames = cursor.fetchall()
        for n in apple_appNames:
            appleCampaigns.append(n[0])
    sql_offer = "select startTime,endTime,contract_type,contract_scale,price from platformOffer where offer_id='%d' and platform='apple'" % offerId
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

        else:
            date1 = datetime.datetime.strptime(startTime, '%Y-%m-%d')
            date2 = datetime.datetime.strptime(time_now, '%Y-%m-%d')
            date_timelta = datetime.timedelta(days=1)
            all_date.append(startTime)
            while date_timelta < (date2 - date1):
                all_date.append((date1 + date_timelta).strftime("%Y-%m-%d"))
                date_timelta += datetime.timedelta(days=1)
            all_date.append(time_now)
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

    for campaignId in appleCampaigns:
        print campaignId
        pem = "/home/ubuntu/appleapi.pem"
        key = "/home/ubuntu/appleapi.key"
        campaign_url = "https://api.searchads.apple.com/api/v1/reports/campaigns/" + str(campaignId) + "/searchterms"
        for date in all_date:
            count_impressions = 0
            count_taps = 0
            count_conversions = 0
            count_cost = 0
            count_cpc = 0
            count_cvr = 0
            count_cpi = 0
            count_ctr = 0
            count_revenue = 0
            params = {
                "startTime": date,
                "endTime": date,
                "selector": {
                    "fields": ["impressions", "conversions", "localSpend"],
                    "orderBy": [{"field": "localSpend", "sortOrder": "DESCENDING"}],
                    "pagination": {"offset": 0, "limit": 1000}
                },
                "groupBy": ["COUNTRY_CODE", "DEVICE_CLASS"],
                "returnRowTotals": True
            }
            result = requests.post(campaign_url, cert=(pem, key), headers=headers, data=json.dumps(params), verify=False)
            rows = result.json()["data"].get("reportingDataResponse")["row"]
            if rows is not None:
                for row in rows:
                    conversions = row["total"].get("conversions")
                    taps = row["total"].get("taps")
                    impressions = row["total"].get("impressions")
                    spend = float(row["total"].get("localSpend")["amount"])
                    count_conversions += conversions
                    count_taps += taps
                    count_impressions += impressions
                    count_cost += spend
            if contract_type == "1":
                cooperation_sql = "select contract_scale from cooperationPer where offer_id='%d' and platform='apple' and date<='%s' and date>='%s' order by date" % (offerId, date, startTime)
                cursor.execute(cooperation_sql)
                cooperation_result = cursor.fetchone()
                if cooperation_result:
                    contract_scale = cooperation_result[0]
                else:
                    history_scale_sql = "select contract_scale from history where platform='apple' and offer_id='%d' order by createdTime desc" % (offerId)
                    cursor.execute(history_scale_sql)
                    history_scale_result = cursor.fetchone()
                    if history_scale_result:
                        contract_scale = history_scale_result[0]
                count_revenue = '%0.2f' % (count_cost * (1 + float(contract_scale) / 100))
            else:
                country_sql = "select id from country where shorthand='US'"
                cursor.execute(country_sql)
                country_result = cursor.fetchone()
                countryId = country_result[0]
                timePrice_sql = "select price from timePrice where country_id='%d' and platform='apple' and offer_id='%d' and date<='%s' and date>='%s' order by date" % (
                countryId, offerId, date, startTime)
                cursor.execute(timePrice_sql)
                timePrice_result = cursor.fetchone()
                if timePrice_result:
                    price = timePrice_result[0]
                else:
                    history_sql = "select country_price from history where country='%s' and platform='apple' and offer_id='%d'order by createdTime desc" % ('US', offerId)
                    cursor.execute(history_sql)
                    history_result = cursor.fetchone()
                    if not history_result:
                        price = offer_price
                    else:
                        price = history_result[0]
                count_revenue = '%0.2f' % (float(count_conversions * price))
            if float(count_conversions) != 0:
                count_cpi = float('%0.2f' % (float(count_cost) / float(count_conversions)))
            if float(count_taps) != 0:
                count_cvr = float('%0.2f' % (float(count_conversions) / float(count_taps) * 100))
                count_cpc = float('%0.2f' % (float(count_cost) / float(count_taps)))
            if float(count_impressions) != 0:
                count_ctr = float('%0.2f' % (float(count_taps) / float(count_impressions)* 100))
            all_result += [
                {
                    "date": date,
                    "impressions": count_impressions,
                    "cost": count_cost,
                    "clicks": count_taps,
                    "conversions": count_conversions,
                    "revenue": count_revenue,
                    "profit": float('%0.2f' % (float(count_revenue) - float(count_cost))),
                    "country": "US",
                    "campaignId": campaignId,
                    "ctr": count_ctr,
                    "cvr": count_cvr,
                    "cpc": count_cpc,
                    "cpi": count_cpi,
                    "rebate": 0,
                    "offer_id": offerId
                }
            ]
updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
for j in all_result:
    campaignId = j["campaignId"]
    date = j["date"]
    country = j["country"]
    offer_id = j["offer_id"]
    revenue = float('%0.2f'%(float(j["revenue"])))
    cost = float('%0.2f'%(float(j["cost"])))
    profit = float('%0.2f'%(float(j["profit"])))
    impressions = int(j["impressions"])
    clicks = int(j["clicks"])
    conversions = int(j["conversions"])
    ctr = float('%0.2f'%(float(j["ctr"])))
    cvr = float('%0.2f' % (float(j["cvr"])))
    cpc = float('%0.2f' % (float(j["cpc"])))
    cpi = float('%0.2f' % (float(j["cpi"])))
    rebate = j["rebate"]
    opt_sql = "select optName from campaignAppName where campaignId='%s'"%campaignId
    cursor.execute(opt_sql)
    opt_result = cursor.fetchone()
    optName = opt_result[0]

    datadetail_sql = "select id from dataDetail where offer_id='%d' and country='%s' and date='%s' and campaignId='%s' and type='apple'" % (offer_id, country, date,campaignId)
    cursor.execute(datadetail_sql)
    datadetail_result = cursor.fetchone()
    if datadetail_result:
        update_sql = "update dataDetail set revenue=%s,profit=%s,cost=%s,impressions=%s,clicks=%s,conversions=%s,ctr=%s,cvr=%s,cpc=%s,cpi=%s,rebate=%s,optName=%s,updateTime=%s where id=%s"
        cursor.execute(update_sql, (revenue, profit, cost, impressions, clicks, conversions, ctr, cvr, cpc, cpi, rebate, optName,updateTime,datadetail_result[0]))
        db.commit()
    else:
        insert_sql = "insert into dataDetail(offer_id,account_id,campaignId,type,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi,date,country,rebate,optName,updateTime) values('%d','%s','%s','%s','%f','%f','%f','%d','%d','%d','%f','%f','%f','%f','%s','%s','%f','%s','%s')" % (offer_id, '', campaignId, 'apple', revenue, profit, cost, impressions, clicks, conversions, ctr, cvr,cpc, cpi, date,country, rebate, optName, updateTime)
        cursor.execute(insert_sql)
        db.commit()

print "ok"