#!/usr/bin/env python
#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import requests

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()
sql = "select facebook_accountId from advertisers where type='facebook'"
cursor.execute(sql)
results = cursor.fetchall()
accountIds = []
for i in results:
    account_ids = i[0].split(",")
    for j in account_ids:
        accountIds.append(j)

accountIds = list(set(accountIds))

sql_token = "select accessToken from token where account='rongchangzhang@gmail.com'"
cursor.execute(sql_token)
token_result = cursor.fetchone()
accessToken = token_result[0]

for account in accountIds:
    print account
    url = "https://graph.facebook.com/v2.8/act_"+str(account)+"/campaigns"
    params = {
        "access_token": accessToken,
        "level": "account",
        "fields": ["name"],
        "limit": "500"
    }
    result = requests.get(url=url, params=params)
    try:
        data = result.json()["data"]
        for j in data:
            campaignName = j["name"]
            campaignId = j['id']

            search_sql = "select id from campaignRelations where campaignName='%s'"%campaignName
            cursor.execute(search_sql)
            exists = cursor.fetchone()
            if exists:
                pass
            else:
                insert_sql = "insert into campaignRelations(campaignId,campaignName,account_id) values('%s','%s','%s')" % (campaignId,campaignName,account)
                cursor.execute(insert_sql)
                db.commit()
    except Exception:
        pass