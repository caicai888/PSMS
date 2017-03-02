#!/usr/bin/env python
#coding: utf-8
from __future__ import division
import requests
import json
import MySQLdb
import datetime

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()

time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
start_date = (datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=240)
time_now = datetime.datetime.strftime(time_now, '%Y-%m-%d')
start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')

sql = "select offer_id,apple_appname from advertisers where type='apple' and offer_id in (select id from offer where status != 'deleted')"
cursor.execute(sql)
results = cursor.fetchall()

headers = {}
headers["Authorization"] = "orgId=152120"
headers["Content-Type"] = "application/json"
#根据campign id获取impressions等数据信息
for i in results:
    print i
    all_date = []
    all_result = []
    revenue_list = []
    profit_list = []
    offerId = i[0]
    applename = i[1].split(",")
    appleCampaigns = []
    for name in applename:
        campaign_app_name_sql = "select campaignId from campaignAppName where appName='%s'"%(name)
        cursor.execute(campaign_app_name_sql)
        apple_appNames = cursor.fetchall()
        for n in apple_appNames:
            appleCampaigns.append(n[0])
    appleCampaigns=list(set(appleCampaigns))
    sql_offer = "select startTime,endTime,contract_type,contract_scale,price from offer where id='%d'"%offerId
    cursor.execute(sql_offer)
    runtime = cursor.fetchone()
    startTime = str(runtime[0])  # 投放的开始时间
    endTime = str(runtime[1])  # 投放的结束时间
    contract_type = runtime[2]
    contract_scale = runtime[3]
    offer_price = runtime[4]
    if time_now <= endTime:
        if start_date >= startTime:
            #获取时间段中的每一天
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

    if all_date != []:
        for campaignId in appleCampaigns:
            pem = "/home/ubuntu/appleapi.pem"
            key = "/home/ubuntu/appleapi.key"
            campaign_url = "https://api.searchads.apple.com/api/v1/reports/campaigns/"+str(campaignId)+"/searchterms"
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
                    "startTime":date,
                    "endTime": date,
                    "selector":{
                        "fields":["impressions","conversions","localSpend"],
                        "orderBy":[{"field":"localSpend","sortOrder":"DESCENDING"}],
                        "pagination": { "offset": 0, "limit": 1000}
                    },
                    "groupBy":["COUNTRY_CODE", "DEVICE_CLASS"],
                    "returnRowTotals": True
                }
                result = requests.post(campaign_url, cert=(pem, key),headers=headers, data=json.dumps(params),verify=False)
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
                    count_revenue = '%0.2f' % (count_cost * (1 + float(contract_scale) / 100))
                else:
                    country_sql = "select id from country where shorthand='US'"
                    cursor.execute(country_sql)
                    country_result = cursor.fetchone()
                    countryId = country_result[0]
                    timePrice_sql = "select price from timePrice where country_id='%d' and offer_id='%d' and date<='%s' and date>='%s' order by date" % (countryId, offerId, date, startTime)
                    cursor.execute(timePrice_sql)
                    timePrice_result = cursor.fetchone()
                    if timePrice_result:
                        price = timePrice_result[0]
                    else:
                        history_sql = "select country_price from history where country='%s' and offer_id='%d'order by createdTime desc" % ('US', offerId)
                        cursor.execute(history_sql)
                        history_result = cursor.fetchone()
                        if not history_result:
                            price = offer_price
                        else:
                            price = history_result[0]
                    count_revenue = '%0.2f' % (float(count_conversions * price))
                all_result += [
                    {
                        "date": date,
                        "impressions": count_impressions,
                        "cost": count_cost,
                        "clicks": count_taps,
                        "conversions": count_conversions,
                        "revenue": count_revenue,
                        "profit": '%0.2f'%(float(count_revenue)-float(count_cost)),
                        "country": "US"
                    }
                ]
    templist = []
    resultlist = []
    for ele in all_result:
        key = ele["date"] + ele["country"]
        if key in templist:
            for x in resultlist:
                if x["date"] == ele["date"] and x["country"] == ele["country"]:
                    x["impressions"] += int(ele["impressions"])
                    x["cost"] += float(ele["cost"])
                    x["clicks"] += int(ele["clicks"])
                    x["conversions"] += int(ele["conversions"])

        else:
            ele["impressions"] = int(ele["impressions"])
            ele["cost"] = float(ele["cost"])
            ele["clicks"] = int(ele["clicks"])
            ele["conversions"] = int(ele["conversions"])
            templist.append(key)
            resultlist.append(ele)

    for l in resultlist:
        l_cpc = '%0.2f'%(float(l["cost"]) / float(l["clicks"])) if l["clicks"] != 0 else 0
        l_cvr = '%0.2f' % (float(l["conversions"] / l["clicks"] * 100)) if l["clicks"] != 0 else 0
        l_cpi = '%0.2f'%(float(l["cost"]) / float(l["conversions"])) if l["conversions"] != 0 else 0
        l_ctr = '%0.2f' % (float(l["clicks"] / l["impressions"] * 100)) if l["impressions"] != 0 else 0
        data_sql = "select id from datas where offer_id='%d' and country='%s' and date='%s' and type='apple'" % (offerId, l["country"], l["date"])
        cursor.execute(data_sql)
        result_apple = cursor.fetchone()
        if not result_apple:
            insert_sql = "insert into datas(offer_id,type,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi,date,country) values('%d','%s','%f','%f','%f','%d','%d','%d','%s','%s','%s','%s','%s','%s')" % (
            offerId, "apple", float(l["revenue"]), float(l["profit"]), float(l["cost"]), l["impressions"], l["clicks"], l["conversions"], l_ctr, l_cvr,l_cpc, l_cpi, l["date"], l["country"])
            cursor.execute(insert_sql)
            db.commit()
        else:
            update_sql = "update datas set revenue='%f',profit='%f',cost='%f',impressions='%d',clicks='%d',conversions='%d',ctr='%s',cvr='%s',cpc='%s',cpi='%s' where id='%d'" % (float(l["revenue"]), float(l["profit"]), float(l["cost"]), l["impressions"], l["clicks"],l["conversions"], l_ctr, l_cvr,l_cpc, l_cpi, result_apple[0])
            cursor.execute(update_sql)
            db.commit()