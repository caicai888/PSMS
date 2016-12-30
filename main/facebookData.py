# -*- coding: utf-8 -*-
from __future__ import division
from main.has_permission import *
from flask import Blueprint, request
from main import db
from models import Offer, Token, Advertisers
import json
import os
import datetime, time
import requests

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
        if dimension == "geo":
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
        elif dimension == "date":
            #按着day维护的总数据
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

        if dimension == "geo":
            impressions_list = []
            cost_list = []
            clicks_list = []
            conversions_list = []
            ctr_list = []
            cpc_list = []
            cvr_list = []
            cpi_list = [],
            revenue_list = [],
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
            # count_cvr = '%0.2f' % (count_conversions / count_clicks * 100) if count_clicks != 0 else 0
            # count_cpi = '%0.2f'% (count_cost / count_conversions)
            # revenue = count_conversions * 1.5
            # profit = revenue - count_cost
            cpi_list = [
                {
                    "country": "ES",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "cpi": 0
                },
                {
                    "country": "GR",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "cpi": 0.13
                },
                {
                    "country": "ES",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "cpi": 0
                },
                {
                    "country": "AR",
                    "date_stop": "2016-09-07",
                    "date_start": "2016-09-07",
                    "cpi": 0.004
                },
                {
                    "country": "AR",
                    "date_stop": "2016-09-06",
                    "date_start": "2016-09-06",
                    "cpi": 0.004
                },
                {
                    "country": "AI",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.07
                },
                {
                    "country": "AR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.003
                },
                {
                    "country": "BD",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.06
                },
                {
                    "country": "CK",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.01
                },
                {
                    "country": "CV",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.02
                },
                {
                    "country": "FM",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0
                },
                {
                    "country": "KG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.04
                },
                {
                    "country": "LR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.08
                },
                {
                    "country": "LY",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.03
                },
                {
                    "country": "MF",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0
                },
                {
                    "country": "MR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.04
                },
                {
                    "country": "NA",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.05
                },
                {
                    "country": "RS",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.22
                },
                {
                    "country": "SC",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.08
                },
                {
                    "country": "TG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.09
                },
                {
                    "country": "TM",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0
                },
                {
                    "country": "TN",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.04
                },
                {
                    "country": "UG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.11
                },
                {
                    "country": "YE",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cpi": 0.02
                },
                {
                    "country": "AI",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04",
                    "cpi": 0.02
                },
                {
                    "country": "BD",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04",
                    "cpi": 0.07
                },
                {
                    "country": "CK",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04",
                    "cpi": 0
                },
                {
                    "country": "CV",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04",
                    "cpi": 0.12
                }
            ]
            conversions_list = [
                {
                    "country": "ES",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "conversions": 6
                },
                {
                    "country": "GR",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "conversions": "17"
                },
                {
                    "conversions": 0,
                    "country": "ES",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08"
                },
                {
                    "conversions": 1628,
                    "country": "AR",
                    "date_stop": "2016-09-07",
                    "date_start": "2016-09-07"
                },
                {
                    "conversions": 2050,
                    "country": "AR",
                    "date_stop": "2016-09-06",
                    "date_start": "2016-09-06"
                },
                {
                    "conversions": 1,
                    "country": "AI",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 1348,
                    "country": "AR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 35,
                    "country": "BD",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 1,
                    "country": "CK",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 6,
                    "country": "CV",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 6,
                    "country": "KG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 4,
                    "country": "LR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 12,
                    "country": "LY",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 5,
                    "country": "MR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 14,
                    "country": "NA",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 1,
                    "country": "RS",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 2,
                    "country": "TG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 27,
                    "country": "TN",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 3,
                    "country": "UG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 6,
                    "country": "YE",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "conversions": 7,
                    "country": "AI",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04"
                },
                {
                    "conversions": 36,
                    "country": "BD",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04"
                },
                {
                    "conversions": 1,
                    "country": "CV",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04"
                },
            ]
            revenue_list = [
                {
                    "country": "ES",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "revenue": 9
                },
                {
                    "country": "GR",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "revenue": 25.5
                },
                {
                    "revenue": 0,
                    "country": "ES",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08"
                },
                {
                    "revenue": 3672,
                    "country": "AR",
                    "date_stop": "2016-09-07",
                    "date_start": "2016-09-07"
                },
                {
                    "revenue": 3075,
                    "country": "AR",
                    "date_stop": "2016-09-06",
                    "date_start": "2016-09-06"
                },
                {
                    "revenue": 1.5,
                    "country": "AI",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 2022,
                    "country": "AR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 52.5,
                    "country": "BD",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 1.5,
                    "country": "CK",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 9,
                    "country": "CV",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 9,
                    "country": "KG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 6,
                    "country": "LR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 18,
                    "country": "LY",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 7.5,
                    "country": "MR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 21,
                    "country": "NA",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 1.5,
                    "country": "RS",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 3,
                    "country": "TG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 40.5,
                    "country": "TN",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 4.5,
                    "country": "UG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 9,
                    "country": "YE",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "revenue": 10.5,
                    "country": "AI",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04"
                },
                {
                    "revenue": 54,
                    "country": "BD",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04"
                },
                {
                    "revenue": 1.5,
                    "country": "CV",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04"
                },
            ]
            profit_list = [
                {
                    "country": "ES",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "profit": 9
                },
                {
                    "country": "GR",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "profit": 25.5
                },
                {
                    "profit": 0,
                    "country": "ES",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08"
                },
                {
                    "profit": 3672,
                    "country": "AR",
                    "date_stop": "2016-09-07",
                    "date_start": "2016-09-07"
                },
                {
                    "profit": 3075,
                    "country": "AR",
                    "date_stop": "2016-09-06",
                    "date_start": "2016-09-06"
                },
                {
                    "profit": 1.5,
                    "country": "AI",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 2022,
                    "country": "AR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 52.5,
                    "country": "BD",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 1.5,
                    "country": "CK",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 9,
                    "country": "CV",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 9,
                    "country": "KG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 6,
                    "country": "LR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 18,
                    "country": "LY",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 7.5,
                    "country": "MR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 21,
                    "country": "NA",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 1.5,
                    "country": "RS",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 3,
                    "country": "TG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 40.5,
                    "country": "TN",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 4.5,
                    "country": "UG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 9,
                    "country": "YE",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05"
                },
                {
                    "profit": 10.5,
                    "country": "AI",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04"
                },
                {
                    "profit": 54,
                    "country": "BD",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04"
                },
                {
                    "profit": 1.5,
                    "country": "CV",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04"
                },
            ]
            cvr_list = [
                {
                    "country": "ES",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "cvr": "0"
                },
                {
                    "country": "GR",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "cvr": "24"
                },
                {
                    "country": "ES",
                    "date_stop": "2016-09-08",
                    "date_start": "2016-09-08",
                    "cvr": "10"
                },
                {
                    "country": "AR",
                    "date_stop": "2016-09-07",
                    "date_start": "2016-09-07",
                    "cvr": "1648"
                },
                {
                    "country": "AR",
                    "date_stop": "2016-09-06",
                    "date_start": "2016-09-06",
                    "cvr": "2085"
                },
                {
                    "country": "AI",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "1"
                },
                {
                    "country": "AR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "1367"
                },
                {
                    "country": "BD",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "64"
                },
                {
                    "country": "CK",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "1"
                },
                {
                    "country": "CV",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "8"
                },
                {
                    "country": "FM",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "0"
                },
                {
                    "country": "KG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "6"
                },
                {
                    "country": "LR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "7"
                },
                {
                    "country": "LY",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "19"
                },
                {
                    "country": "MF",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "0"
                },
                {
                    "country": "MR",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "6"
                },
                {
                    "country": "NA",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "16"
                },
                {
                    "country": "RS",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "3"
                },
                {
                    "country": "SC",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "0"
                },
                {
                    "country": "TG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "3"
                },
                {
                    "country": "TM",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "0"
                },
                {
                    "country": "TN",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "44"
                },
                {
                    "country": "UG",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "3"
                },
                {
                    "country": "YE",
                    "date_stop": "2016-09-05",
                    "date_start": "2016-09-05",
                    "cvr": "11"
                },
                {
                    "country": "AI",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04",
                    "cvr": "7"
                },
                {
                    "country": "BD",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04",
                    "cvr": "63"
                },
                {
                    "country": "CK",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04",
                    "cvr": "0"
                },
                {
                    "country": "CV",
                    "date_stop": "2016-09-04",
                    "date_start": "2016-09-04",
                    "cvr": "2"
                }
            ]
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

        return json.dumps({
            "data_geo": data_geo,
            "data_day": data_day,
            "data_geo_table": data_geo_table
        })