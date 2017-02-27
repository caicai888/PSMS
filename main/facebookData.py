# -*- coding: utf-8 -*-
from __future__ import division
from flask import Blueprint, request
from models import Advertisers, Datas, Adwords
import json
import datetime
import re

facebookDate = Blueprint('facebookDate', __name__)

@facebookDate.route('/api/dashboard')
def dashboard():
    yesterday = (datetime.datetime.now()-datetime.timedelta(hours=16)).strftime("%Y-%m-%d")
    apple_datas = Datas.query.filter_by(type="apple",date=yesterday).all()
    revenue_apple = 0
    profit_apple = 0
    cost_apple = 0
    impressions_apple = 0
    clicks_apple = 0
    conversions_apple = 0
    ctr_apple = 0
    cvr_apple = 0
    cpc_apple = 0
    cpi_apple = 0
    for j in apple_datas:
        revenue_apple += float(j.revenue)
        profit_apple += float(j.profit)
        cost_apple += float(j.cost)
        impressions_apple += int(j.impressions)
        clicks_apple += int(j.clicks)
        conversions_apple += int(j.conversions)
    if conversions_apple != 0:
        cpi_apple = '%0.2f' % (cost_apple / float(conversions_apple))

    if clicks_apple != 0:
        cvr_apple = '%0.2f' % (float(conversions_apple) / float(clicks_apple) * 100)

    if clicks_apple != 0:
        cpc_apple = '%0.2f' % (float(cost_apple) / float(clicks_apple))

    if impressions_apple != 0:
        ctr_apple = '%0.2f' % (clicks_apple / impressions_apple * 100)

    facebook_datas = Datas.query.filter_by(type="facebook",date=yesterday).all()
    revenue = 0
    profit = 0
    cost = 0
    impressions = 0
    clicks = 0
    conversions = 0
    ctr = 0
    cvr = 0
    cpc = 0
    cpi = 0
    for i in facebook_datas:
        revenue += float(i.revenue)
        profit += float(i.profit)
        cost += float(i.cost)
        impressions += int(i.impressions)
        clicks += int(i.clicks)
        conversions += int(i.conversions)

    if conversions != 0:
        cpi = '%0.2f' % (cost / float(conversions))

    if clicks != 0:
        cvr = '%0.2f' % (float(conversions) / float(clicks) * 100)

    if clicks != 0:
        cpc = '%0.2f' % (float(cost) / float(clicks))

    if impressions != 0:
        ctr = '%0.2f' % (clicks / impressions * 100)

    adwords_datas = Adwords.query.filter_by(date=yesterday).all()
    revenue_adwords = 0
    profit_adwords = 0
    cost_adwords = 0
    impressions_adwords = 0
    clicks_adwords = 0
    conversions_adwords = 0
    ctr_adwords = 0
    cvr_adwords = 0
    cpc_adwords = 0
    cpi_adwords = 0
    for ad in adwords_datas:
        revenue_adwords += float(ad.revenue)
        profit_adwords += float(ad.profit)
        cost_adwords += float(ad.cost)
        impressions_adwords += int(ad.impressions)
        clicks_adwords += int(ad.clicks)
        conversions_adwords += float(ad.conversions)
    if conversions_adwords != 0:
        cpi_adwords = '%0.2f' % (cost_adwords / conversions_adwords)

    if clicks_adwords != 0:
        cvr_adwords = '%0.2f' % (conversions_adwords / float(clicks_adwords) * 100)

    if clicks_adwords != 0:
        cpc_adwords = '%0.2f' % (float(cost_adwords) / float(clicks_adwords))

    if impressions_adwords != 0:
        ctr_adwords = '%0.2f' % (clicks_adwords / impressions_adwords * 100)

    result = {
        "impressions": str(impressions),
        "spend": '%0.2f'%(cost),
        "clicks": str(clicks),
        "conversions": str(conversions),
        "cpc": str(cpc),
        "ctr": str(ctr),
        "cpi": str(cpi),
        "cvr": str(cvr),
        "revenue": '%0.2f'%(revenue),
        "profit": '%0.2f'%(profit),
        "impressions_apple": str(impressions_apple),
        "spend_apple": '%0.2f'%(cost_apple),
        "clicks_apple": str(clicks_apple),
        "conversions_apple": str(conversions_apple),
        "cpc_apple": str(cpc_apple),
        "ctr_apple": str(ctr_apple),
        "cpi_apple": str(cpi_apple),
        "cvr_apple": str(cvr_apple),
        "revenue_apple": '%0.2f'%(revenue_apple),
        "profit_apple": '%0.2f'%(profit_apple),
        "impressions_adwords": str(impressions_adwords),
        "spend_adwords": '%0.2f' % (cost_adwords),
        "clicks_adwords": str(clicks_adwords),
        "conversions_adwords": str(conversions_adwords),
        "cpc_adwords": str(cpc_adwords),
        "ctr_adwords": str(ctr_adwords),
        "cpi_adwords": str(cpi_adwords),
        "cvr_adwords": str(cvr_adwords),
        "revenue_adwords": '%0.2f' % (revenue_adwords),
        "profit_adwords": '%0.2f' % (profit_adwords)
    }
    response = {
        "code": 200,
        "message": "success",
        "result": result
    }
    return json.dumps(response)

#所有值的总数
def data_count(impressions_list,cost_list,clicks_list,conversions_list,revenue_list,profit_list):
    count_impressions = 0
    count_cost = 0
    count_clicks = 0
    count_conversions = 0
    count_ctr = 0
    count_cvr = 0
    count_cpc = 0
    count_cpi = 0
    count_revenue = 0
    count_profit = 0
    for i in impressions_list:
        count_impressions += i["impressions"]
    for i in cost_list:
        count_cost += float(i["spend"])
    for i in clicks_list:
        count_clicks += i["clicks"]
    for i in conversions_list:
        count_conversions += float(i["conversions"])
    for i in revenue_list:
        count_revenue += float(i["revenue"])
    for i in profit_list:
        count_profit += float(i["profit"])
    if count_impressions != 0:
        count_ctr = '%0.2f' % (count_clicks / count_impressions * 100)
    if count_clicks != 0:
        count_cvr = '%0.2f' % (float(count_conversions) / float(count_clicks) * 100)
    if count_clicks != 0:
        count_cpc = '%0.2f' % (float(count_cost) / float(count_clicks))
    if count_conversions != 0:
        count_cpi = '%0.2f' % (count_cost / float(count_conversions))

    data_geo = {
        "count_impressions": str(count_impressions),
        "count_cost": '%0.2f' % (count_cost),
        "count_clicks": str(count_clicks),
        "count_conversions": str(count_conversions),
        "count_ctr": count_ctr,
        "count_cvr": count_cvr,
        "count_cpc": count_cpc,
        "count_cpi": count_cpi,
        "revenue": '%0.2f' % (count_revenue),
        "profit": '%0.2f' % (count_profit)
    }
    return data_geo
#折线图的数据显示
def data_range(impressions_list,cost_list,clicks_list,conversions_list,ctr_list,cvr_list,cpc_list,cpi_list,revenue_list,profit_list):
    impressions_range = []
    date_range = []
    dx = dict()
    for i in impressions_list:
        dx.setdefault(i["date_start"], []).append(i["impressions"])
    for k in dx:
        dx[k] = sum(float(i) for i in dx[k])
    impressions_list_range = [{"date_start": k, "impressions": str(v)} for k, v in dx.items()]
    impressions_list_range = sorted(impressions_list_range, key=lambda k: k['date_start'])
    for i in impressions_list_range:
        impressions_range.append(i["impressions"])
        date_range.append(i["date_start"])

    cost_range = []
    dx = dict()
    for i in cost_list:
        dx.setdefault(i["date_start"], []).append(i["spend"])
    for k in dx:
        dx[k] = sum(float(i) for i in dx[k])
    cost_list_range = [{"date_start": k, "spend": str(v)} for k, v in dx.items()]
    cost_list_range = sorted(cost_list_range, key=lambda k: k['date_start'])
    for i in cost_list_range:
        cost_range.append(i["spend"])

    clicks_range = []
    dx = dict()
    for i in clicks_list:
        dx.setdefault(i["date_start"], []).append(i["clicks"])
    for k in dx:
        dx[k] = sum(float(i) for i in dx[k])
    clicks_list_range = [{"date_start": k, "clicks": str(v)} for k, v in dx.items()]
    clicks_list_range = sorted(clicks_list_range, key=lambda k: k['date_start'])
    for i in clicks_list_range:
        clicks_range.append(i["clicks"])

    conversions_range = []
    dx = dict()
    for i in conversions_list:
        dx.setdefault(i["date_start"], []).append(i["conversions"])
    for k in dx:
        dx[k] = sum(float(i) for i in dx[k])
    conversions_list_range = [{"date_start": k, "conversions": str(v)} for k, v in dx.items()]
    conversions_list_range = sorted(conversions_list_range, key=lambda k: k['date_start'])
    for i in conversions_list_range:
        conversions_range.append(i["conversions"])

    ctr_range = []
    dx = dict()
    for i in ctr_list:
        dx.setdefault(i["date_start"], []).append(i["ctr"])
    for k in dx:
        dx[k] = sum(float(i) for i in dx[k])
    ctr_list_range = [{"date_start": k, "ctr": str(v)} for k, v in dx.items()]
    ctr_list_range = sorted(ctr_list_range, key=lambda k: k['date_start'])
    for i in ctr_list_range:
        ctr_range.append('%0.2f' % (float(i["ctr"])))

    cvr_range = []
    dx = dict()
    for i in cvr_list:
        dx.setdefault(i["date_start"], []).append(i["cvr"])
    for k in dx:
        dx[k] = sum(float(i) for i in dx[k])
    cvr_list_range = [{"date_start": k, "cvr": str(v)} for k, v in dx.items()]
    cvr_list_range = sorted(cvr_list_range, key=lambda k: k['date_start'])
    for i in cvr_list_range:
        cvr_range.append(i["cvr"])

    cpc_range = []
    dx = dict()
    for i in cpc_list:
        dx.setdefault(i["date_start"], []).append(i["cpc"])
    for k in dx:
        dx[k] = sum(float(i) for i in dx[k])
    cpc_list_range = [{"date_start": k, "cpc": str(v)} for k, v in dx.items()]
    cpc_list_range = sorted(cpc_list_range, key=lambda k: k['date_start'])
    for i in cpc_list_range:
        cpc_range.append('%0.2f' % (float(i["cpc"])))

    cpi_range = []
    dx = dict()
    for i in cpi_list:
        dx.setdefault(i["date_start"], []).append(i["cpi"])
    for k in dx:
        dx[k] = sum(float(i) for i in dx[k])
    cpi_list_range = [{"date_start": k, "cpi": str(v)} for k, v in dx.items()]
    cpi_list_range = sorted(cpi_list_range, key=lambda k: k['date_start'])
    for i in cpi_list_range:
        cpi_range.append(i["cpi"])

    revenue_range = []
    dx = dict()
    for i in revenue_list:
        dx.setdefault(i["date_start"], []).append(i["revenue"])
    for k in dx:
        dx[k] = sum(float(i) for i in dx[k])
    revenue_list_range = [{"date_start": k, "revenue": str(v)} for k, v in dx.items()]
    revenue_list_range = sorted(revenue_list_range, key=lambda k: k['date_start'])
    for i in revenue_list_range:
        revenue_range.append(i["revenue"])

    profit_range = []
    dx = dict()
    for i in profit_list:
        dx.setdefault(i["date_start"], []).append(i["profit"])
    for k in dx:
        dx[k] = sum(float(i) for i in dx[k])
    profit_list_range = [{"date_start": k, "profit": str(v)} for k, v in dx.items()]
    profit_list_range = sorted(profit_list_range, key=lambda k: k['date_start'])
    for i in profit_list_range:
        profit_range.append(i["profit"])

    data_range_result = {
        "date": date_range,
        "revenue": revenue_range,
        "impressions": impressions_range,
        "costs": cost_range,
        "clicks": clicks_range,
        "conversions": conversions_range,
        "ctr": ctr_range,
        "cvr": cvr_range,
        "cpc": cpc_range,
        "cpi": cpi_range,
        "profit": profit_range
    }
    return data_range_result

def unique_list(impressions_list,cost_list,clicks_list,conversions_list,ctr_list,cvr_list,cpc_list,cpi_list,revenue_list,profit_list):
    tempList = []
    impressions_list_unique = []
    for ele in impressions_list:
        key = ele['date_start'] + ele['country']
        if key in tempList:
            for x in impressions_list_unique:
                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                    x['impressions'] += int(ele['impressions'])
        else:
            ele['impressions'] = int(ele['impressions'])
            tempList.append(key)
            impressions_list_unique.append(ele)

    tempList = []
    cost_list_unique = []
    for ele in cost_list:
        key = ele['date_start'] + ele['country']
        if key in tempList:
            for x in cost_list_unique:
                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                    x['spend'] += float(ele['spend'])
        else:
            ele['spend'] = float(ele['spend'])
            tempList.append(key)
            cost_list_unique.append(ele)

    tempList = []
    clicks_list_unique = []
    for ele in clicks_list:
        key = ele['date_start'] + ele['country']
        if key in tempList:
            for x in clicks_list_unique:
                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                    x['clicks'] += float(ele['clicks'])
        else:
            ele['clicks'] = float(ele['clicks'])
            tempList.append(key)
            clicks_list_unique.append(ele)

    tempList = []
    conversions_list_unique = []
    for ele in conversions_list:
        key = ele['date_start'] + ele['country']
        if key in tempList:
            for x in conversions_list_unique:
                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                    x['conversions'] += int(ele['conversions'])
        else:
            ele['conversions'] = int(ele['conversions'])
            tempList.append(key)
            conversions_list_unique.append(ele)

    tempList = []
    ctr_list_unique = []
    for ele in ctr_list:
        key = ele['date_start'] + ele['country']
        if key in tempList:
            for x in ctr_list_unique:
                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                    x['ctr'] += float(ele['ctr'])
        else:
            ele['ctr'] = float(ele['ctr'])
            tempList.append(key)
            ctr_list_unique.append(ele)

    tempList = []
    cpc_list_unique = []
    for ele in cpc_list:
        key = ele['date_start'] + ele['country']
        if key in tempList:
            for x in cpc_list_unique:
                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                    x['cpc'] += float(ele['cpc'])
        else:
            ele['cpc'] = float(ele['cpc'])
            tempList.append(key)
            cpc_list_unique.append(ele)

    tempList = []
    cvr_list_unique = []
    for ele in cvr_list:
        key = ele['date_start'] + ele['country']
        if key in tempList:
            for x in cvr_list_unique:
                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                    x['cvr'] += float(ele['cvr'])
        else:
            ele['cvr'] = float(ele['cvr'])
            tempList.append(key)
            cvr_list_unique.append(ele)

    tempList = []
    cpi_list_unique = []
    for ele in cpi_list:
        key = ele['date_start'] + ele['country']
        if key in tempList:
            for x in cpi_list_unique:
                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                    x['cpi'] += float(ele['cpi'])
        else:
            ele['cpi'] = float(ele['cpi'])
            tempList.append(key)
            cpi_list_unique.append(ele)

    tempList = []
    profit_list_unique = []
    for ele in profit_list:
        key = ele['date_start'] + ele['country']
        if key in tempList:
            for x in profit_list_unique:
                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                    x['profit'] += float(ele['profit'])
        else:
            ele['profit'] = float(ele['profit'])
            tempList.append(key)
            profit_list_unique.append(ele)

    tempList = []
    revenue_list_unique = []
    for ele in revenue_list:
        key = ele['date_start'] + ele['country']
        if key in tempList:
            for x in revenue_list_unique:
                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                    x['revenue'] += float(ele['revenue'])
        else:
            ele['revenue'] = float(ele['revenue'])
            tempList.append(key)
            revenue_list_unique.append(ele)

    return impressions_list_unique,cost_list_unique,clicks_list_unique,conversions_list_unique,ctr_list_unique,cvr_list_unique,cpc_list_unique,cpi_list_unique,revenue_list_unique,profit_list_unique

@facebookDate.route('/api/report', methods=["POST","GET"])
def faceReport():
    if request.method == "POST":
        data = request.get_json(force=True)
        offerId = int(data['offer_id'])
        start_date = data["start_date"]
        end_date = data["end_date"]
        dimension = data["dimension"]
        advertiser = Advertisers.query.filter_by(offer_id=int(offerId)).first()
        if not advertiser:
            return json.dumps({
                "code":500,
                "message":"not bind ads",
                "data_geo": {},
                "data_geo_table": {},
                "data_date_table": {},
                "data_range": {},
            })
        impressions_list = []
        cost_list = []
        clicks_list = []
        conversions_list = []
        ctr_list = []
        cvr_list = []
        cpc_list = []
        cpi_list = []
        revenue_list = []
        profit_list = []
        if "geo" in dimension:
            try:
                if "source" in dimension:
                    adwords_results = Adwords.query.filter(Adwords.offer_id==offerId,Adwords.date>=start_date,Adwords.date<=end_date).order_by(Adwords.date.desc()).all()
                    facebook_results = Datas.query.filter(Datas.offer_id==offerId,Datas.date >= start_date, Datas.date<=end_date,Datas.type=="facebook").order_by(Datas.date.desc()).all()
                    apple_results = Datas.query.filter(Datas.offer_id == offerId, Datas.date >= start_date, Datas.date <= end_date,
                                                          Datas.type == "apple").order_by(Datas.date.desc()).all()
                    ## adwords
                    impressions_list_ad = []
                    cost_list_ad = []
                    clicks_list_ad = []
                    conversions_list_ad = []
                    ctr_list_ad = []
                    cvr_list_ad = []
                    cpc_list_ad = []
                    cpi_list_ad = []
                    revenue_list_ad = []
                    profit_list_ad = []
                    for i in adwords_results:
                        date = i.date
                        if i.is_UAC == 1:
                            country = re.findall(r'\[(.*)\]', i.campaignName)[0]
                        else:
                            country = i.country
                        impressions_list_ad += [
                            {
                                "impressions": int(i.impressions),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]
                        cost_list_ad += [
                            {
                                "spend": '%0.2f' % (float(i.cost)),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]
                        clicks_list_ad += [
                            {
                                "clicks": int(i.clicks),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]
                        conversions_list_ad += [
                            {
                                "conversions": float(i.conversions),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]
                        ctr_list_ad += [
                            {
                                "ctr": '%0.2f' % (float(i.ctr)),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]
                        cvr_list_ad += [
                            {
                                "cvr": '%0.2f' % (float(i.cvr)),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]
                        cpc_list_ad += [
                            {
                                "cpc": '%0.2f' % (float(i.cpc)),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]
                        cpi_list_ad += [
                            {
                                "cpi": '%0.2f' % (float(i.cpi)),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]
                        revenue_list_ad += [
                            {
                                "revenue": '%0.2f' % (float(i.revenue)),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]
                        profit_list_ad += [
                            {
                                "profit": '%0.2f' % (float(i.profit)),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]

                    adwords_results_unique = unique_list(impressions_list_ad,cost_list_ad,clicks_list_ad,conversions_list_ad,ctr_list_ad,cvr_list_ad,cpc_list_ad,cpi_list_ad,revenue_list_ad,profit_list_ad)
                    print "++++"*10
                    print adwords_results_unique

                    ## facebook
                    for i in facebook_results:
                        date = i.date
                        country = i.country
                        impressions_list += [
                            {
                                "impressions": int(i.impressions),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        cost_list += [
                            {
                                "spend": '%0.2f' % (float(i.cost)),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        clicks_list += [
                            {
                                "clicks": int(i.clicks),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        conversions_list += [
                            {
                                "conversions": float(i.conversions),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        ctr_list += [
                            {
                                "ctr": '%0.2f' % (float(i.ctr)),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        cvr_list += [
                            {
                                "cvr": '%0.2f' % (float(i.cvr)),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        cpc_list += [
                            {
                                "cpc": '%0.2f' % (float(i.cpc)),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        cpi_list += [
                            {
                                "cpi": '%0.2f' % (float(i.cpi)),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        revenue_list += [
                            {
                                "revenue": '%0.2f' % (float(i.revenue)),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        profit_list += [
                            {
                                "profit": '%0.2f' % (float(i.profit)),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]

                    ## apple
                    for i in apple_results:
                        date = i.date
                        country = i.country
                        impressions_list += [
                            {
                                "impressions": int(i.impressions),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        cost_list += [
                            {
                                "spend": '%0.2f' % (float(i.cost)),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        clicks_list += [
                            {
                                "clicks": int(i.clicks),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        conversions_list += [
                            {
                                "conversions": float(i.conversions),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        ctr_list += [
                            {
                                "ctr": '%0.2f' % (float(i.ctr)),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        cvr_list += [
                            {
                                "cvr": '%0.2f' % (float(i.cvr)),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        cpc_list += [
                            {
                                "cpc": '%0.2f' % (float(i.cpc)),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        cpi_list += [
                            {
                                "cpi": '%0.2f' % (float(i.cpi)),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        revenue_list += [
                            {
                                "revenue": '%0.2f' % (float(i.revenue)),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        profit_list += [
                            {
                                "profit": '%0.2f' % (float(i.profit)),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]



                    data_geo_table = {
                        "impressions_list": impressions_list,
                        "cost_list": cost_list,
                        "clicks_list": clicks_list,
                        "conversions_list": conversions_list,
                        "ctr_list": ctr_list,
                        "cvr_list": cvr_list,
                        "cpc_list": cpc_list,
                        "cpi_list": cpi_list,
                        "revenue_list": revenue_list,
                        "profit_list": profit_list,
                        "head": ["Date", "Geo","source", "Revenue", "Profit", "Cost", "Impressions", "Clicks", "Conversions", "CTR", "CVR", "CPC", "CPI"]
                    }
                    data_range_result = data_range(impressions_list, cost_list, clicks_list, conversions_list, ctr_list, cvr_list, cpc_list, cpi_list,revenue_list, profit_list)
                    data_geo = data_count(impressions_list, cost_list, clicks_list, conversions_list, revenue_list, profit_list)
                    return json.dumps({
                        "code": 200,
                        "data_geo": data_geo,
                        "data_geo_table": data_geo_table,
                        "data_date_table": {},
                        "data_range": data_range_result,
                        "message": "success"
                    })
                    return json.dumps(geo_datas)
                else:
                    adwords_results = Adwords.query.filter(Adwords.offer_id==offerId,Adwords.date >= start_date, Adwords.date<=end_date).order_by(Adwords.date.desc()).all()
                    data_results = Datas.query.filter(Datas.offer_id==offerId,Datas.date >= start_date, Datas.date<=end_date).order_by(Datas.date.desc()).all()
                    for i in adwords_results:
                        date = i.date
                        if i.is_UAC == 1:
                            country = re.findall(r'\[(.*)\]', i.campaignName)[0]
                        else:
                            country = i.country
                        impressions_list += [
                            {
                                "impressions": int(i.impressions),
                                "country": country,
                                "date_start": date
                            }
                        ]
                        cost_list += [
                            {
                                "spend": '%0.2f' % (float(i.cost)),
                                "country": country,
                                "date_start": date
                            }
                        ]
                        clicks_list += [
                            {
                                "clicks": int(i.clicks),
                                "country": country,
                                "date_start": date
                            }
                        ]
                        conversions_list += [
                            {
                                "conversions": float(i.conversions),
                                "country": country,
                                "date_start": date
                            }
                        ]
                        ctr_list += [
                            {
                                "ctr": '%0.2f' % (float(i.ctr)),
                                "country": country,
                                "date_start": date
                            }
                        ]
                        cvr_list += [
                            {
                                "cvr": '%0.2f' % (float(i.cvr)),
                                "country": country,
                                "date_start": date
                            }
                        ]
                        cpc_list += [
                            {
                                "cpc": '%0.2f' % (float(i.cpc)),
                                "country": country,
                                "date_start": date
                            }
                        ]
                        cpi_list += [
                            {
                                "cpi": '%0.2f' % (float(i.cpi)),
                                "country": country,
                                "date_start": date
                            }
                        ]
                        revenue_list += [
                            {
                                "revenue": '%0.2f' % (float(i.revenue)),
                                "country": country,
                                "date_start": date
                            }
                        ]
                        profit_list += [
                            {
                                "profit": '%0.2f' % (float(i.profit)),
                                "country": country,
                                "date_start": date
                            }
                        ]
                    for i in data_results:
                        country = i.country
                        date = i.date
                        impressions_list += [
                            {
                                "impressions": int(i.impressions),
                                "country": country,
                                "date_start": date,
                                "date_stop": date
                            }
                        ]
                        cost_list += [
                            {
                                "spend": '%0.2f'%(float(i.cost)),
                                "country": country,
                                "date_start": date,
                                "date_stop": date
                            }
                        ]
                        clicks_list += [
                            {
                                "clicks": int(i.clicks),
                                "country": country,
                                "date_start": date,
                                "date_stop": date
                            }
                        ]
                        conversions_list += [
                            {
                                "conversions": float(i.conversions),
                                "country": country,
                                "date_start": date,
                                "date_stop": date
                            }
                        ]
                        ctr_list += [
                            {
                                "ctr": '%0.2f'%(float(i.ctr)),
                                "country": country,
                                "date_start": date,
                                "date_stop": date
                            }
                        ]
                        cvr_list += [
                            {
                                "cvr": '%0.2f'%(float(i.cvr)),
                                "country": country,
                                "date_start": date,
                                "date_stop": date
                            }
                        ]
                        cpc_list += [
                            {
                                "cpc": '%0.2f'%(float(i.cpc)),
                                "country": country,
                                "date_start": date,
                                "date_stop": date
                            }
                        ]
                        cpi_list += [
                            {
                                "cpi": '%0.2f'%(float(i.cpi)),
                                "country": country,
                                "date_start": date,
                                "date_stop": date
                            }
                        ]
                        revenue_list += [
                            {
                                "revenue": '%0.2f'%(float(i.revenue)),
                                "country": country,
                                "date_start": date,
                                "date_stop": date
                            }
                        ]
                        profit_list += [
                            {
                                "profit": '%0.2f'%(float(i.profit)),
                                "country": country,
                                "date_start": date,
                                "date_stop": date
                            }
                        ]

                    tempList = []
                    impressions_list_unique = []
                    for ele in impressions_list:
                        key = ele['date_start'] + ele['country']
                        if key in tempList:
                            for x in impressions_list_unique:
                                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                                    x['impressions'] += int(ele['impressions'])
                        else:
                            ele['impressions'] = int(ele['impressions'])
                            tempList.append(key)
                            impressions_list_unique.append(ele)

                    tempList = []
                    cost_list_unique = []
                    for ele in cost_list:
                        key = ele['date_start'] + ele['country']
                        if key in tempList:
                            for x in cost_list_unique:
                                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                                    x['spend'] += float(ele['spend'])
                        else:
                            ele['spend'] = float(ele['spend'])
                            tempList.append(key)
                            cost_list_unique.append(ele)

                    tempList = []
                    clicks_list_unique = []
                    for ele in clicks_list:
                        key = ele['date_start'] + ele['country']
                        if key in tempList:
                            for x in clicks_list_unique:
                                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                                    x['clicks'] += float(ele['clicks'])
                        else:
                            ele['clicks'] = float(ele['clicks'])
                            tempList.append(key)
                            clicks_list_unique.append(ele)

                    tempList = []
                    conversions_list_unique = []
                    for ele in conversions_list:
                        key = ele['date_start'] + ele['country']
                        if key in tempList:
                            for x in conversions_list_unique:
                                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                                    x['conversions'] += int(ele['conversions'])
                        else:
                            ele['conversions'] = int(ele['conversions'])
                            tempList.append(key)
                            conversions_list_unique.append(ele)
                    ## ctr cvr cpc cpi可能有问题
                    tempList = []
                    ctr_list_unique = []
                    for ele in ctr_list:
                        key = ele['date_start'] + ele['country']
                        if key in tempList:
                            for x in ctr_list_unique:
                                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                                    x['ctr'] += float(ele['ctr'])
                        else:
                            ele['ctr'] = float(ele['ctr'])
                            tempList.append(key)
                            ctr_list_unique.append(ele)

                    tempList = []
                    cpc_list_unique = []
                    for ele in cpc_list:
                        key = ele['date_start'] + ele['country']
                        if key in tempList:
                            for x in cpc_list_unique:
                                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                                    x['cpc'] += float(ele['cpc'])
                        else:
                            ele['cpc'] = float(ele['cpc'])
                            tempList.append(key)
                            cpc_list_unique.append(ele)

                    tempList = []
                    cvr_list_unique = []
                    for ele in cvr_list:
                        key = ele['date_start'] + ele['country']
                        if key in tempList:
                            for x in cvr_list_unique:
                                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                                    x['cvr'] += float(ele['cvr'])
                        else:
                            ele['cvr'] = float(ele['cvr'])
                            tempList.append(key)
                            cvr_list_unique.append(ele)

                    tempList = []
                    cpi_list_unique = []
                    for ele in cpi_list:
                        key = ele['date_start'] + ele['country']
                        if key in tempList:
                            for x in cpi_list_unique:
                                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                                    x['cpi'] += float(ele['cpi'])
                        else:
                            ele['cpi'] = float(ele['cpi'])
                            tempList.append(key)
                            cpi_list_unique.append(ele)

                    tempList = []
                    profit_list_unique = []
                    for ele in profit_list:
                        key = ele['date_start'] + ele['country']
                        if key in tempList:
                            for x in profit_list_unique:
                                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                                    x['profit'] += float(ele['profit'])
                        else:
                            ele['profit'] = float(ele['profit'])
                            tempList.append(key)
                            profit_list_unique.append(ele)

                    tempList = []
                    revenue_list_unique = []
                    for ele in revenue_list:
                        key = ele['date_start'] + ele['country']
                        if key in tempList:
                            for x in revenue_list_unique:
                                if x['date_start'] == ele['date_start'] and x['country'] == ele['country']:
                                    x['revenue'] += float(ele['revenue'])
                        else:
                            ele['revenue'] = float(ele['revenue'])
                            tempList.append(key)
                            revenue_list_unique.append(ele)

                    data_geo_table = {
                        "impressions_list": impressions_list_unique,
                        "cost_list": cost_list_unique,
                        "clicks_list": clicks_list_unique,
                        "conversions_list": conversions_list_unique,
                        "ctr_list": ctr_list_unique,
                        "cvr_list": cvr_list_unique,
                        "cpc_list": cpc_list_unique,
                        "cpi_list": cpi_list_unique,
                        "revenue_list": revenue_list_unique,
                        "profit_list": profit_list_unique,
                        "head": ["Date", "Geo", "Revenue", "Profit", "Cost", "Impressions", "Clicks", "Conversions", "CTR", "CVR", "CPC", "CPI"]
                    }
                    data_range_result = data_range(impressions_list_unique,cost_list_unique,clicks_list_unique,conversions_list_unique,ctr_list_unique,cvr_list_unique,cpc_list_unique,cpi_list_unique,revenue_list_unique,profit_list_unique)
                    data_geo = data_count(impressions_list_unique,cost_list_unique,clicks_list_unique,conversions_list_unique,revenue_list_unique,profit_list_unique)
                    return json.dumps({
                        "code": 200,
                        "data_geo": data_geo,
                        "data_geo_table": data_geo_table,
                        "data_date_table": {},
                        "data_range": data_range_result,
                        "message": "success"
                    })
                    return json.dumps(geo_datas)
            except Exception as e:
                print e
                return json.dumps({
                    "code": 500,
                    "message": "no bind data or bind wrong data"
                })

        else:
           try:
               if "source" in dimension:
                   adwords_results = Adwords.query.filter(Adwords.offer_id == offerId,Adwords.date>=start_date,Adwords.date<=end_date).order_by(Adwords.date.desc()).all()
                   facebook_results = Datas.query.filter(Datas.offer_id==offerId,Datas.date>=start_date,Datas.date<=end_date,Datas.type=="facebook").order_by(Datas.date.desc()).all()
                   apple_results = Datas.query.filter(Datas.offer_id == offerId, Datas.date >= start_date, Datas.date <= end_date,
                                                         Datas.type == "apple").order_by(Datas.date.desc()).all()
                   ##adwords
                   impressions_list_all_adwords = []
                   cost_list_all_adwords = []
                   clicks_list_all_adwords = []
                   conversions_list_all_adwords = []
                   ctr_list_all_adwords = []
                   cvr_list_all_adwords = []
                   cpc_list_all_adwords = []
                   cpi_list_all_adwords = []
                   revenue_list_all_adwords = []
                   profit_list_all_adwords = []
                   for i in adwords_results:
                       date = i.date
                       impressions_list_all_adwords += [
                           {
                               "impressions": int(i.impressions),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       cost_list_all_adwords += [
                           {
                               "spend": '%0.2f' % (float(i.cost)),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       clicks_list_all_adwords += [
                           {
                               "clicks": int(i.clicks),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       conversions_list_all_adwords += [
                           {
                               "conversions": float(i.conversions),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       ctr_list_all_adwords += [
                           {
                               "ctr": '%0.2f' % (float(i.ctr)),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       cvr_list_all_adwords += [
                           {
                               "cvr": '%0.2f' % (float(i.cvr)),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       cpc_list_all_adwords += [
                           {
                               "cpc": '%0.2f' % (float(i.cpc)),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       cpi_list_all_adwords += [
                           {
                               "cpi": '%0.2f' % (float(i.cpi)),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       revenue_list_all_adwords += [
                           {
                               "revenue": '%0.2f' % (float(i.revenue)),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       profit_list_all_adwords += [
                           {
                               "profit": '%0.2f' % (float(i.profit)),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]

                   data_range_result_adwords = data_range(impressions_list_all_adwords,cost_list_all_adwords,clicks_list_all_adwords,conversions_list_all_adwords,ctr_list_all_adwords,cvr_list_all_adwords,cpc_list_all_adwords,cpi_list_all_adwords,revenue_list_all_adwords,profit_list_all_adwords)
                   revenue_list_new = data_range_result_adwords["revenue"][::-1]
                   cost_list_new = data_range_result_adwords["costs"][::-1]
                   profit_list_new = data_range_result_adwords["profit"][::-1]
                   impressions_list_new = data_range_result_adwords["impressions"][::-1]
                   clicks_list_new = data_range_result_adwords["clicks"][::-1]
                   conversions_list_new = data_range_result_adwords["conversions"][::-1]
                   date_new = data_range_result_adwords["date"][::-1]
                   for i in range(len(date_new)):
                       impressions_list += [
                           {
                               "impressions": float(impressions_list_new[i]),
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       cost_list += [
                           {
                               "spend": '%0.2f' % (float(cost_list_new[i])),
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       clicks_list += [
                           {
                               "clicks": float(clicks_list_new[i]),
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       conversions_list += [
                           {
                               "conversions": float(conversions_list_new[i]),
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       ctr_list += [
                           {
                               "ctr": '%0.2f' % (float(clicks_list_new[i]) / float(impressions_list_new[i]) * 100) if impressions_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       cvr_list += [
                           {
                               "cvr": '%0.2f' % (float(conversions_list_new[i]) / float(clicks_list_new[i]) * 100) if clicks_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       cpc_list += [
                           {
                               "cpc": '%0.2f' % (float(cost_list_new[i]) / float(clicks_list_new[i])) if clicks_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       cpi_list += [
                           {
                               "cpi": '%0.2f' % (float(cost_list_new[i]) / float(conversions_list_new[i])) if conversions_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       revenue_list += [
                           {
                               "revenue": '%0.2f' % (float(revenue_list_new[i])),
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       profit_list += [
                           {
                               "profit": '%0.2f' % (float(profit_list_new[i])),
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]

                   ## facebook
                   impressions_list_all_fb = []
                   cost_list_all_fb = []
                   clicks_list_all_fb = []
                   conversions_list_all_fb = []
                   ctr_list_all_fb = []
                   cvr_list_all_fb = []
                   cpc_list_all_fb = []
                   cpi_list_all_fb = []
                   revenue_list_all_fb = []
                   profit_list_all_fb = []
                   for i in facebook_results:
                       date = i.date
                       impressions_list_all_fb += [
                           {
                               "impressions": int(i.impressions),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       cost_list_all_fb += [
                           {
                               "spend": '%0.2f' % (float(i.cost)),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       clicks_list_all_fb += [
                           {
                               "clicks": int(i.clicks),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       conversions_list_all_fb += [
                           {
                               "conversions": float(i.conversions),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       ctr_list_all_fb += [
                           {
                               "ctr": '%0.2f' % (float(i.ctr)),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       cvr_list_all_fb += [
                           {
                               "cvr": '%0.2f' % (float(i.cvr)),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       cpc_list_all_fb += [
                           {
                               "cpc": '%0.2f' % (float(i.cpc)),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       cpi_list_all_fb += [
                           {
                               "cpi": '%0.2f' % (float(i.cpi)),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       revenue_list_all_fb += [
                           {
                               "revenue": '%0.2f' % (float(i.revenue)),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       profit_list_all_fb += [
                           {
                               "profit": '%0.2f' % (float(i.profit)),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]

                   data_range_result_fb = data_range(impressions_list_all_fb, cost_list_all_fb, clicks_list_all_fb,
                                                          conversions_list_all_fb, ctr_list_all_fb, cvr_list_all_fb,
                                                          cpc_list_all_fb, cpi_list_all_fb, revenue_list_all_fb,profit_list_all_fb)
                   revenue_list_new = data_range_result_fb["revenue"][::-1]
                   cost_list_new = data_range_result_fb["costs"][::-1]
                   profit_list_new = data_range_result_fb["profit"][::-1]
                   impressions_list_new = data_range_result_fb["impressions"][::-1]
                   clicks_list_new = data_range_result_fb["clicks"][::-1]
                   conversions_list_new = data_range_result_fb["conversions"][::-1]
                   date_new = data_range_result_fb["date"][::-1]
                   for i in range(len(date_new)):
                       impressions_list += [
                           {
                               "impressions": float(impressions_list_new[i]),
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       cost_list += [
                           {
                               "spend": '%0.2f' % (float(cost_list_new[i])),
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       clicks_list += [
                           {
                               "clicks": float(clicks_list_new[i]),
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       conversions_list += [
                           {
                               "conversions": float(conversions_list_new[i]),
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       ctr_list += [
                           {
                               "ctr": '%0.2f' % (float(clicks_list_new[i]) / float(impressions_list_new[i]) * 100) if impressions_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       cvr_list += [
                           {
                               "cvr": '%0.2f' % (float(conversions_list_new[i]) / float(clicks_list_new[i]) * 100) if clicks_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       cpc_list += [
                           {
                               "cpc": '%0.2f' % (float(cost_list_new[i]) / float(clicks_list_new[i])) if clicks_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       cpi_list += [
                           {
                               "cpi": '%0.2f' % (float(cost_list_new[i]) / float(conversions_list_new[i])) if conversions_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       revenue_list += [
                           {
                               "revenue": '%0.2f' % (float(revenue_list_new[i])),
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       profit_list += [
                           {
                               "profit": '%0.2f' % (float(profit_list_new[i])),
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]

                   ## apple
                   impressions_list_all_ap = []
                   cost_list_all_ap = []
                   clicks_list_all_ap = []
                   conversions_list_all_ap = []
                   ctr_list_all_ap = []
                   cvr_list_all_ap = []
                   cpc_list_all_ap = []
                   cpi_list_all_ap = []
                   revenue_list_all_ap = []
                   profit_list_all_ap = []
                   for i in apple_results:
                       date = i.date
                       impressions_list_all_ap += [
                           {
                               "impressions": int(i.impressions),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       cost_list_all_ap += [
                           {
                               "spend": '%0.2f' % (float(i.cost)),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       clicks_list_all_ap += [
                           {
                               "clicks": int(i.clicks),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       conversions_list_all_ap += [
                           {
                               "conversions": float(i.conversions),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       ctr_list_all_ap += [
                           {
                               "ctr": '%0.2f' % (float(i.ctr)),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       cvr_list_all_ap += [
                           {
                               "cvr": '%0.2f' % (float(i.cvr)),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       cpc_list_all_ap += [
                           {
                               "cpc": '%0.2f' % (float(i.cpc)),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       cpi_list_all_ap += [
                           {
                               "cpi": '%0.2f' % (float(i.cpi)),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       revenue_list_all_ap += [
                           {
                               "revenue": '%0.2f' % (float(i.revenue)),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       profit_list_all_ap += [
                           {
                               "profit": '%0.2f' % (float(i.profit)),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]

                   data_range_result_ap = data_range(impressions_list_all_ap, cost_list_all_ap, clicks_list_all_ap,
                                                     conversions_list_all_ap, ctr_list_all_ap, cvr_list_all_ap,
                                                     cpc_list_all_ap, cpi_list_all_ap, revenue_list_all_ap, profit_list_all_ap)
                   revenue_list_new = data_range_result_ap["revenue"][::-1]
                   cost_list_new = data_range_result_ap["costs"][::-1]
                   profit_list_new = data_range_result_ap["profit"][::-1]
                   impressions_list_new = data_range_result_ap["impressions"][::-1]
                   clicks_list_new = data_range_result_ap["clicks"][::-1]
                   conversions_list_new = data_range_result_ap["conversions"][::-1]
                   date_new = data_range_result_ap["date"][::-1]
                   for i in range(len(date_new)):
                       impressions_list += [
                           {
                               "impressions": float(impressions_list_new[i]),
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       cost_list += [
                           {
                               "spend": '%0.2f' % (float(cost_list_new[i])),
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       clicks_list += [
                           {
                               "clicks": float(clicks_list_new[i]),
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       conversions_list += [
                           {
                               "conversions": float(conversions_list_new[i]),
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       ctr_list += [
                           {
                               "ctr": '%0.2f' % (float(clicks_list_new[i]) / float(impressions_list_new[i]) * 100) if impressions_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       cvr_list += [
                           {
                               "cvr": '%0.2f' % (float(conversions_list_new[i]) / float(clicks_list_new[i]) * 100) if clicks_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       cpc_list += [
                           {
                               "cpc": '%0.2f' % (float(cost_list_new[i]) / float(clicks_list_new[i])) if clicks_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       cpi_list += [
                           {
                               "cpi": '%0.2f' % (float(cost_list_new[i]) / float(conversions_list_new[i])) if conversions_list_new[i] != 0 else 0,
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       revenue_list += [
                           {
                               "revenue": '%0.2f' % (float(revenue_list_new[i])),
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       profit_list += [
                           {
                               "profit": '%0.2f' % (float(profit_list_new[i])),
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]

                   data_date_table = {
                       "impressions_list": impressions_list,
                       "cost_list": cost_list,
                       "clicks_list": clicks_list,
                       "conversions_list": conversions_list,
                       "ctr_list": ctr_list,
                       "cvr_list": cvr_list,
                       "cpc_list": cpc_list,
                       "cpi_list": cpi_list,
                       "revenue_list": revenue_list,
                       "profit_list": profit_list,
                       "head": ["Date", "source","Revenue", "Profit", "Cost", "Impressions", "Clicks", "Conversions", "CTR", "CVR", "CPC", "CPI"]
                   }
                   data_geo = data_count(impressions_list, cost_list, clicks_list, conversions_list, revenue_list, profit_list)
                   data_range_result = data_range(impressions_list,cost_list,clicks_list,conversions_list,ctr_list,cvr_list,cpc_list,cpi_list,revenue_list,profit_list)
                   return json.dumps({
                       "code": 200,
                       "data_geo": data_geo,
                       "data_geo_table": {},
                       "data_date_table": data_date_table,
                       "data_range": data_range_result,
                       "message": "success"
                   })
               else:
                   adwords_results = Adwords.query.filter(Adwords.offer_id == offerId, Adwords.date >= start_date, Adwords.date <= end_date).order_by(Adwords.date.desc()).all()
                   data_results = Datas.query.filter(Datas.offer_id==offerId,Datas.date>=start_date,Datas.date<=end_date).order_by(Datas.date.desc()).all()
                   impressions_list_all = []
                   cost_list_all = []
                   clicks_list_all = []
                   conversions_list_all = []
                   ctr_list_all = []
                   cvr_list_all=[]
                   cpc_list_all=[]
                   cpi_list_all=[]
                   revenue_list_all=[]
                   profit_list_all=[]
                   for i in data_results:
                       date = i.date
                       impressions_list_all += [
                           {
                               "impressions": int(i.impressions),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cost_list_all += [
                           {
                               "spend": '%0.2f' % (float(i.cost)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       clicks_list_all += [
                           {
                               "clicks": int(i.clicks),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       conversions_list_all += [
                           {
                               "conversions": int(i.conversions),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       ctr_list_all += [
                           {
                               "ctr": '%0.2f' % (float(i.ctr)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cvr_list_all += [
                           {
                               "cvr": '%0.2f' % (float(i.cvr)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cpc_list_all += [
                           {
                               "cpc": '%0.2f' % (float(i.cpc)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cpi_list_all += [
                           {
                               "cpi": '%0.2f' % (float(i.cpi)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       revenue_list_all += [
                           {
                               "revenue": '%0.2f' % (float(i.revenue)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       profit_list_all += [
                           {
                               "profit": '%0.2f' % (float(i.profit)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]

                   for i in adwords_results:
                       date = i.date
                       impressions_list_all += [
                           {
                               "impressions": int(i.impressions),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cost_list_all += [
                           {
                               "spend": '%0.2f' % (float(i.cost)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       clicks_list_all += [
                           {
                               "clicks": int(i.clicks),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       conversions_list_all += [
                           {
                               "conversions": float(i.conversions),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       ctr_list_all += [
                           {
                               "ctr": '%0.2f' % (float(i.ctr)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cvr_list_all += [
                           {
                               "cvr": '%0.2f' % (float(i.cvr)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cpc_list_all += [
                           {
                               "cpc": '%0.2f' % (float(i.cpc)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cpi_list_all += [
                           {
                               "cpi": '%0.2f' % (float(i.cpi)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       revenue_list_all += [
                           {
                               "revenue": '%0.2f' % (float(i.revenue)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       profit_list_all += [
                           {
                               "profit": '%0.2f' % (float(i.profit)),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]

                   data_range_result = data_range(impressions_list_all,cost_list_all,clicks_list_all,conversions_list_all,ctr_list_all,cvr_list_all,cpc_list_all,cpi_list_all,revenue_list_all,profit_list_all)
                   revenue_list_new = data_range_result["revenue"][::-1]
                   cost_list_new = data_range_result["costs"][::-1]
                   profit_list_new = data_range_result["profit"][::-1]
                   impressions_list_new = data_range_result["impressions"][::-1]
                   clicks_list_new = data_range_result["clicks"][::-1]
                   conversions_list_new = data_range_result["conversions"][::-1]
                   date_new = data_range_result["date"][::-1]
                   for i in range(len(date_new)):
                       impressions_list += [
                           {
                               "impressions":float(impressions_list_new[i]),
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       cost_list += [
                           {
                               "spend": '%0.2f'%(float(cost_list_new[i])),
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       clicks_list += [
                           {
                               "clicks": float(clicks_list_new[i]),
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       conversions_list += [
                           {
                               "conversions": float(conversions_list_new[i]),
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       ctr_list += [
                           {
                               "ctr": '%0.2f'%(float(clicks_list_new[i])/float(impressions_list_new[i])*100) if impressions_list_new[i] !=0 else 0,
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       cvr_list += [
                           {
                               "cvr": '%0.2f' % (float(conversions_list_new[i]) / float(clicks_list_new[i]) * 100) if clicks_list_new[i] !=0 else 0,
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       cpc_list += [
                           {
                               "cpc": '%0.2f' % (float(cost_list_new[i]) / float(clicks_list_new[i])) if float(clicks_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       cpi_list += [
                           {
                               "cpi": '%0.2f' % (float(cost_list_new[i]) / float(conversions_list_new[i])) if float(conversions_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       revenue_list += [
                           {
                               "revenue": '%0.2f'%(float(revenue_list_new[i])),
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       profit_list += [
                           {
                               "profit": '%0.2f'%(float(profit_list_new[i])),
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]

                   data_date_table = {
                       "impressions_list": impressions_list,
                       "cost_list": cost_list,
                       "clicks_list": clicks_list,
                       "conversions_list": conversions_list,
                       "ctr_list": ctr_list,
                       "cvr_list": cvr_list,
                       "cpc_list": cpc_list,
                       "cpi_list": cpi_list,
                       "revenue_list": revenue_list,
                       "profit_list": profit_list,
                       "head": ["Date", "Revenue", "Profit", "Cost", "Impressions", "Clicks", "Conversions", "CTR", "CVR", "CPC", "CPI"]
                   }
                   data_geo = data_count(impressions_list,cost_list,clicks_list,conversions_list,revenue_list,profit_list)
                   return json.dumps({
                       "code": 200,
                       "data_geo": data_geo,
                       "data_geo_table": {},
                       "data_date_table": data_date_table,
                       "data_range": data_range_result,
                       "message": "success"
                   })
           except Exception as e:
               print e
               return json.dumps({
                   "code": 500,
                   "message": "no bind data or bind wrong data"
               })
