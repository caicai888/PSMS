#!/usr/bin/env python
#coding: utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import requests
import datetime, time

time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
# time_now = datetime.datetime.now()
start_date = (datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=720)
time_now = datetime.datetime.strftime(time_now, '%Y-%m-%d')
start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()
# sql = "select offer_id,advertise_series from advertisers where type='facebook' and offer_id in (select id from offer where status != 'deleted')"
ids=60
sql = "select offer_id,advertise_series from advertisers where type='facebook' and offer_id='%d'"%(ids)
cursor.execute(sql)
results = cursor.fetchall()

sql_token = "select accessToken from token where account='rongchangzhang@gmail.com'"
cursor.execute(sql_token)
token_result = cursor.fetchone()
accessToken = token_result[0]

for i in results:
    all_date = []
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
    offerId = i[0]
    advertise_names = i[1].split(",")
    advertise_series = []
    for name in advertise_names:
        campaignRelation_sql = "select campaignId from campaignRelations where campaignName like '%s'"%(name+"%")
        cursor.execute(campaignRelation_sql)
        campaign_name = cursor.fetchall()
        for n in campaign_name:
            advertise_series.append(n[0])
    advertise_series = list(set(advertise_series))
    sql_offer = "select startTime,endTime,contract_type,contract_scale,price from offer where id='%d'"%offerId   #获取offer投放的时间
    cursor.execute(sql_offer)
    runtime = cursor.fetchone()
    startTime = str(runtime[0])  #投放的开始时间
    endTime = str(runtime[1])  #投放的结束时间
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
    if time_ranges != []:
        for campaignId in advertise_series:
            url = "https://graph.facebook.com/v2.8/" + str(campaignId) + "/insights"
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
                conversions = 0
                for action in actions:
                    if "mobile_app_install" in action["action_type"]:
                        conversions = int(action["value"])

                conver_data = {
                    "country": j["country"],
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
                    "date_start": j["date_start"]
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

                country_sql = "select id from country where shorthand='%s'"%country
                cursor.execute(country_sql)
                country_result = cursor.fetchone()
                countryId = country_result[0]

                timePrice_sql = "select price from timePrice where country_id='%d' and offer_id='%d' and date<='%s' and date>='%s' order by date" %(countryId,offerId,date,startTime)
                cursor.execute(timePrice_sql)
                timePrice_result = cursor.fetchone()
                if timePrice_result:
                    price = timePrice_result[0]
                else:
                    history_sql = "select country_price from history where country='%s' and offer_id='%d'order by createdTime"%(country,offerId)
                    cursor.execute(history_sql)
                    history_result = cursor.fetchone()
                    if not history_result:
                        price = offer_price
                    else:
                        price = history_result[0]
                print "+++++"*10
                print price
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

        for l in range(len(impressions_list)):
            country_fb = impressions_list[l].get("country")
            date_fb = impressions_list[l].get("date_start")
            revenue_fb = revenue_list[l].get("revenue")
            profit_fb = profit_list[l].get("profit")
            cost_fb = cost_list[l].get("spend")
            impressions_fb = impressions_list[l].get("impressions")
            clicks_fb = clicks_list[l].get("clicks")
            conversions_fb = conversions_list[l].get("conversions")
            ctr_fb = ctr_list[l].get("ctr")
            cvr_fb = cvr_list[l].get("cvr")
            cpc_fb = cpc_list[l].get("cpc")
            cpi_fb = cpi_list[l].get("cpi")
            data_sql = "select id from datas where offer_id='%d' and country='%s' and date='%s'"%(offerId,country_fb,date_fb)
            cursor.execute(data_sql)
            result = cursor.fetchone()
            if not result:
                insert_sql = "insert into datas(offer_id,type,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi,date,country) values('%d','%s','%f','%f','%f','%d','%d','%d','%s','%s','%s','%s','%s','%s')"%(offerId,"facebook",float(revenue_fb),float(profit_fb),float(cost_fb),impressions_fb,clicks_fb,conversions_fb,ctr_fb,cvr_fb,cpc_fb,cpi_fb,date_fb,country_fb)
                cursor.execute(insert_sql)
                db.commit()
            else:
                update_sql = "update datas set revenue='%f',profit='%f',cost='%f',impressions='%d',clicks='%d',conversions='%d',ctr='%s',cvr='%s',cpc='%s',cpi='%s' where id='%d'"%(float(revenue_fb),float(profit_fb),float(cost_fb),impressions_fb,clicks_fb,conversions_fb,ctr_fb,cvr_fb,cpc_fb,cpi_fb,result[0])
                cursor.execute(update_sql)
                db.commit()
