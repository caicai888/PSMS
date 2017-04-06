#!/usr/bin/env python
#coding: utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import requests
import datetime
import re

time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
# time_now = datetime.datetime.now()
start_date = (datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=240)
# start_date = datetime.datetime.now()-datetime.timedelta(hours=240)
time_now = datetime.datetime.strftime(time_now, '%Y-%m-%d')
start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()

all_date = []
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

BM_ids = ["1028817710518180","1746897442253097","1757829464437163","293966850988133","1167706699949156","1674500329444481","463502927174004","1635816073357528","1107609542637861","838474136281412"]
accounts = []
for i in BM_ids:
    accessToken = "EAAHgEYXO0BABABt1QAdnb4kDVpgDv0RcA873EqcNbHFeN8IZANMyXZAU736VKOj1JjSdOPk2WuZC7KwJZBBD76CUbA09tyWETQpOd5OCRSctIo6fuj7cMthZCH6pZA6PZAFmrMgGZChehXreDa3caIZBkBwkyakDAGA4exqgy2sI7JwZDZD"
    url = "https://graph.facebook.com/v2.8/"+str(i)+"/adaccounts"
    params = {
        "access_token": accessToken,
        "fields": ["name"],
        "limit": "500"
    }
    result = requests.get(url=url, params=params)
    data = result.json()["data"]
    for j in data:
        print j
        accounts += [
            {
                "name": j["name"],
                "accountId": j["account_id"]
            }
        ]
accounts_unique = []
for a in accounts:
    if a in accounts_unique:
        pass
    else:
        accounts_unique.append(a)

for i in accounts_unique:
    url = "https://graph.facebook.com/v2.8/act_" + str(i['account_id']) + "/insights"
    params = {
        "access_token": "EAAHgEYXO0BABABt1QAdnb4kDVpgDv0RcA873EqcNbHFeN8IZANMyXZAU736VKOj1JjSdOPk2WuZC7KwJZBBD76CUbA09tyWETQpOd5OCRSctIo6fuj7cMthZCH6pZA6PZAFmrMgGZChehXreDa3caIZBkBwkyakDAGA4exqgy2sI7JwZDZD",
        "level": "account",
        "fields": ["spend"],
        "time_ranges": str(time_ranges)
    }
    result = requests.get(url=url, params=params)
    data = result.json()["data"]
    print data
    if data is None:
        pass
    else:
        for j in data:
            cost = float(j['spend'])
            if re.search('mad', i['name'], re.IGNORECASE):
                accountName = 'Madhouse'
            elif re.search('YOYO', i['name'], re.IGNORECASE):
                accountName = u'品众'
            elif re.search('Bluefocus', i['name'], re.IGNORECASE):
                accountName = u'蓝标'
            elif re.search('PAPAYA', i['name'], re.IGNORECASE):
                accountName = u'木瓜'
            elif re.search('Meetsocial', i['name'], re.IGNORECASE):
                accountName = u'飞书'
            elif re.search('SUSU', i['name'], re.IGNORECASE):
                accountName = u'常乐'
            elif re.search('Advertiser', i['name'], re.IGNORECASE):
                accountName = 'Advertiser'
            else:
                accountName = ""

            rebate_sql = "select scale from rebate where accountName='%s'" %(accountName)
            cursor.execute(rebate_sql)
            rebate_result = cursor.fetchone()
            if rebate_result:
                scale = rebate_result[0]
            else:
                scale = 0
            rebate =  float('%0.2f'%(cost*float(scale)/100))

            account_sql = "select id from accountRebate where accountId='%s' and name='%s' and date='%s'"%(i['account_id'],i['name'],j['date_start'])
            cursor.execute(account_sql)
            account_result = cursor.fetchone()
            if account_result:
                account_update = "update accountRebate set cost='%f',rebate='%f',updateTime='%s' where id='%d'" %(float('%0.2f'%(cost)),rebate,time_now,account_result[0])
                cursor.execute(account_update)
                db.commit()
            else:
                account_insert = "insert into accountRebate(accountId,name,accountName,cost,rebate,date,updateTime) values('%s','%s','%s','%f','%f','%s','%s')" %(i['account_id'],i['name'],accountName,float('%0.2f'%(cost)),rebate,j['date_start'],time_now)
                cursor.execute(account_insert)
                db.commit()