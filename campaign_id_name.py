#!/usr/bin/env python
#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import requests
import datetime,time
import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
import re

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()
# sql = "select facebook_accountId from advertisers where type='facebook' and offer_id in (select id from offer where status != 'deleted')"
sql = "select facebook_accountId from advertisers where type='facebook' and offer_id=75"
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
    url = "https://graph.facebook.com/v2.8/act_"+str(account)+"/campaigns"
    params = {
        "access_token": accessToken,
        "level": "account",
        "fields": ["name"],
        "limit": "500"
    }
    result = requests.get(url=url, params=params)
    print result.json()
    # try:
    data = result.json()["data"]
    for j in data:
        campaignName = j["name"]
        campaignId = j['id']
        print campaignName
        search_sql = "select id from campaignRelations where campaignId='%s' and account_id='%s'"%(campaignId,account)
        cursor.execute(search_sql)
        exists = cursor.fetchone()
        if not exists:
            campaign_name = campaignName.split('_')
            optName = ""
            for c in campaign_name:
                if "66" in c:
                    optName = c
            insert_sql = "insert into campaignRelations(campaignId,campaignName,account_id,optName,account_name) values('%s','%s','%s','%s','%s')" % (campaignId, campaignName, account, optName,'')
            cursor.execute(insert_sql)
            db.commit()
        else:
            campaign_name = campaignName.split('_')
            optName = ""
            for c in campaign_name:
                if "66" in c:
                    optName = c
            update_sql = "update campaignRelations set optName='%s',campaignName='%s',campaignId='%s' where id='%d'" % (optName, campaignName, campaignId, exists[0])
            cursor.execute(update_sql)
            db.commit()
    # except Exception:
    #     pass
    url_account = "https://graph.facebook.com/v2.8/act_"+str(account)+"/insights"
    params = {
        "access_token": accessToken,
        "level": "account",
        "fields": ["account_name"],
        "limit": "500"
    }
    result_account = requests.get(url=url_account,params=params)
    try:
        data_account = result_account.json()["data"]
        account_name = data_account[0]['account_name']
        if re.search('mad',account_name,re.IGNORECASE):
            accountName = 'Madhouse'
        elif re.search('YOYO', account_name, re.IGNORECASE):
            accountName = u'品众'
        elif re.search('Bluefocus',account_name,re.IGNORECASE):
            accountName = u'蓝标'
        elif re.search('PAPAYA',account_name,re.IGNORECASE):
            accountName = u'木瓜'
        elif re.search('Meetsocial',account_name,re.IGNORECASE):
            accountName = u'飞书'
        elif re.search('SUSU',account_name,re.IGNORECASE):
            accountName = u'常乐'
        elif re.search('Advertiser',account_name,re.IGNORECASE):
            accountName = 'Advertiser'
        else:
            accountName = ""
        search_account_sql = "select id from campaignRelations where account_id='%s'" %(account)
        cursor.execute(search_account_sql)
        exists = cursor.fetchone()
        if exists:
            update_account_sql = "update campaignRelations set account_name='%s' where account_id='%s'"%(accountName,account)
            cursor.execute(update_account_sql)
            db.commit()
        else:
            pass
    except Exception:
        pass

# if (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime('%H:%M') >= "07:00":
#     mail_body = "facebook campaign name finished"
#     mail_from = "ads_reporting@newborntown.com"
#     mail_to = "liyin@newborntown.com"
#     msg = MIMEMultipart()
#     body = MIMEText(mail_body)
#     msg.attach(body)
#     msg['From'] = mail_from
#     msg['To'] = mail_to
#     msg['date'] = time.strftime('%Y-%m-%d')
#     msg['Subject'] = "get facebook camapaign name finished"
#     smtp = smtplib.SMTP()
#     smtp.connect('smtp.exmail.qq.com', 25)
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.ehlo()
#     smtp.login('ads_reporting@newborntown.com', '5igmKD3F0cLScrS5')
#     smtp.sendmail(mail_from, mail_to, msg.as_string())
#     smtp.quit()