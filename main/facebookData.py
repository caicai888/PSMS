# -*- coding: utf-8 -*-
from __future__ import division
from flask import Blueprint, request
from models import Advertisers, Datas, Adwords, DataSolidified
import json
import re
import datetime
from main import db

facebookDate = Blueprint('facebookDate', __name__)

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
        "count_impressions": format(count_impressions,','),
        "count_cost": format(float('%0.2f' % (count_cost)),','),
        "count_clicks": format(count_clicks,','),
        "count_conversions": format(count_conversions,','),
        "count_ctr": count_ctr,
        "count_cvr": count_cvr,
        "count_cpc": count_cpc,
        "count_cpi": count_cpi,
        "revenue": format(float('%0.2f' % (count_revenue)),','),
        "profit": format(float('%0.2f' % (count_profit)),',')
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

    ctr_list_unique = []
    for c in range(len(clicks_list_unique)):
        ctr_list_unique += [
            {
                "ctr": '%0.2f' % (float(clicks_list_unique[c]['clicks']) / float(impressions_list_unique[c]["impressions"]) * 100 if float(
                    impressions_list_unique[c]["impressions"]) != 0 else 0),
                "country": clicks_list_unique[c]["country"],
                "date_start": clicks_list_unique[c]["date_start"],
                "date_stop": clicks_list_unique[c]['date_start']
            }
        ]


    cvr_list_unique = []
    for c in range(len(conversions_list_unique)):
        cvr_list_unique += [
            {
                "cvr": '%0.2f' % (float(conversions_list_unique[c]["conversions"]) / float(clicks_list_unique[c]["clicks"]) * 100 if float(clicks_list_unique[c]["clicks"]) != 0 else 0),
                "country": conversions_list_unique[c]["country"],
                "date_start": conversions_list_unique[c]['date_start'],
                "date_stop": conversions_list_unique[c]['date_start']
            }
        ]

    cpi_list_unique = []
    for c in range(len(cost_list_unique)):
        cpi_list_unique += [
            {
                "cpi": '%0.2f' % (float(cost_list_unique[c]["spend"]) / float(conversions_list_unique[c]['conversions']) if float(conversions_list_unique[c]['conversions']) != 0 else 0),
                "country": cost_list_unique[c]["country"],
                "date_start": cost_list_unique[c]["date_start"],
                "date_stop": cost_list_unique[c]["date_start"]
            }
        ]

    cpc_list_unique = []
    for c in range(len(cost_list_unique)):
        cpc_list_unique += [
            {
                "cpc": '%0.2f' % (float(cost_list_unique[c]["spend"]) / float(clicks_list_unique[c]['clicks']) if float(clicks_list_unique[c]['clicks']) != 0 else 0),
                "country": cost_list_unique[c]["country"],
                "date_start": cost_list_unique[c]["date_start"],
                "date_stop": cost_list_unique[c]["date_start"]
            }
        ]

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
                                "spend": float('%0.2f' % (float(i.cost))),
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
                        revenue_list_ad += [
                            {
                                "revenue": float('%0.2f' % (float(i.revenue))),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]
                        profit_list_ad += [
                            {
                                "profit": float('%0.2f' % (float(i.profit))),
                                "country": country,
                                "date_start": date,
                                "source": "adwords"
                            }
                        ]

                    adwords_results_unique = unique_list(impressions_list_ad,cost_list_ad,clicks_list_ad,conversions_list_ad,ctr_list_ad,cvr_list_ad,cpc_list_ad,cpi_list_ad,revenue_list_ad,profit_list_ad)
                    impressions_list.extend(adwords_results_unique[0])
                    cost_list.extend(adwords_results_unique[1])
                    clicks_list.extend(adwords_results_unique[2])
                    conversions_list.extend(adwords_results_unique[3])
                    ctr_list.extend(adwords_results_unique[4])
                    cvr_list.extend(adwords_results_unique[5])
                    cpc_list.extend(adwords_results_unique[6])
                    cpi_list.extend(adwords_results_unique[7])
                    revenue_list.extend(adwords_results_unique[8])
                    profit_list.extend(adwords_results_unique[9])

                    ## facebook
                    impressions_list_fb = []
                    cost_list_fb = []
                    clicks_list_fb = []
                    conversions_list_fb = []
                    ctr_list_fb = []
                    cvr_list_fb = []
                    cpc_list_fb = []
                    cpi_list_fb = []
                    revenue_list_fb = []
                    profit_list_fb = []
                    for i in facebook_results:
                        date = i.date
                        country = i.country
                        impressions_list_fb += [
                            {
                                "impressions": int(i.impressions),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        cost_list_fb += [
                            {
                                "spend": float('%0.2f' % (float(i.cost))),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        clicks_list_fb += [
                            {
                                "clicks": int(i.clicks),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        conversions_list_fb += [
                            {
                                "conversions": float(i.conversions),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        revenue_list_fb += [
                            {
                                "revenue": float('%0.2f' % (float(i.revenue))),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]
                        profit_list_fb += [
                            {
                                "profit": float('%0.2f' % (float(i.profit))),
                                "country": country,
                                "date_start": date,
                                "source": "facebook"
                            }
                        ]

                    facebook_results_unique = unique_list(impressions_list_fb, cost_list_fb, clicks_list_fb, conversions_list_fb, ctr_list_fb,cvr_list_fb, cpc_list_fb, cpi_list_fb, revenue_list_fb, profit_list_fb)
                    impressions_list.extend(facebook_results_unique[0])
                    cost_list.extend(facebook_results_unique[1])
                    clicks_list.extend(facebook_results_unique[2])
                    conversions_list.extend(facebook_results_unique[3])
                    ctr_list.extend(facebook_results_unique[4])
                    cvr_list.extend(facebook_results_unique[5])
                    cpc_list.extend(facebook_results_unique[6])
                    cpi_list.extend(facebook_results_unique[7])
                    revenue_list.extend(facebook_results_unique[8])
                    profit_list.extend(facebook_results_unique[9])

                    ## apple
                    impressions_list_ap = []
                    cost_list_ap = []
                    clicks_list_ap = []
                    conversions_list_ap = []
                    ctr_list_ap = []
                    cvr_list_ap = []
                    cpc_list_ap = []
                    cpi_list_ap = []
                    revenue_list_ap = []
                    profit_list_ap = []
                    for i in apple_results:
                        date = i.date
                        country = i.country
                        impressions_list_ap += [
                            {
                                "impressions": int(i.impressions),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        cost_list_ap += [
                            {
                                "spend": float('%0.2f' % (float(i.cost))),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        clicks_list_ap += [
                            {
                                "clicks": int(i.clicks),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        conversions_list_ap += [
                            {
                                "conversions": float(i.conversions),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        revenue_list_ap += [
                            {
                                "revenue": float('%0.2f' % (float(i.revenue))),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                        profit_list_ap += [
                            {
                                "profit": float('%0.2f' % (float(i.profit))),
                                "country": country,
                                "date_start": date,
                                "source": "apple"
                            }
                        ]
                    apple_results_unique = unique_list(impressions_list_ap, cost_list_ap, clicks_list_ap, conversions_list_ap, ctr_list_ap,cvr_list_ap, cpc_list_ap, cpi_list_ap, revenue_list_ap, profit_list_ap)
                    impressions_list.extend(apple_results_unique[0])
                    cost_list.extend(apple_results_unique[1])
                    clicks_list.extend(apple_results_unique[2])
                    conversions_list.extend(apple_results_unique[3])
                    ctr_list.extend(apple_results_unique[4])
                    cvr_list.extend(apple_results_unique[5])
                    cpc_list.extend(apple_results_unique[6])
                    cpi_list.extend(apple_results_unique[7])
                    revenue_list.extend(apple_results_unique[8])
                    profit_list.extend(apple_results_unique[9])

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
                                    # x['spend'] += float(ele['spend'])
                                    x['spend'] += float("{:.2f}".format(float(ele['spend'])))
                        else:
                            ele['spend'] = float("{:.2f}".format(float(ele['spend'])))
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

                    ctr_list_unique = []
                    for c in range(len(clicks_list_unique)):
                        ctr_list_unique += [
                            {
                                "ctr": '%0.2f'%(float(clicks_list_unique[c]['clicks'])/float(impressions_list_unique[c]["impressions"])*100 if float(impressions_list_unique[c]["impressions"]) != 0 else 0),
                                "country": clicks_list_unique[c]["country"],
                                "date_start": clicks_list_unique[c]["date_start"],
                                "date_stop": clicks_list_unique[c]['date_start']
                            }
                        ]

                    cpc_list_unique = []
                    for c in range(len(cost_list_unique)):
                        cpc_list_unique += [
                            {
                                "cpc": '%0.2f' % (float(cost_list_unique[c]["spend"]) / float(clicks_list_unique[c]['clicks']) if float(clicks_list_unique[c]['clicks']) != 0 else 0),
                                "country": cost_list_unique[c]["country"],
                                "date_start": cost_list_unique[c]["date_start"],
                                "date_stop": cost_list_unique[c]["date_start"]
                            }
                        ]

                    cvr_list_unique = []
                    for c in range(len(conversions_list_unique)):
                        cvr_list_unique += [
                            {
                                "cvr": '%0.2f'%(float(conversions_list_unique[c]["conversions"])/float(clicks_list_unique[c]["clicks"])*100 if float(clicks_list_unique[c]["clicks"]) != 0 else 0),
                                "country": conversions_list_unique[c]["country"],
                                "date_start": conversions_list_unique[c]['date_start'],
                                "date_stop": conversions_list_unique[c]['date_start']
                            }
                        ]

                    cpi_list_unique = []
                    for c in range(len(cost_list_unique)):
                        cpi_list_unique += [
                            {
                                "cpi": '%0.2f' % (float(cost_list_unique[c]["spend"])/float(conversions_list_unique[c]['conversions']) if float(conversions_list_unique[c]['conversions']) != 0 else 0),
                                "country": cost_list_unique[c]["country"],
                                "date_start": cost_list_unique[c]["date_start"],
                                "date_stop": cost_list_unique[c]["date_start"]
                            }
                        ]

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
                               "spend": float('%0.2f' % (float(i.cost))),
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
                               "ctr": float('%0.2f' % (float(i.ctr))),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       cvr_list_all_adwords += [
                           {
                               "cvr": float('%0.2f' % (float(i.cvr))),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       cpc_list_all_adwords += [
                           {
                               "cpc": float('%0.2f' % (float(i.cpc))),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       cpi_list_all_adwords += [
                           {
                               "cpi": float('%0.2f' % (float(i.cpi))),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       revenue_list_all_adwords += [
                           {
                               "revenue": float('%0.2f' % (float(i.revenue))),
                               "date_start": date,
                               "source": "adwords"
                           }
                       ]
                       profit_list_all_adwords += [
                           {
                               "profit": float('%0.2f' % (float(i.profit))),
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
                               "spend": float('%0.2f' % (float(cost_list_new[i]))),
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
                               "ctr": float('%0.2f' % (float(clicks_list_new[i]) / float(impressions_list_new[i]) * 100)) if float(impressions_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       cvr_list += [
                           {
                               "cvr": float('%0.2f' % (float(conversions_list_new[i]) / float(clicks_list_new[i]) * 100)) if float(clicks_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       cpc_list += [
                           {
                               "cpc": float('%0.2f' % (float(cost_list_new[i]) / float(clicks_list_new[i]))) if float(clicks_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       cpi_list += [
                           {
                               "cpi": float('%0.2f' % (float(cost_list_new[i]) / float(conversions_list_new[i]))) if float(conversions_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       revenue_list += [
                           {
                               "revenue": float('%0.2f' % (float(revenue_list_new[i]))),
                               "date_start": date_new[i],
                               "source": "adwords"
                           }
                       ]
                       profit_list += [
                           {
                               "profit": float('%0.2f' % (float(profit_list_new[i]))),
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
                               "spend": float('%0.2f' % (float(i.cost))),
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
                               "ctr": float('%0.2f' % (float(i.ctr))),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       cvr_list_all_fb += [
                           {
                               "cvr": float('%0.2f' % (float(i.cvr))),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       cpc_list_all_fb += [
                           {
                               "cpc": float('%0.2f' % (float(i.cpc))),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       cpi_list_all_fb += [
                           {
                               "cpi": float('%0.2f' % (float(i.cpi))),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       revenue_list_all_fb += [
                           {
                               "revenue": float('%0.2f' % (float(i.revenue))),
                               "date_start": date,
                               "source": "facebook"
                           }
                       ]
                       profit_list_all_fb += [
                           {
                               "profit": float('%0.2f' % (float(i.profit))),
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
                               "spend": float('%0.2f' % (float(cost_list_new[i]))),
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
                               "ctr": float('%0.2f' % (float(clicks_list_new[i]) / float(impressions_list_new[i]) * 100)) if float(impressions_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       cvr_list += [
                           {
                               "cvr": float('%0.2f' % (float(conversions_list_new[i]) / float(clicks_list_new[i]) * 100)) if float(clicks_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       cpc_list += [
                           {
                               "cpc": float('%0.2f' % (float(cost_list_new[i]) / float(clicks_list_new[i]))) if float(clicks_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       cpi_list += [
                           {
                               "cpi": float('%0.2f' % (float(cost_list_new[i]) / float(conversions_list_new[i]))) if float(conversions_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       revenue_list += [
                           {
                               "revenue": float('%0.2f' % (float(revenue_list_new[i]))),
                               "date_start": date_new[i],
                               "source": "facebook"
                           }
                       ]
                       profit_list += [
                           {
                               "profit": float('%0.2f' % (float(profit_list_new[i]))),
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
                               "spend": float('%0.2f' % (float(i.cost))),
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
                               "ctr": float('%0.2f' % (float(i.ctr))),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       cvr_list_all_ap += [
                           {
                               "cvr": float('%0.2f' % (float(i.cvr))),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       cpc_list_all_ap += [
                           {
                               "cpc": float('%0.2f' % (float(i.cpc))),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       cpi_list_all_ap += [
                           {
                               "cpi": float('%0.2f' % (float(i.cpi))),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       revenue_list_all_ap += [
                           {
                               "revenue": float('%0.2f' % (float(i.revenue))),
                               "date_start": date,
                               "source": "apple"
                           }
                       ]
                       profit_list_all_ap += [
                           {
                               "profit": float('%0.2f' % (float(i.profit))),
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
                               "spend": float('%0.2f' % (float(cost_list_new[i]))),
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
                               "ctr": float('%0.2f' % (float(clicks_list_new[i]) / float(impressions_list_new[i]) * 100)) if float(impressions_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       cvr_list += [
                           {
                               "cvr": float('%0.2f' % (float(conversions_list_new[i]) / float(clicks_list_new[i]) * 100)) if float(clicks_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       cpc_list += [
                           {
                               "cpc": float('%0.2f' % (float(cost_list_new[i]) / float(clicks_list_new[i]))) if float(clicks_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       cpi_list += [
                           {
                               "cpi": float('%0.2f' % (float(cost_list_new[i]) / float(conversions_list_new[i]))) if float(conversions_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       revenue_list += [
                           {
                               "revenue": float('%0.2f' % (float(revenue_list_new[i]))),
                               "date_start": date_new[i],
                               "source": "apple"
                           }
                       ]
                       profit_list += [
                           {
                               "profit": float('%0.2f' % (float(profit_list_new[i]))),
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
                               "spend": float('%0.2f' % (float(i.cost))),
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
                               "ctr": float('%0.2f' % (float(i.ctr))),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cvr_list_all += [
                           {
                               "cvr": float('%0.2f' % (float(i.cvr))),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cpc_list_all += [
                           {
                               "cpc": float('%0.2f' % (float(i.cpc))),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cpi_list_all += [
                           {
                               "cpi": float('%0.2f' % (float(i.cpi))),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       revenue_list_all += [
                           {
                               "revenue": float('%0.2f' % (float(i.revenue))),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       profit_list_all += [
                           {
                               "profit": float('%0.2f' % (float(i.profit))),
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
                               "spend": float('%0.2f' % (float(i.cost))),
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
                               "ctr": float('%0.2f' % (float(i.ctr))),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cvr_list_all += [
                           {
                               "cvr": float('%0.2f' % (float(i.cvr))),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cpc_list_all += [
                           {
                               "cpc": float('%0.2f' % (float(i.cpc))),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       cpi_list_all += [
                           {
                               "cpi": float('%0.2f' % (float(i.cpi))),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       revenue_list_all += [
                           {
                               "revenue": float('%0.2f' % (float(i.revenue))),
                               "date_start": date,
                               "date_stop": date
                           }
                       ]
                       profit_list_all += [
                           {
                               "profit": float('%0.2f' % (float(i.profit))),
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
                               "spend": float('%0.2f'%(float(cost_list_new[i]))),
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
                               "ctr": float('%0.2f'%(float(clicks_list_new[i])/float(impressions_list_new[i])*100)) if float(impressions_list_new[i]) !=0 else 0,
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       cvr_list += [
                           {
                               "cvr": float('%0.2f' % (float(conversions_list_new[i]) / float(clicks_list_new[i]) * 100)) if float(clicks_list_new[i]) !=0 else 0,
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       cpc_list += [
                           {
                               "cpc": float('%0.2f' % (float(cost_list_new[i]) / float(clicks_list_new[i]))) if float(clicks_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       cpi_list += [
                           {
                               "cpi": float('%0.2f' % (float(cost_list_new[i]) / float(conversions_list_new[i]))) if float(conversions_list_new[i]) != 0 else 0,
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       revenue_list += [
                           {
                               "revenue": float('%0.2f'%(float(revenue_list_new[i]))),
                               "date_start": date_new[i],
                               "date_stop": date_new[i]
                           }
                       ]
                       profit_list += [
                           {
                               "profit": float('%0.2f'%(float(profit_list_new[i]))),
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

#数据固化
@facebookDate.route('/api/report/solidify',methods=["POST","GET"])
def dataSolidify():
    if request.method == "POST":
        data = request.get_json(force=True)
        offerId = int(data['offer_id'])
        start_date = data["start_date"]
        end_date = data["end_date"]
        solidifies_data = []
        createdTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        dataSolidifies = DataSolidified.query.filter(DataSolidified.offer_id==offerId,DataSolidified.date >= start_date,DataSolidified.date <= end_date).all()
        if dataSolidifies:
            return json.dumps({
                "code": 500,
                "message": u"您选择的日期中有固化的数据,请重新选择日期"
            })
        else:
            adwordsDatas = Adwords.query.filter(Adwords.offer_id == offerId,Adwords.date >= start_date,Adwords.date <= end_date).all()
            for a in adwordsDatas:
                solidifies_data += [
                    {
                        "date": a.date,
                        "offer_id": offerId,
                        "type": "adwords",
                        "revenue": a.revenue,
                        "cost": a.cost,
                        "profit": a.profit,
                        "impressions": a.impressions,
                        "clicks": a.clicks,
                        "conversions": a.conversions,
                        "ctr": a.ctr,
                        "cvr": a.cvr,
                        "cpc": a.cpc,
                        "cpi": a.cpi,
                        "country": a.country,
                        "rebate": a.rebate,
                        "createdTime": createdTime
                    }
                ]
            data_all = Datas.query.filter(Datas.offer_id == offerId, Datas.date >= start_date,Datas.date <= end_date).all()
            for i in data_all:
                solidifies_data += [
                    {
                        "date": i.date,
                        "offer_id": offerId,
                        "type": i.type,
                        "revenue": i.revenue,
                        "cost": i.cost,
                        "profit": i.profit,
                        "impressions": i.impressions,
                        "clicks": i.clicks,
                        "conversions": i.conversions,
                        "ctr": i.ctr,
                        "cvr": i.cvr,
                        "cpc": i.cpc,
                        "cpi": i.cpi,
                        "country": i.country,
                        "rebate": i.rebate,
                        "createdTime": createdTime,
                        "id": i.id
                    }
                ]
            if solidifies_data == []:
                return json.dumps({
                    "code": 500,
                    "message": u"该时间段内没有数据,不能固化哦!"
                })
            for j in solidifies_data:
                data_solidify = DataSolidified(j['offer_id'],j['type'],j['revenue'],j['profit'],j['cost'],j['impressions'],j['clicks'],j['conversions'],j['ctr'],j['cvr'],j['cpc'],j['cpi'],j['date'],j['country'],j['rebate'],j['createdTime'])
                try:
                    db.session.add(data_solidify)
                    db.session.commit()
                    db.create_all()
                except Exception as e:
                    print e
                    return json.dumps({
                        "code": 500,
                        "message": u"固化失败"
                    })
            return json.dumps({
                "code": 200,
                "message": "success"
            })