# -*- coding: utf-8 -*-
from __future__ import division
from flask import Blueprint, request
# from main import db, adwordsData
import adwordsData
from models import Advertisers, Datas
import json
import os
import datetime

facebookDate = Blueprint('facebookDate', __name__)

@facebookDate.route('/api/dashboard')
def dashboard():
    yesterday = (datetime.datetime.now()-datetime.timedelta(hours=16)).strftime("%Y-%m-%d")

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
        ctr += float(i.ctr)

    if conversions != 0:
        cpi = '%0.2f' % (cost / float(conversions))

    if clicks != 0:
        cvr = '%0.2f' % (float(conversions) / float(clicks) * 100)

    if clicks != 0:
        cpc = '%0.2f' % (float(cost) / float(clicks))

    if impressions != 0:
        ctr = '%0.2f' % (clicks / impressions * 100)

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
        "profit": '%0.2f'%(profit)
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
                data_results = Datas.query.filter(Datas.offer_id==offerId,Datas.date >= start_date, Datas.date<=end_date).order_by(Datas.date.desc()).all()
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
                            "conversions": int(i.conversions),
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
                    "head": ["Date", "Geo", "Revenue", "Profit", "Cost", "Impressions", "Clicks", "Conversions", "CTR", "CVR", "CPC", "CPI"]
                }
                data_range_result = data_range(impressions_list,cost_list,clicks_list,conversions_list,ctr_list,cvr_list,cpc_list,cpi_list,revenue_list,profit_list)
                data_geo = data_count(impressions_list,cost_list,clicks_list,conversions_list,revenue_list,profit_list)
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
                           "cpc": '%0.2f' % (float(cost_list_new[i]) / float(clicks_list_new[i])) if clicks_list_new[i] != 0 else 0,
                           "date_start": date_new[i],
                           "date_stop": date_new[i]
                       }
                   ]
                   cpi_list += [
                       {
                           "cpi": '%0.2f' % (float(cost_list_new[i]) / float(conversions_list_new[i])) if conversions_list_new[i] != 0 else 0,
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