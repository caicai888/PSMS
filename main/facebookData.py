# -*- coding: utf-8 -*-
from __future__ import division
from main.has_permission import *
from flask import Blueprint, request
from main import db
from models import Offer, Token, Advertisers, TimePrice, Country
import json
import os
import datetime, time
import requests
from collections import Counter

facebookDate = Blueprint('facebookDate', __name__)

@facebookDate.route('/api/dashboard')
def dashboard():
    yesterday = (datetime.datetime.now()-datetime.timedelta(hours=24)).strftime("%Y-%m-%d")
    yesterday = "2016-08-27"
    token = Token.query.filter().first()
    accessToken = token.accessToken
    time_range = "{'since': "+"'"+str(yesterday)+"'"+", 'until': "+"'"+str(yesterday)+"'"+"}"
    url = "https://graph.facebook.com/v2.8/act_1004988846265857/insights"
    filed_lists = ["impressions","spend","clicks","cpc","ctr","actions"]
    result = []
    for i in filed_lists:
        params_impressions = {
            "access_token": accessToken,
            "level": "account",
            "fields": [i],
            "time_range": str(time_range)
        }
        result_impressions = requests.get(url=url, params=params_impressions)
        data_impressions = result_impressions.json()["data"]
        value = data_impressions[0].get(i)
        if i == "actions":
            i = "conversions"
            for action in data_impressions[0].get("actions"):
                if "offsite_conversion" in action["action_type"]:
                    conversions = action["value"]
                elif "link_click" in action["action_type"]:
                    conversions = action["value"]
                else:
                    conversions = 0
            value = conversions

        data = {
            i:value
        }
        result += [data]

    clicks = int(result[2].get("clicks"))
    if int(clicks) != int(0):
        cvr = '%0.2f'%(int(conversions) / int(clicks) * 100 )
    else:
        cvr = 0
    data_cvr = {
        "cvr": cvr
    }
    result += [data_cvr]
    if int(conversions) != 0:
        cpi = '%0.2f'%(float(result[1].get("spend"))/float(conversions))
    else:
        cpi = 0
    data_cpi = {
        "cpi": cpi
    }
    result += [data_cpi]
    revenue = float(conversions)*1.5
    data_revenue = {
        "revenue": str(revenue)
    }
    result += [data_revenue]
    profit = float(revenue) - float(result[1].get("spend"))
    data_profit = {
        "profit": str(profit)
    }
    result += [data_profit]
    response = {
        "code": 200,
        "message": "success",
        "result": result
    }
    return json.dumps(response)

@facebookDate.route('/api/report', methods=["POST","GET"])
def faceReport():
    if request.method == "POST":
        data = request.get_json(force=True)
        offerId = data["offer_id"]
        start_date = data["start_date"]
        end_date = data["end_date"]
        dimension = data["dimension"]
        offer = Offer.query.filter_by(id=offerId).first()
        price_default = offer.price
        advertiser = Advertisers.query.filter_by(offer_id=int(offerId),type="facebook").first()
        accessToken = advertiser.token
        accessToken = "EAAHgEYXO0BABAO8dhDyFvLiFnIuBpaYDYp6bcSRtkJQg5cpFy7BCJiL9xyQrRkVpheDhP4EGZCgKzBqKeGh9y0Fdd7PPZBzHnT0Q7hvyEWxTpKgJXyB3EkZBZA01OC6wx7f9NdX9popYJksnTNT2ZCpiFHX8gqIncF9vvGGEQtAZDZD"
        advertise_groups = advertiser.advertise_groups.split(",")
        advertise_groups = ["6050664418448","6050664365648","6050357178448"]
        count_impressions = 0
        count_cost = 0
        count_clicks = 0
        count_conversions = 0
        count_ctr = 0
        count_cpc = 0
        if "geo" in dimension:
            for i in advertise_groups:
                url = "https://graph.facebook.com/v2.8/"+str(i)+"/insights"
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["impressions"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_impressions += int(j["impressions"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["spend"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_cost += float(j["spend"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["clicks"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_clicks += float(j["clicks"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["actions"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    actions = j.get("actions",[])
                    for action in actions:
                        if "offsite_conversion" in action["action_type"]:
                            conversions = action["value"]
                            count_conversions += int(conversions)
                        elif "link_click" in action["action_type"]:
                            conversions = action["value"]
                            count_conversions += int(conversions)
                        else:
                            conversions = 0
                            count_conversions += conversions
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["ctr"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_ctr += float(j["ctr"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["cpc"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_cpc += float(j["cpc"])
            count_cvr = '%0.2f' % (count_conversions / count_clicks * 100) if count_clicks != 0 else 0
            count_cpi = '%0.2f'% (count_cost / count_conversions)
            revenue = count_conversions * 1.5
            profit = revenue - count_cost
            data_geo = {
                "count_impressions": count_impressions,
                "count_cost": count_cost,
                "count_clicks": count_clicks,
                "count_conversions": count_conversions,
                "count_ctr": count_ctr,
                "count_cvr": count_cvr,
                "count_cpc": count_cpc,
                "count_cpi": count_cpi,
                "revenue": revenue,
                "profit": profit
            }
            data_day = {}
        elif "date" in dimension and len(dimension)==1:
            #按着day维度的总数据
            for i in advertise_groups:
                url = "https://graph.facebook.com/v2.8/"+str(i)+"/insights"
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["impressions"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_impressions += int(j["impressions"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["spend"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_cost += float(j["spend"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["clicks"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_clicks += float(j["clicks"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["actions"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    actions = j.get("actions",[])
                    for action in actions:
                        if "offsite_conversion" in action["action_type"]:
                            conversions = action["value"]
                            count_conversions += int(conversions)
                        elif "link_click" in action["action_type"]:
                            conversions = action["value"]
                            count_conversions += int(conversions)
                        else:
                            conversions = 0
                            count_conversions += conversions
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["ctr"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_ctr += float(j["ctr"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["cpc"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_cpc += float(j["cpc"])
            count_cvr = '%0.2f' % (count_conversions / count_clicks * 100) if count_clicks != 0 else 0
            count_cpi = '%0.2f'% (count_cost / count_conversions)
            revenue = count_conversions * 1.5
            profit = revenue - count_cost
            data_day = {
                "count_impressions": count_impressions,
                "count_cost": count_cost,
                "count_clicks": count_clicks,
                "count_conversions": count_conversions,
                "count_ctr": count_ctr,
                "count_cvr": count_cvr,
                "count_cpc": count_cpc,
                "count_cpi": count_cpi,
                "revenue": revenue,
                "profit": profit
            }
            data_geo ={}


        all_date = ["2016-08-26","2016-08-27","2016-08-28","2016-08-29","2016-08-30","2016-08-31","2016-09-01","2016-09-02","2016-09-03","2016-09-04","2016-09-05","2016-09-06","2016-09-07","2016-09-08","2016-09-09","2016-09-10"]
        time_ranges = []
        for day in all_date[::-1]:
            time_ranges.append("{'since': " + "'" + str(day) + "'" + ", 'until': " + "'" + str(day) + "'" + "}")
        if "geo" in dimension:
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
            for i in advertise_groups:
                url = "https://graph.facebook.com/v2.8/"+str(i)+"/insights"
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["impressions"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    impressions_list.append(j)

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["spend"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    cost_list.append(j)

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["clicks"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    clicks_list.append(j)

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["actions"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    actions = j.get("actions",[])
                    for action in actions:
                        if "offsite_conversion" in action["action_type"]:
                            conversions = int(action["value"])
                        elif "link_click" in action["action_type"]:
                            conversions = int(action["value"])
                        else:
                            conversions = 0
                        conver_data = {
                            "country": j["country"],
                            "date_stop": j["date_stop"],
                            "date_start": j["date_start"],
                            "conversions": conversions
                        }
                        conversions_list += [conver_data]
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["ctr"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    ctr_list.append(j)

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["cpc"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    cpc_list.append(j)

            if len(conversions_list) >= len(clicks_list):
                len_difference = len(conversions_list) - len(clicks_list)
                for i in range(len_difference):
                    clicks_list += [
                        {
                            "country": conversions_list[-1].get("country"),
                            "clicks": 0,
                            "date_start": conversions_list[-1].get("date_start"),
                            "date_stop": conversions_list[-1].get("date_stop")
                        }
                    ]
            else:
                len_difference = len(clicks_list) - len(conversions_list)
                for i in range(len_difference):
                    conversions_list += [
                        {
                            "country": clicks_list[-1].get("country"),
                            "conversions": 0,
                            "date_start": clicks_list[-1].get("date_start"),
                            "date_stop": clicks_list[-1].get("date_stop")
                        }
                    ]
            for l in range(len(conversions_list)):
                if conversions_list[l].get("date_start") == clicks_list[l].get("date_start") and conversions_list[l].get("country") == clicks_list:
                    cvr = '%0.2f' % (int(conversions_list[l].get("conversions")) / int(clicks_list[l].get("clicks")) * 100) if int(clicks_list[l].get("clicks")) != 0 else 0
                    cvr_list += [
                        {
                            "country": conversions_list[l].get("country"),
                            "cvr": cvr,
                            "date_start": conversions_list[l].get("date_start"),
                            "date_stop": conversions_list[l].get("date_stop")
                        }
                    ]
                else:
                    cvr_list += [
                        {
                            "country": conversions_list[l].get("country"),
                            "cvr": 0,
                            "date_start": conversions_list[l].get("date_start"),
                            "date_stop": conversions_list[l].get("date_stop")
                        }
                    ]
            if len(conversions_list) > len(cost_list):
                len_difference = len(conversions_list) - len(cost_list)
                for i in range(len_difference):
                    cost_list += [
                        {
                            "country": conversions_list[-1].get("country"),
                            "spend": 0,
                            "date_start": conversions_list[-1].get("date_start"),
                            "date_stop": conversions_list[-1].get("date_stop")
                        }
                    ]
            else:
                len_difference = len(cost_list) - len(conversions_list)
                for i in range(len_difference):
                    conversions_list += [
                        {
                            "country": cost_list[-1].get("country"),
                            "conversions": 0,
                            "date_start": cost_list[-1].get("date_start"),
                            "date_stop": cost_list[-1].get("date_stop")
                        }
                    ]

            for l in range(len(conversions_list)):
                if conversions_list[l].get("date_start") == cost_list[l].get("date_start") and conversions_list[l].get("country") == cost_list[l].get("country"):
                    cpi = '%0.2f' % (float(cost_list[l].get("spend")) / float(conversions_list[l].get("conversions")) * 100) if conversions_list[l].get("conversions") != 0 else 0
                    cpi_dict = {
                        "country": conversions_list[l].get("country"),
                        "cpi": cpi,
                        "date_start": conversions_list[l].get("date_start"),
                        "date_stop": conversions_list[l].get("date_stop")
                    }

                else:
                    cpi_dict = {
                        "country": conversions_list[l].get("country"),
                        "cpi": 0,
                        "date_start": conversions_list[l].get("date_start"),
                        "date_stop": conversions_list[l].get("date_stop")
                    }
                cpi_list += [cpi_dict]

            for r in range(len(conversions_list)):
                country = conversions_list[r].get("country")
                date = conversions_list[r].get("date_start")
                conversion = float(conversions_list[r].get("conversions"))
                countries = Country.query.filter_by(shorthand=country).first()
                country_id = countries.id
                time_price = TimePrice.query.filter_by(country_id=country_id,date=date).first()
                if time_price:
                    price = time_price.price
                else:
                    price = price_default
                revenue_list += [
                    {
                        "country": country,
                        "revenue": float(conversion*price),
                        "date_start": date,
                        "date_stop": date
                    }
                ]

            # profit = revenue - count_cost
            for p in range(len(revenue_list)):
                if revenue_list[p].get("country") == cost_list[p].get("country") and revenue_list[p].get("date_start") == cost_list[p].get("date_start"):
                    profit = {
                        "country": revenue_list[p].get("country"),
                        "profit": float(revenue_list[p].get("revenue"))-float(cost_list[p].get("spend")),
                        "date_start": revenue_list[p].get("date_start"),
                        "date_stop": revenue_list[p].get("date_stop")
                    }

                else:
                    profit = {
                        "country": revenue_list[p].get("country"),
                        "profit": 0,
                        "date_start": revenue_list[p].get("date_start"),
                        "date_stop": revenue_list[p].get("date_stop")
                    }
                profit_list += [profit]

            data_geo_table = {
                "impressions_list": impressions_list,
                "cost_list": cost_list,
                "clicks_list": clicks_list,
                "conversions_list":conversions_list,
                "ctr_list": ctr_list,
                "cvr_list": cvr_list,
                "cpc_list": cpc_list,
                "cpi_list": cpi_list,
                "revenue_list": revenue_list,
                "profit_list": profit_list,
                "head": ["Date","Geo","Revenue","Profit","Cost","Impressions","Clicks","Conversions","CTR","CVR","CPC","CPA"]
            }
            data_date_table = {}

        elif "date" in dimension:
            data_geo_table = {}
            impressions_count = []
            costs_count = []
            clicks_count = []
            ctr_count = []
            cpc_count = []
            conversions_list = []
            cost_list = []
            revenue_list = []
            profit_list = []
            conversions_count_list = []

            for i in advertise_groups:
                url = "https://graph.facebook.com/v2.8/" + str(i) + "/insights"
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["actions"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    actions = j.get("actions", [])
                    for action in actions:
                        if "offsite_conversion" in action["action_type"]:
                            conversions = int(action["value"])
                        elif "link_click" in action["action_type"]:
                            conversions = int(action["value"])
                        else:
                            conversions = 0
                        conver_data = {
                            "country": j["country"],
                            "date_stop": j["date_stop"],
                            "date_start": j["date_start"],
                            "conversions": conversions
                        }
                        conversions_list += [conver_data]
                for r in range(len(conversions_list)):
                    country = conversions_list[r].get("country")
                    date = conversions_list[r].get("date_start")
                    conversion = float(conversions_list[r].get("conversions"))
                    countries = Country.query.filter_by(shorthand=country).first()
                    country_id = countries.id
                    time_price = TimePrice.query.filter_by(country_id=country_id, date=date).first()
                    if time_price:
                        price = time_price.price
                    else:
                        price = price_default
                    revenue_list += [
                        {
                            "country": country,
                            "revenue": float(conversion * price),
                            "date_start": date,
                            "date_stop": date
                        }
                    ]

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["spend"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    cost_list.append(j)

                if len(revenue_list) >= len(cost_list):
                    len_difference = len(revenue_list) - len(cost_list)
                    for le in range(len_difference):
                        cost_list += [{
                            "country": revenue_list[-1].get("country"),
                            "spend": 0,
                            "date_start": revenue_list[-1].get("date_start"),
                            "date_stop": revenue_list[-1].get("date_stop")
                        }]
                else:
                    len_difference = len(cost_list) - len(revenue_list)
                    for le in range(len_difference):
                        revenue_list += [{
                            "country": cost_list[-1].get("country"),
                            "spend": 0,
                            "date_start": cost_list[-1].get("date_start"),
                            "date_stop": cost_list[-1].get("date_stop")
                        }]

                for r in range(len(revenue_list)):
                    if revenue_list[r].get("date_start") == cost_list[r].get("date_start"):
                        profit_list += [
                            {
                                "profit": float(revenue_list[r].get("revenue"))-float(cost_list[r].get("spend")),
                                "date_start": revenue_list[r].get("date_start")
                            }
                        ]
                    else:
                        profit_list += [
                            {
                                "profit": 0,
                                "date_start": revenue_list[r].get("date_start")
                            }
                        ]


            for t in time_ranges:
                for i in advertise_groups:
                    url = "https://graph.facebook.com/v2.8/" + str(i) + "/insights"
                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["impressions"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()
                    if data != []:
                        impressions_count.append(data)

                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["spend"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url,params=params)
                    data = result.json()
                    if data != []:
                        costs_count.append(data)

                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["clicks"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()
                    if data != []:
                        clicks_count.append(data)

                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["ctr"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()
                    if data != []:
                        ctr_count.append(data)

                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["cpc"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()
                    if data != []:
                        cpc_count.append(data)

                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["actions"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()
                    if data["actions"] != []:
                        for action in data["actions"]:
                            if "offsite_conversion" in action["action_type"]:
                                conversions = action["value"]
                                date_start = action["date_start"]
                                con_data = {
                                    "conversions": int(conversions),
                                    "date_start": date_start
                                }
                            elif "link_click" in action["action_type"]:
                                conversions = action["value"]
                                date_start = action["date_start"]
                                con_data = {
                                    "conversions": int(conversions),
                                    "date_start": date_start
                                }
                            conversions_count_list += [con_data]

            impressions_count_list = []
            costs_count_list = []
            clicks_count_list = []
            cpc_count_list = []
            ctr_count_list = []
            cvr_count_list = []
            cpi_count_list = []
            for t_impression in impressions_count:
                if t_impression["data"] != []:
                    impression_data = {
                        "impressions":t_impression["data"][0].get("impressions"),
                        "date_start": t_impression["data"][0].get("date_start")
                    }
                    impressions_count_list+=[impression_data]

            for t_cost in costs_count:
                if t_cost["data"] != []:
                    costs_data = {
                        "spend": float(t_cost["data"][0].get("spend")),
                        "date_start": t_cost["data"][0].get("date_start")
                    }
                    costs_count_list += [costs_data]

            for t_clicks in clicks_count:
                if t_clicks["data"] != []:
                    clicks_data = {
                        "clicks": int(t_clicks["data"][0].get("clicks")),
                        "date_start": t_clicks["data"][0].get("date_start")
                    }
                clicks_count_list += [clicks_data]

            for t_cpc in cpc_count:
                if t_cpc["data"] != []:
                    cpc_data = {
                        "cpc": t_cpc["data"][0].get("cpc"),
                        "date_start": t_cpc["data"][0].get("date_start")
                    }
                cpc_count_list += [cpc_data]

            for t_ctr in ctr_count:
                if t_ctr["data"] != []:
                    ctr_data = {
                        "ctr": t_ctr["data"][0].get("ctr"),
                        "date_start": t_ctr["data"][0].get("date_start ")
                    }
                ctr_count_list += [ctr_data]

            if len(conversions_count_list) >= len(clicks_count_list):
                len_difference = len(conversions_count_list)-len(clicks_count_list)
                for i in range(len_difference):
                    clicks_count_list += [
                        {
                            "clicks": 0,
                            "date_start": conversions_count_list[-1].get("date_start")
                        }
                    ]
            else:
                len_difference = len(clicks_count_list)-len(conversions_count_list)
                for i in range(len_difference):
                    conversions_count_list += [
                        {
                            "conversions": 0,
                            "date_start": clicks_count_list[-1].get("date_start")
                        }
                    ]
            for l in range(len(conversions_count_list)):
                if conversions_count_list[l].get("date_start") == clicks_count_list[l].get("date_start"):
                    cvr = '%0.2f' % (conversions_count_list[l].get("conversions") / clicks_count_list[l].get("clicks") * 100) if clicks_count_list[l].get("clicks") !=0 else 0
                    cvr_count_list += [
                        {
                            "cvr": cvr,
                            "date_start": conversions_count_list[l].get("date_start")
                        }
                    ]
                else:
                    cvr_count_list += [
                        {
                            "cvr": 0,
                            "date_start": conversions_count_list[l].get("date_start")
                        }
                    ]

            if len(conversions_count_list) > len(costs_count_list):
                len_difference = len(conversions_count_list) - len(costs_count_list)
                for i in range(len_difference):
                    costs_count_list += [
                        {
                            "spend": 0,
                            "date_start": conversions_count_list[-1].get("date_start")
                        }
                    ]
            else:
                len_difference = len(costs_count_list) - len(conversions_count_list)
                for i in range(len_difference):
                    conversions_count_list += [
                        {
                            "conversions": 0,
                            "date_start": costs_count_list[-1].get("date_start")
                        }
                    ]

            for l in range(len(conversions_count_list)):
                if conversions_count_list[l].get("date_start") == costs_count_list[l].get("date_start"):
                    cpi = '%0.2f' % (costs_count_list[l].get("spend") / float(conversions_count_list[l].get("conversions")) * 100) if conversions_count_list[l].get("conversions") !=0 else 0
                    cpi_count_list += [
                        {
                            "cpi": cpi,
                            "date_start": conversions_count_list[l].get("date_start")
                        }
                    ]
                else:
                    cpi_count_list += [
                        {
                            "cpi": 0,
                            "date_start": conversions_count_list[l].get("date_start")
                        }
                    ]

            data_date_table = {
                "impressions_list": impressions_count_list,
                "cost_list": costs_count_list,
                "clicks_list": clicks_count_list,
                "conversions_list":conversions_count_list,
                "ctr_list": ctr_count_list,
                "cvr_list": cvr_count_list,
                "cpc_list": cpc_count_list,
                "cpi_list": cpi_count_list,
                "revenue_list": revenue_list,
                "profit_list": [],
                "head": ["Date","Revenue","Profit","Cost","Impressions","Clicks","Conversions","CTR","CVR","CPC","CPA"]
            }
            data_geo_table ={}

            # impressions_count_list = [{"impressions":"400","date_start":"2016-09-08"},{"impressions":"500","date_start":"2016-09-08"},{"impressions":"300","date_start":"2016-09-09"}]



        return json.dumps({
            "code": 200,
            "data_geo": data_geo,
            "data_day": data_day,
            "data_geo_table": data_geo_table,
            "data_date_table": data_date_table,
            "message": "success"
        })