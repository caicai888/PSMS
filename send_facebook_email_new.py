#!/usr/bin/env python
#coding: utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import xlwt
import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import datetime,time
import base64

time_now = datetime.datetime.now()+datetime.timedelta(hours=8)
time_now=time_now.strftime('%H:%M')
time_now = "18:00"
db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()
# sql = "select id,email_users,app_name,email_template from offer where email_time='%s' and status != 'deleted'"%(time_now)
appName_sql = "select app_name from offer where email_time='%s' and status != 'deleted'"%(time_now)
cursor.execute(appName_sql)
appName_results = cursor.fetchall()
app_names = []
for i in appName_results:
    app_names.append(i[0])

app_names = list(set(app_names))

# startTime = ((datetime.datetime.now()+datetime.timedelta(hours=8))-datetime.timedelta(hours=120)).strftime("%Y-%m-%d")
# today = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
startTime = "2017-03-19"
today = "2017-03-23"
date1 = datetime.datetime.strptime(startTime, '%Y-%m-%d')
date2 = datetime.datetime.strptime(today, '%Y-%m-%d')
date_timelta = datetime.timedelta(days=1)
all_date = []
all_date.append(startTime)
while date_timelta < (date2 - date1):
    all_date.append((date1 + date_timelta).strftime("%Y-%m-%d"))
    date_timelta += datetime.timedelta(days=1)
all_date.append(today)

time_ranges = []
for day in all_date[::-1]:
    time_ranges.append("{'since': " + "'" + str(day) + "'" + ", 'until': " + "'" + str(day) + "'" + "}")

accessToken = "EAAHgEYXO0BABABt1QAdnb4kDVpgDv0RcA873EqcNbHFeN8IZANMyXZAU736VKOj1JjSdOPk2WuZC7KwJZBBD76CUbA09tyWETQpOd5OCRSctIo6fuj7cMthZCH6pZA6PZAFmrMgGZChehXreDa3caIZBkBwkyakDAGA4exqgy2sI7JwZDZD"
# try:
for j in app_names:
    sql = "select id,email_users,email_template from offer where status != 'deleted' and app_name='%s'"%j
    cursor.execute(sql)
    results = cursor.fetchall()
    mail_to = []
    mail_templates = []
    for e in results:
        mail_to+=(e[1].split(','))
        mail_templates+=(e[2].split(','))
    mail_to = list(set(mail_to))
    email_templates = list(set(mail_templates))
    all_data = []
    revenue_count = 0
    profit_count = 0
    cost_count = 0
    impressions_count = 0
    clicks_count = 0
    conversions_count = 0
    ctr_count = 0
    cvr_count = 0
    cpc_count = 0
    cpi_count = 0
    all_data_result = 0
    for i in results:
        offerId = i[0]
        fb_ap_sql = "select id from datas where date='%s' and offer_id='%d'" %(startTime,offerId)
        cursor.execute(fb_ap_sql)
        fb_ap_result = cursor.fetchone()
        ad_sql = "select id from adwords where date='%s' and offer_id='%d'" %(startTime,offerId)
        cursor.execute(ad_sql)
        ad_result = cursor.fetchone()
        if not fb_ap_result and not ad_result:
            all_data_result = 1
    if all_data_result == 1:
        pass
    else:
        for i in results:
            offerId = i[0]
            if u'全部维度' in email_templates:
                fb_data_sql = "select date,type,country,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi from datas where date>='%s' and date <= '%s' and type='facebook' and offer_id='%d' order by date ASC" % (startTime, today, offerId)
                cursor.execute(fb_data_sql)
                fb_data_result = cursor.fetchall()
                all_data += fb_data_result
                ap_data_sql = "select date,type,country,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi from datas where date>='%s' and date <= '%s' and type='apple' and offer_id='%d' order by date ASC"%(startTime,today,offerId)
                cursor.execute(ap_data_sql)
                ap_data_result = cursor.fetchall()
                all_data += ap_data_result
                ad_data_sql = "select date,'adwords',country,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi from datas where date>='%s' and date <= '%s' and offer_id='%d' order by date ASC"%(startTime,today,offerId)
                cursor.execute(ad_data_sql)
                ad_data_result = cursor.fetchall()
                all_data += ad_data_result
            elif "GEO" in email_templates:
                if "Source" in email_templates:
                    fb_data_sql = "select date,type,country,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi from datas where date>='%s' and date<='%s' and type='facebook' and offer_id='%d' group by country,date order by date ASC" % (startTime,today,offerId)
                    cursor.execute(fb_data_sql)
                    fb_data_result = cursor.fetchall()
                    for f in fb_data_result:
                        all_data += [
                            {
                                "Date": f[0],
                                "Source": f[1],
                                "GEO": f[2],
                                "Revenue": f[3],
                                "Profit": f[4],
                                "Cost": f[5],
                                "Impressions": f[6],
                                "Clicks": f[7],
                                "Conversions": f[8],
                                "Ctr": f[9],
                                "Cvr": f[10],
                                "Cpc": f[11],
                                "Cpi": f[12]
                            }
                        ]

                    ap_data_sql = "select date,type,country,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi from datas where date>='%s' and date<='%s' and type='apple' and offer_id='%d' group by country,date order by date ASC" % (startTime,today,offerId)
                    cursor.execute(ap_data_sql)
                    ap_data_result = cursor.fetchall()
                    for f in ap_data_result:
                        all_data += [
                            {
                                "Date": f[0],
                                "Source": f[1],
                                "GEO": f[2],
                                "Revenue": f[3],
                                "Profit": f[4],
                                "Cost": f[5],
                                "Impressions": f[6],
                                "Clicks": f[7],
                                "Conversions": f[8],
                                "Ctr": f[9],
                                "Cvr": f[10],
                                "Cpc": f[11],
                                "Cpi": f[12]
                            }
                        ]

                    ad_data_sql = "select date,'adwords',country,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi from adwords where date>='%s' and date<='%s' and offer_id='%d' group by country,date order by date ASC" % (startTime,today,offerId)
                    cursor.execute(ad_data_sql)
                    ad_data_result = cursor.fetchall()
                    for f in ad_data_result:
                        all_data += [
                            {
                                "Date": f[0],
                                "Source": f[1],
                                "GEO": f[2],
                                "Revenue": f[3],
                                "Profit": f[4],
                                "Cost": f[5],
                                "Impressions": f[6],
                                "Clicks": f[7],
                                "Conversions": f[8],
                                "Ctr": f[9],
                                "Cvr": f[10],
                                "Cpc": f[11],
                                "Cpi": f[12]
                            }
                        ]
                else:
                    fb_ap_sql = "select date,country,sum(revenue) revenue,sum(profit) profit,sum(cost) cost,sum(impressions) impressions,sum(clicks) clicks,sum(conversions) conversions from datas where date>='%s' and date<='%s' and offer_id='%d' group by country,date order by date ASC" % (startTime,today,offerId)
                    cursor.execute(fb_ap_sql)
                    fb_ap_result = cursor.fetchall()
                    for f in fb_ap_result:
                        all_data += [
                            {
                                "Date": f[0],
                                "GEO": f[1],
                                "Revenue": f[2],
                                "Profit": f[3],
                                "Cost": f[4],
                                "Impressions": int(f[5]),
                                "Clicks": int(f[6]),
                                "Conversions": int(f[7]),
                            }
                        ]
                    ad_sql = "select date,country,sum(revenue) revenue,sum(profit) profit,sum(cost) cost,sum(impressions) impressions,sum(clicks) clicks,sum(conversions) conversions from adwords where date>='%s' and date<='%s' and offer_id='%d' group by country,date order by date ASC" % (startTime,today,offerId)
                    cursor.execute(ad_sql)
                    ad_result = cursor.fetchall()
                    for f in ad_result:
                        all_data += [
                            {
                                "Date": f[0],
                                "GEO": f[1],
                                "Revenue": f[2],
                                "Profit": f[3],
                                "Cost": f[4],
                                "Impressions": int(f[5]),
                                "Clicks": int(f[6]),
                                "Conversions": int(f[7]),
                            }
                        ]
                    tempList = []
                    all_data_list_unique = []
                    for ele in all_data:
                        key = ele['Date'] + ele['GEO']
                        if key in tempList:
                            for x in all_data_list_unique:
                                if x['Date'] == ele['Date'] and x['GEO'] == ele['GEO']:
                                    x['Revenue'] += float('%0.2f' % (float(ele['Revenue'])))
                                    x['Cost'] += float('%0.2f' % (float(ele['Cost'])))
                                    x['Profit'] += float('%0.2f' % (float(ele['Profit'])))
                                    x['Impressions'] += int(ele['Revenue'])
                                    x['Clicks'] += int(ele['Clicks'])
                                    x['Conversions'] += int(ele['Conversions'])
                        else:
                            ele['Revenue'] = float('%0.2f' % (float(ele['Revenue'])))
                            ele['Cost'] = float('%0.2f' % (float(ele['Cost'])))
                            ele['Profit'] = float('%0.2f' % (float(ele['Profit'])))
                            ele['Impressions'] = int(ele['Impressions'])
                            ele['Clicks'] = int(ele['Clicks'])
                            ele['Conversions'] = int(ele['Conversions'])

                            tempList.append(key)
                            all_data_list_unique.append(ele)
                    all_data = all_data_list_unique
                    for q in all_data:
                        cvr = 0
                        cpc = 0
                        ctr = 0
                        cpi = 0
                        if float(q["Clicks"]) != 0:
                            cvr = float(q['Conversions'])/float(q['Clicks']) * 100
                            cpc = float(q['Cost'])/float(q['Clicks'])
                        if float(q['Conversions']) != 0 :
                            cpi = float(q['Cost'])/float(q['Conversions'])
                        if float(q['Impressions']) != 0:
                            ctr = float(q['Clicks'])/float(q['Impressions']) * 100
                        q['Cvr'] = cvr
                        q['Cpc'] = cpc
                        q['Cpi'] = cpi
                        q['Ctr'] = ctr
            elif "Source" in email_templates:
                fb_data_sql = "select date,type,sum(revenue) revenue,sum(profit) profit,sum(cost) cost,sum(impressions) impressions,sum(clicks) clicks,sum(conversions) conversions,sum(cost)/sum(conversions) cpi,sum(conversions)/sum(clicks)*100 cvr, sum(cost)/sum(clicks) cpc,sum(clicks)/sum(impressions)*100 ctr from datas where date>='%s' and date <= '%s' and type='facebook' and offer_id='%d' group by date order by date ASC"%(startTime,today,offerId)
                cursor.execute(fb_data_sql)
                fb_data_result = cursor.fetchall()
                for f in fb_data_result:
                    all_data += [
                        {
                            "Date": f[0],
                            "Resource": f[1],
                            "Revenue": f[2],
                            "Profit": f[3],
                            "Cost": f[4],
                            "Impressions": f[5],
                            "Clicks": f[6],
                            "Conversions": f[7],
                            "Cpi": f[8],
                            "Cvr": f[9],
                            "Cpc": f[10],
                            "Ctr": f[11]
                        }
                    ]

                ap_data_sql = "select date,type,sum(revenue) revenue,sum(profit) profit,sum(cost) cost,sum(impressions) impressions,sum(clicks) clicks,sum(conversions) conversions,sum(cost)/sum(conversions) cpi,sum(conversions)/sum(clicks)*100 cvr, sum(cost)/sum(clicks) cpc,sum(clicks)/sum(impressions)*100 ctr from datas where date>='%s' and date <= '%s' and type='apple' and offer_id='%d' group by date order by date ASC"%(startTime,today,offerId)
                cursor.execute(ap_data_sql)
                ap_data_result = cursor.fetchall()
                for f in ap_data_result:
                    all_data += [
                        {
                            "Date": f[0],
                            "Source": f[1],
                            "Revenue": f[2],
                            "Profit": f[3],
                            "Cost": f[4],
                            "Impressions": f[5],
                            "Clicks": f[6],
                            "Conversions": f[7],
                            "Cpi": f[8],
                            "Cvr": f[9],
                            "Cpc": f[10],
                            "Ctr": f[11]
                        }
                    ]
                ad_data_sql = "select date,'adwords',sum(revenue) revenue,sum(profit) profit,sum(cost) cost,sum(impressions) impressions,sum(clicks) clicks,sum(conversions) conversions,sum(cost)/sum(conversions) cpi,sum(conversions)/sum(clicks)*100 cvr, sum(cost)/sum(clicks) cpc,sum(clicks)/sum(impressions)*100 ctr from adwords where date>='%s' and date <= '%s' and offer_id='%d' group by date order by date ASC" % (startTime, today, offerId)
                cursor.execute(ad_data_sql)
                ad_data_result = cursor.fetchall()
                for f in ad_data_result:
                    all_data += [
                        {
                            "Date": f[0],
                            "type": f[1],
                            "revenue": f[2],
                            "profit": f[3],
                            "cost": f[4],
                            "impressions": f[5],
                            "clicks": f[6],
                            "conversions": f[7],
                            "cpi": f[8],
                            "cvr": f[9],
                            "cpc": f[10],
                            "ctr": f[11]
                        }
                    ]

            else:
                fb_ap_sql = "select date,sum(revenue) revenue,sum(profit) profit,sum(cost) cost,sum(impressions) impressions,sum(clicks) clicks,sum(conversions) conversions from datas where date>='%s' and date <= '%s' and offer_id='%d' group by date order by date ASC"%(startTime,today,offerId)
                cursor.execute(fb_ap_sql)
                fb_ap_result = cursor.fetchall()
                for f in fb_ap_result:
                    all_data += [
                        {
                            "Date": f[0],
                            "Revenue": f[1],
                            "Profit": f[2],
                            "Cost": f[3],
                            "Impressions": f[4],
                            "Clicks": f[5],
                            "Conversions": f[6]
                        }
                    ]

                ad_sql ="select date,sum(revenue) revenue,sum(profit) profit,sum(cost) cost,sum(impressions) impressions,sum(clicks) clicks,sum(conversions) conversions from adwords where date>='%s' and date <= '%s' and offer_id='%d' group by date order by date ASC"%(startTime,today,offerId)
                cursor.execute(ad_sql)
                ad_result = cursor.fetchall()
                for f in ad_result:
                    all_data += [
                        {
                            "Date": f[0],
                            "Revenue": f[1],
                            "Profit": f[2],
                            "Cost": f[3],
                            "Impressions": f[4],
                            "Clicks": f[5],
                            "Conversions": f[6]
                        }
                    ]

                tempList = []
                all_data_list_unique = []
                for ele in all_data:
                    key = ele['Date']
                    if key in tempList:
                        for x in all_data_list_unique:
                            if x['Date'] == ele['Date']:
                                x['Revenue'] += float('%0.2f' % (float(ele['Revenue'])))
                                x['Cost'] += float('%0.2f' % (float(ele['Cost'])))
                                x['Profit'] += float('%0.2f' % (float(ele['Profit'])))
                                x['Impressions'] += int(ele['Impressions'])
                                x['Clicks'] += int(ele['Clicks'])
                                x['Conversions'] += int(ele['Conversions'])
                    else:
                        ele['Revenue'] = float('%0.2f' % (float(ele['Revenue'])))
                        ele['Cost'] = float('%0.2f' % (float(ele['Cost'])))
                        ele['Profit'] = float('%0.2f' % (float(ele['Profit'])))
                        ele['Impressions'] = int(ele['Impressions'])
                        ele['Clicks'] = int(ele['Clicks'])
                        ele['Conversions'] = int(ele['Conversions'])

                        tempList.append(key)
                        all_data_list_unique.append(ele)
                all_data = all_data_list_unique
                for q in all_data:
                    cvr = 0
                    cpc = 0
                    ctr = 0
                    cpi = 0
                    if float(q["Clicks"]) != 0:
                        cvr = float(q['Conversions']) / float(q['Clicks']) * 100
                        cpc = float(q['Cost']) / float(q['Clicks'])
                    if float(q['Conversions']) != 0:
                        cpi = float(q['Cost']) / float(q['Conversions'])
                    if float(q['Impressions']) != 0:
                        ctr = float(q['Clicks']) / float(q['Impressions']) * 100
                    q['Cvr'] = cvr
                    q['Cpc'] = cpc
                    q['Cpi'] = cpi
                    q['Ctr'] = ctr

        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet(j.encode("utf8") + u"数据详情")
        if u'全部维度' in email_templates:
            sheet.write(0, 0, "Date")
            sheet.write(0, 1, "Geo")
            sheet.write(0, 2, "source")
            sheet.write(0, 3, "Revenue")
            sheet.write(0, 4, "Profit")
            sheet.write(0, 5, "Cost")
            sheet.write(0, 6, "Impressions")
            sheet.write(0, 7, "Clicks")
            sheet.write(0, 8, "Conversions")
            sheet.write(0, 9, "CTR")
            sheet.write(0, 10, "CVR")
            sheet.write(0, 11, "CPC")
            sheet.write(0, 12, "CPI")
            count = 0

            for data in all_data:
                count += 1
                revenue_count += float('%0.2f'%float(data[3]))
                profit_count += float('%0.2f'%float(data[4]))
                cost_count += float('%0.2f'%float(data[5]))
                impressions_count += int(data[6])
                clicks_count += int(data[7])
                conversions_count += int(data[8])
                sheet.write(count, 0, data[0])
                sheet.write(count, 1, data[2])
                sheet.write(count, 2, data[1])
                sheet.write(count, 3, float('%0.2f'%float(data[3])))
                sheet.write(count, 4, float('%0.2f'%float(data[4])))
                sheet.write(count, 5, float('%0.2f'%float(data[5])))
                sheet.write(count, 6, data[6])
                sheet.write(count, 7, data[7])
                sheet.write(count, 8, data[8])
                sheet.write(count, 9, float('%0.2f'%float(data[9])))
                sheet.write(count, 10, float('%0.2f'%float(data[10])))
                sheet.write(count, 11, float('%0.2f'%float(data[11])))
                sheet.write(count, 12, float('%0.2f'%float(data[12])))
                continue

            sheet.write(count+1, 0, 'Total')
            sheet.write(count+1, 3, revenue_count)
            sheet.write(count+1, 4, profit_count)
            sheet.write(count+1, 5, cost_count)
            sheet.write(count+1, 6, impressions_count)
            sheet.write(count+1, 7, clicks_count)
            sheet.write(count+1, 8, conversions_count)
            if clicks_count !=0:
                cvr_count = conversions_count/clicks_count * 100
                cpc_count = cost_count/clicks_count
            if conversions_count != 0:
                cpi_count = cost_count/conversions_count
            if impressions_count != 0:
                ctr_count = clicks_count/impressions_count * 100
            sheet.write(count+1, 9, ctr_count)
            sheet.write(count+1, 10, cvr_count)
            sheet.write(count+1, 11, cpc_count)
            sheet.write(count+1, 12, cpi_count)

        else:
            print email_templates
            print all_data
            count = 0
            temlen = len(email_templates)
            for t in range(len(email_templates)):
                sheet.write(0, t, email_templates[t])
            sheet.write(0,temlen,"Date")
            for data in all_data:
                count += 1
                for n in range(len(email_templates)):
                    sheet.write(count,n,data[email_templates[n]])
                sheet.write(count,temlen, data['Date'])
                continue


        file_name = '=?UTF-8?B?' +base64.b64encode(j)+'?='+ "_data.xls"
        file_dir = '/home/ubuntu/code'
        wbk.save(file_name)
        mail_body="data"
        mail_from="ads_reporting@newborntown.com"
        msg = MIMEMultipart()
        body = MIMEText(mail_body)
        msg.attach(body)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file_name, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="' + file_name.encode("utf8") + '"')
        msg.attach(part)
        msg['From'] = mail_from
        msg['To'] = ';'.join(mail_to)
        msg['date'] = time.strftime('%Y-%m-%d')
        msg['Subject'] = '=?UTF-8?B?' + base64.b64encode(j) + '?='+"_report Data"
        smtp = smtplib.SMTP()
        smtp.connect('smtp.exmail.qq.com',25)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('ads_reporting@newborntown.com', '5igmKD3F0cLScrS5')
        smtp.sendmail(mail_from, mail_to, msg.as_string())
        smtp.quit()





# except Exception as e:
#     print e
