#!/usr/bin/env python
#coding: utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import requests
import datetime

time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
# time_now = datetime.datetime.now()
start_date = (datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=720)
time_now = datetime.datetime.strftime(time_now, '%Y-%m-%d')
start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()
sql = "select offer_id,facebook_keywords from advertisers where type='facebook' and offer_id in (select id from offer where status != 'deleted')"
cursor.execute(sql)
results = cursor.fetchall()

sql_token = "select accessToken from token where account='rongchangzhang@gmail.com'"
cursor.execute(sql_token)
token_result = cursor.fetchone()
accessToken = token_result[0]

for i in results:
    keywords = i[1].split(",")
    offerId = i[0]
    rebateAmount = 0
    all_date = []
    cost_list = []
    sql_offer = "select startTime,endTime,contract_type,contract_scale,price from platformOffer where offer_id='%d' and platform='facebook'" % offerId
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

    for key in keywords:
        account_sql = "select campaignId,account_id from campaignRelations where campaignName like '%s'"%(key+"%")
        cursor.execute(account_sql)
        account_result = cursor.fetchall()
        if time_ranges != []:
            for j in account_result:
                accountId = j[1]
                campaignId = j[0]
                rebate_sql = "select scale from rebate where accountId='%s'" %(accountId)
                cursor.execute(rebate_sql)
                rebate_result = cursor.fetchone()
                scale = float(rebate_result[0])
                url = "https://graph.facebook.com/v2.8/" + str(campaignId) + "/insights"
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
                    rebate = float(j["spend"])*scale/100
                    j["rebate"] = '%0.2f'%(rebate)
                    cost_list.append(j)

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
                    x['rebate'] += float(ele['rebate'])
        else:
            ele['spend'] = float(ele['spend'])
            ele['rebate'] = float(ele['rebate'])
            tempList.append(key)
            cost_list.append(ele)

    for cost in cost_list:
        updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        data_sql = "select id from datas where offer_id='%d' and type='facebook' and date='%s' and country='%s'" % (offerId,cost["date_start"],cost["country"])
        cursor.execute(data_sql)
        data_result = cursor.fetchone()
        if data_result:
            update_sql = "update datas set rebate=%s,updateTime=%s where id=%s"
            cursor.execute(update_sql,(float(cost["rebate"]),updateTime,data_result[0]))
            db.commit()
        else:
            pass