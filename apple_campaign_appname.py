#!/usr/bin/env python
#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import requests
import datetime
import json

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()

url = "https://api.searchads.apple.com/api/v1/reports/campaigns"
pem = "/home/ubuntu/appleapi.pem"
key = "/home/ubuntu/appleapi.key"

headers = {}
headers["Authorization"] = "orgId=152120"
headers["Content-Type"] = "application/json"

date1 = "2017-02-26"
all_date = []
time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
time_now = datetime.datetime.strftime(time_now, '%Y-%m-%d')
all_date.append(date1)
date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
date2 = datetime.datetime.strptime(time_now, '%Y-%m-%d')
date_timelta = datetime.timedelta(days=1)
while date_timelta < (date2 - date1):
    all_date.append((date1 + date_timelta).strftime("%Y-%m-%d"))
    date_timelta += datetime.timedelta(days=1)
all_date.append(time_now)
print all_date
for i in all_date:
    params = {
        "startTime": i,
        "endTime": i,
        "selector":{
            "fields": ["campaignId","campaignName","appName"],
            "orderBy":[{"field":"campaignId","sortOrder":"DESCENDING"}],
            "pagination": { "offset": 0, "limit": 1000}
        },
        "groupBy":["COUNTRY_CODE", "DEVICE_CLASS"],
        "returnRowTotals": True
    }
    result = requests.post(url, cert=(pem, key),headers=headers, data=json.dumps(params),verify=False)

    rows = result.json()['data'].get('reportingDataResponse')['row']
    apple_campaign_app =[]
    apple_campaign_appname = []
    if rows is not None:
        for i in rows:
            campaignId = str(i['metadata'].get('campaignId'))
            campaignName = i['metadata'].get('campaignName')
            appId = str(i['metadata'].get('app')['adamId'])
            appName = i['metadata'].get('app')['appName']
            result = {
                "campaignId": campaignId,
                "campaignName": campaignName,
                "appId": appId,
                "appName": appName
            }
            apple_campaign_app += [result]

    for j in apple_campaign_app:
        if j not in apple_campaign_appname:
            apple_campaign_appname.append(j)

    print apple_campaign_appname
    for i in apple_campaign_appname:
        search_sql = "select id from campaignAppName where appName='%s' and campaignId='%s'" %(i["appName"],i["campaignId"])
        cursor.execute(search_sql)
        exists = cursor.fetchone()
        if exists:
            pass
        else:
            insert_sql = "insert into campaignAppName(campaignId,campaignName,appId,appName) values('%s','%s','%s','%s')"%(i["campaignId"],i["campaignName"],i["appId"],i["appName"])
            cursor.execute(insert_sql)
            db.commit()