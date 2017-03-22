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

time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
# time_now = datetime.datetime.now()
start_date = (datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=720)
time_now = datetime.datetime.strftime(time_now, '%Y-%m-%d')
start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()
sql = "select offer_id,facebook_keywords from advertisers where type='facebook' and offer_id in (select id from offer where status != 'deleted')"
# sql = "select offer_id,facebook_keywords from advertisers where type='facebook' and offer_id=19"
cursor.execute(sql)
results = cursor.fetchall()

sql_token = "select accessToken from token where account='rongchangzhang@gmail.com'"
cursor.execute(sql_token)
token_result = cursor.fetchone()
accessToken = token_result[0]
updateTime = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
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
    #获取offer投放的时间
    sql_offer = "select startTime,endTime,contract_type,contract_scale,price from platformOffer where offer_id='%d' and platform='facebook'" % offerId
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
                j["campaignId"] = campaignId
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
                j["campaignId"] = campaignId
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
                j["campaignId"] = campaignId
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
                    "conversions": conversions,
                    "campaignId": campaignId
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
                j["campaignId"] = campaignId
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
                    "date_start": j["date_start"],
                    "campaignId": campaignId
                }
                cpc_list += [data_cpc]

        for l in range(len(impressions_list)):
            country_fb = impressions_list[l].get("country")
            date_fb = impressions_list[l].get("date_start")
            revenue_fb = float('%0.2f'%(float(revenue_list[l].get("revenue"))))
            cost_fb = float('%0.2f'%(float(cost_list[l].get("spend"))))
            profit_fb = float(rebate_fb-cost_fb)
            impressions_fb = impressions_list[l].get("impressions")
            clicks_fb = clicks_list[l].get("clicks")
            conversions_fb = conversions_list[l].get("conversions")
            ctr_fb = ctr_list[l].get("ctr")
            cvr_fb = float('%0.2f'%(float(conversions_fb)/float(clicks_fb)*100) if float(clicks_fb) != 0 else 0)
            cpc_fb = float(cpc_list[l].get("cpc"))
            cpi_fb = float('%0.2f'%(cost_fb/float(conversions_fb)) if float(conversions_fb) !=0 else 0)
            campaignId = impressions_list[l].get("campaignId")

            account_sql = "select account_id,optName from campaignRelations where campaignId='%s'" % campaignId
            cursor.execute(account_sql)
            account_result = cursor.fetchone()
            accountId = account_result[0]
            optName = account_result[1]
            print optName
            rebate_sql = "select scale from rebate where accountId='%s'" % (accountId)
            cursor.execute(rebate_sql)
            rebate_result = cursor.fetchone()
            if rebate_result:
                rebate_fb = float('%0.2f' % (float(cost_fb) * float(rebate_result[0]) / 100))
            else:
                rebate_fb = 0

            datadetail_sql = "select id from dataDetail where offer_id='%d' and country='%s' and date='%s' and campaignId='%s' and type='facebook'" % (offerId, country_fb, date_fb, campaignId)
            cursor.execute(datadetail_sql)
            datadetail_result = cursor.fetchone()
            if datadetail_result:
                update_sql = "update dataDetail set revenue=%s,profit=%s,cost=%s,impressions=%s,clicks=%s,conversions=%s,ctr=%s,cvr=%s,cpc=%s,cpi=%s,rebate=%s,optName=%s,updateTime=%s where id=%s"
                cursor.execute(update_sql, (revenue_fb, profit_fb, cost_fb, impressions_fb, clicks_fb, conversions_fb, ctr_fb, cvr_fb, cpc_fb, cpi_fb, rebate_fb, optName, updateTime,datadetail_result[0]))
                db.commit()
            else:
                insert_sql = "insert into dataDetail(offer_id,account_id,campaignId,type,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi,date,country,rebate,optName,updateTime) values('%d','%s','%s','%s','%f','%f','%f','%d','%d','%d','%f','%f','%f','%f','%s','%s','%f','%s','%s')" % (offerId, accountId, campaignId, 'facebook', revenue_fb, profit_fb, cost_fb, impressions_fb, clicks_fb, conversions_fb, ctr_fb, cvr_fb,
                cpc_fb, cpi_fb, date_fb, country_fb, rebate_fb, optName, updateTime)
                cursor.execute(insert_sql)
                db.commit()

# if (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime('%H:%M') >= "18:00":
#     mail_body = "facebook data finished"
#     mail_from = "ads_reporting@newborntown.com"
#     mail_to = "liyin@newborntown.com"
#     msg = MIMEMultipart()
#     body = MIMEText(mail_body)
#     msg.attach(body)
#     msg['From'] = mail_from
#     msg['To'] = mail_to
#     msg['date'] = time.strftime('%Y-%m-%d')
#     msg['Subject'] = "get facebook Data finished"
#     smtp = smtplib.SMTP()
#     smtp.connect('smtp.exmail.qq.com', 25)
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.ehlo()
#     smtp.login('ads_reporting@newborntown.com', '5igmKD3F0cLScrS5')
#     smtp.sendmail(mail_from, mail_to, msg.as_string())
#     smtp.quit()
print "ok"