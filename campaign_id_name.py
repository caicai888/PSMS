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

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()
sql = "select facebook_accountId from advertisers where type='facebook' and offer_id in (select id from offer where status != 'deleted')"
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

            search_sql = "select id from campaignRelations where campaignId='%s' and campaignName='%s'"%(campaignId,campaignName)
            cursor.execute(search_sql)
            exists = cursor.fetchone()
            if exists:
                campaign_name = campaignName.split('_')
                for c in campaign_name:
                    if "66" in c:
                        update_sql = "update campaignRelations set optName='%s',campaignName='%s' where campaignId='%s'" % (c,campaignName,campaignId)
                        cursor.execute(update_sql)
                        db.commit()
            else:
                campaign_name = campaignName.split('_')
                for c in campaign_name:
                    if "66" in c:
                        insert_sql = "insert into campaignRelations(campaignId,campaignName,account_id,optName) values('%s','%s','%s','%s')" % (campaignId,campaignName,account,c)
                        cursor.execute(insert_sql)
                        db.commit()
    except Exception:
        pass

if (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime('%H:%M') >= "07:29":
    mail_body = "facebook campaign name finished"
    mail_from = "ads_reporting@newborntown.com"
    mail_to = "liyin@newborntown.com"
    msg = MIMEMultipart()
    body = MIMEText(mail_body)
    msg.attach(body)
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['date'] = time.strftime('%Y-%m-%d')
    msg['Subject'] = "get facebook camapaign name finished"
    smtp = smtplib.SMTP()
    smtp.connect('smtp.exmail.qq.com', 25)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login('ads_reporting@newborntown.com', '5igmKD3F0cLScrS5')
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    smtp.quit()