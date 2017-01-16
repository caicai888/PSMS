# -*- coding: utf-8 -*-
from __future__ import division
from main.has_permission import *
from flask import Blueprint, request
from main import db
from models import Offer, Token, Advertisers, TimePrice, Country, History
import json
import os
import datetime, time
import requests

facebookDate = Blueprint('facebookDate', __name__)

@facebookDate.route('/api/dashboard')
def dashboard():
    yesterday = (datetime.datetime.now()-datetime.timedelta(hours=24)).strftime("%Y-%m-%d")
    token = Token.query.filter().first()
    accessToken = token.accessToken
    time_range = "{'since': "+"'"+str(yesterday)+"'"+", 'until': "+"'"+str(yesterday)+"'"+"}"

    advertisers = Advertisers.query.filter(Advertisers.type=="facebook").all()
    advertisers_group = []
    for i in advertisers:
        advertise_group = i.advertise_series
        offer_id = i.offer_id

        for j in advertise_group.split(','):
            group_result = {
                "offer_id": offer_id,
                "account": j
            }
            advertisers_group += [group_result]

    impressions_count = 0
    conversions_count = 0
    spend_count = 0
    clicks_count = 0
    cpc_count = 0
    ctr_count = 0
    revenue_count = 0

    for ad in advertisers_group:
        try:
            url = "https://graph.facebook.com/v2.8/"+str(ad["account"])+"/insights"
            params_impressions = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["impressions"],
                "time_range": str(time_range)
            }
            result_impressions = requests.get(url=url, params=params_impressions)
            data_impressions = result_impressions.json()["data"]
            for i in data_impressions:
                impressions_count += int(i["impressions"])

            params_conversions = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["actions"],
                "time_range": str(time_range)
            }
            result_conversions = requests.get(url=url, params=params_conversions)
            data_conversions = result_conversions.json()["data"]
            if data_conversions != []:
                for j in data_conversions:
                    actions = j.get("actions", [])
                    for action in actions:
                        if "mobile_app_install" in action["action_type"]:
                            conversions = action["value"]
                        else:
                            conversions = 0
                        conversions_count += int(conversions)

            params_spend = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["spend"],
                "time_range": str(time_range)
            }
            result_spend = requests.get(url=url, params=params_spend)
            data_spend = result_spend.json()["data"]
            for i in data_spend:
                spend_count += float(i["spend"])

            params_clicks = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["clicks"],
                "time_range": str(time_range)
            }
            result_clicks = requests.get(url=url, params=params_clicks)
            data_clicks = result_clicks.json()["data"]
            for i in data_clicks:
                clicks_count += int(i["clicks"])

            params_cpc = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["cpc"],
                "time_range": str(time_range)
            }
            result_cpc = requests.get(url=url, params=params_cpc)
            data_cpc = result_cpc.json()["data"]
            for i in data_cpc:
                cpc_count += float(i["cpc"])

            params_ctr = {
                "access_token": accessToken,
                "level": "campaign",
                "fields": ["ctr"],
                "time_range": str(time_range)
            }
            result_ctr = requests.get(url=url, params=params_ctr)
            data_ctr = result_ctr.json()["data"]
            for i in data_ctr:
                ctr_count += float(i["ctr"])

            offer = Offer.query.filter_by(id=int(ad["offer_id"])).first()
            contract_type = offer.contract_type
            if contract_type == "1":
                contract_scale = float(offer.contract_scale)
                params_spend = {
                    "access_token": accessToken,
                    "level": "campaign",
                    "fields": ["spend"],
                    "time_range": str(time_range)
                }
                result_spend = requests.get(url=url, params=params_spend)
                data_spend = result_spend.json()["data"]
                for i in data_spend:
                    revenue_count += float(i["spend"])*(1+contract_scale/100)
            else:
                params_revenue = {
                    "access_token": accessToken,
                    "level": "campaign",
                    "fields": ["actions"],
                    "breakdowns": ["country"],
                    "time_range": str(time_range)
                }
                result_revenue = requests.get(url=url, params=params_revenue)
                data_revenue = result_revenue.json()["data"]
                if data_revenue != []:
                    for action in data_revenue:
                        country = action["country"]
                        date = action["date_start"]
                        countries = Country.query.filter_by(shorthand=country).first()
                        country_id = countries.id
                        startTime = offer.startTime
                        prices = TimePrice.query.filter(TimePrice.country_id==country_id,TimePrice.offer_id == int(ad["offer_id"]),TimePrice.date <= date,TimePrice.date>=startTime).order_by(TimePrice.date.desc()).first()
                        if not prices:
                            prices_history = History.query.filter(History.country==country, History.offer_id==ad["offer_id"]).order_by(History.createdTime.desc()).first()
                            if not prices_history:
                                price = offer.price
                            else:
                                price = prices_history.price
                        else:
                            price = prices.price
                        actions = action.get("actions", [])
                        for j in actions:
                            if "mobile_app_install" in j["action_type"]:
                                conversions_revenue = float(j["value"])
                            else:
                                conversions_revenue = 0
                            revenue_count += (conversions_revenue * float(price))
        except Exception as e:
            print e
            impressions_count = 0
            conversions_count = 0
            spend_count = 0
            clicks_count = 0
            cpc_count = 0
            ctr_count = 0
            revenue_count = 0

    if float(conversions_count) != 0:
        cpi = '%0.2f' % ((float(spend_count)) / float(conversions_count))
    else:
        cpi = 0
    if float(clicks_count) != 0:
        cvr = '%0.2f' %(float(conversions_count)/float(clicks_count)*100)
    else:
        cvr = 0
    result = {
        "impressions": str(impressions_count),
        "spend": '%0.2f'%(float(spend_count)),
        "clicks": str(clicks_count),
        "conversions": str(conversions_count),
        "cpc": '%0.2f'%(float(cpc_count)),
        "ctr": '%0.2f'%(float(ctr_count)),
        "cpi": str(cpi),
        "cvr": str(cvr),
        "revenue": '%0.2f'%(revenue_count),
        "profit": '%0.2f'%(float(revenue_count)-float(spend_count))
    }
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
        offerId = int(data["offer_id"])
        start_date = data["start_date"]
        end_date = data["end_date"]
        dimension = data["dimension"]

        offer = Offer.query.filter_by(id=offerId).first()
        price_default = offer.price
        contract_type = offer.contract_type
        contract_scale = offer.contract_scale

        advertiser = Advertisers.query.filter_by(offer_id=int(offerId),type="facebook").first()
        if not advertiser:
            return json.dumps({
                "code":500,
                "message":"not bind ads",
                "data_geo": {},
                "data_geo_table": {},
                "data_date_table": {},
                "data_range": {},
            })
        accessToken = advertiser.token
        accessToken = "EAAHgEYXO0BABAFXOL9QQ8GNPhLi5eC04UKySrmkpgdLy9MrZBIczE8xsD4uxfLCmZAZBaFuyGuZB3ZAyRATxrsAPOZCwr5OZBYQcjcr3cHZCJUUzvvB2oABEGmO2EuZAyYlPq1OZCcwdZBcOi7SgoD60XFSMN7ZCYwbngOVDqYmRoUb16wZDZD"
        advertise_groups = advertiser.advertise_series.split(",")
        count_impressions = 0
        count_cost = 0
        count_clicks = 0
        count_conversions = 0
        count_ctr = 0
        count_cpc = 0
        if advertise_groups == []:
            return json.dumps({
                "code": 500,
                "message": "not bind data!"
            })
        else:
            try:
                if "geo" in dimension:
                    for i in advertise_groups:
                        url = "https://graph.facebook.com/v2.8/"+str(i)+"/insights"
                        params = {
                            "access_token": accessToken,
                            "level": "campaign",
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
                            "level": "campaign",
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
                            "level": "campaign",
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
                            "level": "campaign",
                            "fields": ["actions"],
                            "breakdowns": ["country"],
                            "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                        }
                        result = requests.get(url=url, params=params)
                        data = result.json()["data"]
                        for j in data:
                            actions = j.get("actions",[])
                            for action in actions:
                                if "mobile_app_install" in action["action_type"]:
                                    conversions = action["value"]
                                    count_conversions += int(conversions)
                                else:
                                    conversions = 0
                                    count_conversions += conversions
                        params = {
                            "access_token": accessToken,
                            "level": "campaign",
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
                            "level": "campaign",
                            "fields": ["cpc"],
                            "breakdowns": ["country"],
                            "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                        }
                        result = requests.get(url=url, params=params)
                        data = result.json()["data"]
                        for j in data:
                            count_cpc += float(j["cpc"])
                    count_cvr = '%0.2f' % (count_conversions / count_clicks * 100) if count_clicks != 0 else 0
                    count_cpi = '%0.2f'% (count_cost / count_conversions) if count_conversions != 0 else 0
                    revenue = 0
                    profit = 0
                    data_geo = {
                        "count_impressions": str(count_impressions),
                        "count_cost": '%0.2f'%(count_cost),
                        "count_clicks": str(count_clicks),
                        "count_conversions": str(count_conversions),
                        "count_ctr": '%0.2f'%(float(count_ctr)),
                        "count_cvr": count_cvr,
                        "count_cpc": '%0.2f'% (float(count_cpc)),
                        "count_cpi": count_cpi,
                        "revenue": '%0.2f'%(revenue),
                        "profit": '%0.2f'%(profit)
                    }
                elif "date" in dimension and len(dimension)==1:
                    #按着day维度的总数据
                    for i in advertise_groups:
                        url = "https://graph.facebook.com/v2.8/"+str(i)+"/insights"
                        params = {
                            "access_token": accessToken,
                            "level": "campaign",
                            "fields": ["impressions"],
                            "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                        }
                        result = requests.get(url=url, params=params)
                        data = result.json()["data"]
                        for j in data:
                            count_impressions += int(j["impressions"])

                        params = {
                            "access_token": accessToken,
                            "level": "campaign",
                            "fields": ["spend"],
                            "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                        }
                        result = requests.get(url=url, params=params)
                        data = result.json()["data"]
                        for j in data:
                            count_cost += float(j["spend"])

                        params = {
                            "access_token": accessToken,
                            "level": "campaign",
                            "fields": ["clicks"],
                            "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                        }
                        result = requests.get(url=url, params=params)
                        data = result.json()["data"]
                        for j in data:
                            count_clicks += float(j["clicks"])

                        params = {
                            "access_token": accessToken,
                            "level": "campaign",
                            "fields": ["actions"],
                            "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                        }
                        result = requests.get(url=url, params=params)
                        data = result.json()["data"]
                        for j in data:
                            actions = j.get("actions",[])
                            for action in actions:
                                if "mobile_app_install" in action["action_type"]:
                                    conversions = action["value"]
                                    count_conversions += int(conversions)
                                else:
                                    conversions = 0
                                    count_conversions += conversions
                        params = {
                            "access_token": accessToken,
                            "level": "campaign",
                            "fields": ["ctr"],
                            "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                        }
                        result = requests.get(url=url, params=params)
                        data = result.json()["data"]
                        for j in data:
                            count_ctr += float(j["ctr"])

                        params = {
                            "access_token": accessToken,
                            "level": "campaign",
                            "fields": ["cpc"],
                            "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                        }
                        result = requests.get(url=url, params=params)
                        data = result.json()["data"]
                        for j in data:
                            count_cpc += float(j["cpc"])
                    count_cvr = '%0.2f' % (count_conversions / count_clicks * 100) if count_clicks != 0 else 0
                    count_cpi = '%0.2f'% (count_cost / count_conversions) if count_conversions != 0 else 0
                    revenue = 0
                    profit = 0
                    data_geo = {
                        "count_impressions": str(count_impressions),
                        "count_cost": '%0.2f'%(count_cost),
                        "count_clicks": str(count_clicks),
                        "count_conversions": str(count_conversions),
                        "count_ctr": '%0.2f'%(count_ctr),
                        "count_cvr": count_cvr,
                        "count_cpc": '%0.2f'%(count_cpc),
                        "count_cpi": count_cpi,
                        "revenue": '%0.2f'%(revenue),
                        "profit": '%0.2f'%(profit)
                    }


                all_date = []
                date1 = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                date2 = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                date_timelta = datetime.timedelta(days=1)
                all_date.append(start_date)
                while date_timelta < (date2-date1):
                    all_date.append((date1+date_timelta).strftime("%Y-%m-%d"))
                    date_timelta += datetime.timedelta(days=1)
                all_date.append(end_date)

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
                            "level": "campaign",
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
                            "level": "campaign",
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
                            "level": "campaign",
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
                            "level": "campaign",
                            "fields": ["actions"],
                            "breakdowns": ["country"],
                            "time_ranges": str(time_ranges)
                        }
                        result = requests.get(url=url, params=params)
                        data = result.json()["data"]
                        for j in data:
                            actions = j.get("actions",[])
                            for action in actions:
                                if "mobile_app_install" in action["action_type"]:
                                    conversions = int(action["value"])

                            conver_data = {
                                "country": j["country"],
                                "date_stop": j["date_stop"],
                                "date_start": j["date_start"],
                                "conversions": conversions
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
                                "cpc": '%0.2f'%(float(j["cpc"])),
                                "country": j["country"],
                                "date_start": j["date_start"],
                                "date_stop": j["date_stop"]
                            }
                            cpc_list+=[data_cpc]

                    if len(conversions_list) >= len(clicks_list):
                        count = len(clicks_list)
                        len_difference = len(conversions_list) - len(clicks_list)
                        for i in range(len_difference):
                            clicks_list += [
                                {
                                    "country": conversions_list[count+i].get("country"),
                                    "clicks": 0,
                                    "date_start": conversions_list[count+i].get("date_start"),
                                    "date_stop": conversions_list[count+i].get("date_stop")
                                }
                            ]
                    else:
                        count = len(conversions_list)
                        len_difference = len(clicks_list) - len(conversions_list)
                        for i in range(len_difference):
                            conversions_list += [
                                {
                                    "country": clicks_list[count+i].get("country"),
                                    "conversions": 0,
                                    "date_start": clicks_list[count+i].get("date_start"),
                                    "date_stop": clicks_list[count+i].get("date_stop")
                                }
                            ]
                    for l in conversions_list:
                        date_start = l["date_start"]
                        for i in clicks_list:
                            if date_start == i["date_start"]:
                                cvr = '%0.2f' %(float(l["conversions"])/float(i["clicks"]) * 100) if float(i["clicks"]) != 0 else 0
                                cvr_list += [
                                    {
                                        "cvr": cvr,
                                        "date_start": date_start,
                                        "country": l["country"],
                                        "date_stop": date_start
                                    }
                                ]

                    for l in conversions_list:
                        date_start = l["date_start"]
                        for i in cost_list:
                            if date_start == i["date_start"]:
                                cpi = '%0.2f' %(float(i["spend"])/float(l["conversions"])) if float(l["conversions"]) != 0 else 0
                                cpi_list += [
                                    {
                                        "cpi": cpi,
                                        "date_start": date_start,
                                        "country": l["country"],
                                        "date_stop": date_start
                                    }
                                ]

                    if contract_type == "1":
                        for r in range(len(cost_list)):
                            country = cost_list[r].get("country")
                            date = cost_list[r].get("date_start")
                            cost = float(cost_list[r].get("spend"))
                            revenue_list += [
                                {
                                    "country": country,
                                    "revenue": '%0.2f'%(cost*(1+float(contract_scale)/100)),
                                    "date_start": date,
                                    "date_stop": date
                                }
                            ]

                    else:
                        for r in range(len(conversions_list)):
                            country = conversions_list[r].get("country")
                            date = conversions_list[r].get("date_start")
                            conversion = float(conversions_list[r].get("conversions"))
                            countries = Country.query.filter_by(shorthand=country).first()
                            country_id = countries.id
                            time_price = TimePrice.query.filter(TimePrice.country_id == country_id, TimePrice.offer_id == offerId, TimePrice.date <= date,TimePrice.date >= offer.startTime).order_by(TimePrice.date.desc()).first()
                            if time_price:
                                price = time_price.price
                            else:
                                prices_history = History.query.filter(History.country == country, History.offer_id == offerId).order_by(
                                    History.createdTime.desc()).first()
                                if not prices_history:
                                    price = price_default
                                else:
                                    price = prices_history.price

                            revenue_list += [
                                {
                                    "country": country,
                                    "revenue": float(conversion*price),
                                    "date_start": date,
                                    "date_stop": date
                                }
                            ]
                    print "&&&&" * 10
                    print revenue_list

                    for r in cost_list:
                        date_start = r["date_start"]
                        for j in revenue_list:
                            if date_start == j["date_start"]:
                                profit = '%0.2f' % (float(j["revenue"])-float(r["spend"]))
                                profit_list += [
                                    {
                                        "profit": profit,
                                        "date_start": date_start,
                                        "country": r["country"],
                                        "date_stop": date_start
                                    }
                                ]

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
                        ctr_range.append('%0.2f'%(float(i["ctr"])))

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
                        cpc_range.append('%0.2f'%(float(i["cpc"])))

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

                    data_range = {
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
                    count_revenue = 0
                    for a in revenue_list:
                        print "+++++++"*10
                        print a["revenue"]
                        count_revenue += float(a["revenue"])
                    data_geo["revenue"] = '%0.2f'%(count_revenue)
                    data_geo["profit"] = '%0.2f'%(float(count_revenue)-float(data_geo["count_cost"]))
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
                        "head": ["Date","Geo","Revenue","Profit","Cost","Impressions","Clicks","Conversions","CTR","CVR","CPC","CPI"]
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
                    revenue_new_list = []
                    profit_list = []
                    conversions_count_list = []

                    for i in advertise_groups:
                        url = "https://graph.facebook.com/v2.8/" + str(i) + "/insights"
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
                            for action in actions:
                                if "mobile_app_install" in action["action_type"]:
                                    conversions = int(action["value"])

                            conver_data = {
                                "country": j["country"],
                                "date_stop": j["date_stop"],
                                "date_start": j["date_start"],
                                "conversions": conversions
                            }
                            conversions_list += [conver_data]

                        if contract_type == "2":
                            for r in range(len(conversions_list)):
                                country = conversions_list[r].get("country")
                                date = conversions_list[r].get("date_start")
                                conversion = int(conversions_list[r].get("conversions"))
                                countries = Country.query.filter_by(shorthand=country).first()
                                country_id = countries.id
                                time_price = TimePrice.query.filter(TimePrice.country_id == country_id, TimePrice.offer_id == offerId,TimePrice.date <= date, TimePrice.date >= offer.startTime).order_by(TimePrice.date.desc()).first()
                                if time_price:
                                    price = time_price.price
                                else:
                                    prices_history = History.query.filter(History.country == country, History.offer_id == offerId).order_by(History.createdTime.desc()).first()
                                    if not prices_history:
                                        price = price_default
                                    else:
                                        price = prices_history.price

                                revenue_new_list += [
                                    {
                                        "country": country,
                                        "revenue": float(conversion * price),
                                        "date_start": date,
                                        "date_stop": date
                                    }
                                ]

                    for t in time_ranges:
                        for i in advertise_groups:
                            url = "https://graph.facebook.com/v2.8/" + str(i) + "/insights"
                            params = {
                                "access_token": accessToken,
                                "level": "campaign",
                                "fields": ["impressions"],
                                "time_range": str(t)
                            }
                            result = requests.get(url=url, params=params)
                            data = result.json()
                            if data != []:
                                impressions_count.append(data)

                            params = {
                                "access_token": accessToken,
                                "level": "campaign",
                                "fields": ["spend"],
                                "time_range": str(t)
                            }
                            result = requests.get(url=url,params=params)
                            data = result.json()
                            if data != []:
                                costs_count.append(data)

                            params = {
                                "access_token": accessToken,
                                "level": "campaign",
                                "fields": ["clicks"],
                                "time_range": str(t)
                            }
                            result = requests.get(url=url, params=params)
                            data = result.json()
                            if data != []:
                                clicks_count.append(data)

                            params = {
                                "access_token": accessToken,
                                "level": "campaign",
                                "fields": ["ctr"],
                                "time_range": str(t)
                            }
                            result = requests.get(url=url, params=params)
                            data = result.json()
                            if data != []:
                                ctr_count.append(data)

                            params = {
                                "access_token": accessToken,
                                "level": "campaign",
                                "fields": ["cpc"],
                                "time_range": str(t)
                            }
                            result = requests.get(url=url, params=params)
                            data = result.json()
                            if data != []:
                                cpc_count.append(data)

                            params = {
                                "access_token": accessToken,
                                "level": "campaign",
                                "fields": ["actions"],
                                "time_range": str(t)
                            }
                            result = requests.get(url=url, params=params)
                            data = result.json()["data"]

                            if data != []:
                                if data[0]["actions"] != []:
                                    for action in data[0]["actions"]:
                                        if "mobile_app_install" in action["action_type"]:
                                            conversions = action["value"]
                                            date_start = data[0]["date_start"]
                                            con_data = {
                                                "conversions": int(conversions),
                                                "date_start": date_start
                                            }

                                        else:
                                            conversions = 0
                                            date_start = data[0]["date_start"]
                                            con_data = {
                                                "conversions": int(conversions),
                                                "date_start": date_start
                                            }
                                        conversions_count_list += [con_data]
                    dx = dict()
                    for i in conversions_count_list:
                        dx.setdefault(i["date_start"], []).append(i["conversions"])
                    for k in dx:
                        dx[k] = sum(int(i) for i in dx[k])
                    conversions_count_list = [{"date_start": k, "conversions": str(v)} for k, v in dx.items()]
                    conversions_count_list = sorted(conversions_count_list, key=lambda k: k['date_start'])[::-1]

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
                    dx = dict()
                    for i in impressions_count_list:
                        dx.setdefault(i["date_start"], []).append(i["impressions"])
                    for k in dx:
                        dx[k] = sum(float(i) for i in dx[k])
                    impressions_count_list = [{"date_start": k, "impressions": str(v)} for k, v in dx.items()]
                    impressions_count_list = sorted(impressions_count_list, key=lambda k: k['date_start'])[::-1]

                    for t_cost in costs_count:
                        if t_cost["data"] != []:
                            costs_data = {
                                "spend": float(t_cost["data"][0].get("spend")),
                                "date_start": t_cost["data"][0].get("date_start")
                            }
                            costs_count_list += [costs_data]
                    dx = dict()
                    for i in costs_count_list:
                        dx.setdefault(i["date_start"], []).append(i["spend"])
                    for k in dx:
                        dx[k] = sum(float(i) for i in dx[k])
                    costs_count_list = [{"date_start": k, "spend": str(v)} for k, v in dx.items()]
                    costs_count_list = sorted(costs_count_list, key=lambda k: k['date_start'])[::-1]
                    if contract_type == "1":
                        for r in range(len(costs_count_list)):
                            revenue_new_list += [
                                {
                                    "revenue": '%0.2f'%(float(costs_count_list[r].get("spend"))*(1+float(contract_scale)/100)),
                                    "date_start": costs_count_list[r].get("date_start"),
                                }
                            ]

                    for t_clicks in clicks_count:
                        if t_clicks["data"] != []:
                            clicks_data = {
                                "clicks": int(t_clicks["data"][0].get("clicks")),
                                "date_start": t_clicks["data"][0].get("date_start")
                            }
                            clicks_count_list += [clicks_data]
                    dx = dict()
                    for i in clicks_count_list:
                        dx.setdefault(i["date_start"], []).append(i["clicks"])
                    for k in dx:
                        dx[k] = sum(float(i) for i in dx[k])
                    clicks_count_list = [{"date_start": k, "clicks": str(v)} for k, v in dx.items()]
                    clicks_count_list = sorted(clicks_count_list, key=lambda k: k['date_start'])[::-1]

                    for t_cpc in cpc_count:
                        if t_cpc["data"] != []:
                            cpc_data = {
                                "cpc": '%0.2f'%(float(t_cpc["data"][0].get("cpc"))),
                                "date_start": t_cpc["data"][0].get("date_start")
                            }
                            cpc_count_list += [cpc_data]
                    dx = dict()
                    for i in cpc_count_list:
                        dx.setdefault(i["date_start"], []).append(i["cpc"])
                    for k in dx:
                        dx[k] = sum(float(i) for i in dx[k])
                    cpc_count_list = [{"date_start": k, "cpc": str(v)} for k, v in dx.items()]
                    cpc_count_list = sorted(cpc_count_list, key=lambda k: k['date_start'])[::-1]

                    for t_ctr in ctr_count:
                        if t_ctr["data"] != []:
                            ctr_data = {
                                "ctr": '%0.2f'%(float(t_ctr["data"][0].get("ctr"))),
                                "date_start": t_ctr["data"][0].get("date_start")
                            }
                            ctr_count_list += [ctr_data]
                    dx = dict()
                    for i in ctr_count_list:
                        dx.setdefault(i["date_start"], []).append(i["ctr"])
                    for k in dx:
                        dx[k] = sum(float(i) for i in dx[k])
                    ctr_count_list = [{"date_start": k, "ctr": str(v)} for k, v in dx.items()]
                    ctr_count_list = sorted(ctr_count_list, key=lambda k: k['date_start'])[::-1]

                    for l in conversions_count_list:
                        date_start = l["date_start"]
                        for i in clicks_count_list:
                            if date_start == i["date_start"]:
                                cvr = '%0.2f' %(float(l["conversions"])/float(i["clicks"]) * 100) if float(i["clicks"]) != 0 else 0
                                cvr_count_list += [
                                    {
                                        "cvr": cvr,
                                        "date_start": date_start
                                    }
                                ]

                    for l in conversions_count_list:
                        date_start = l["date_start"]
                        for i in costs_count_list:
                            if date_start == i["date_start"]:
                                cpi = '%0.2f'%(float(i["spend"])/float(l["conversions"])) if float(l["conversions"]) != 0 else 0
                                cpi_count_list += [
                                    {
                                        "cpi": cpi,
                                        "date_start": date_start
                                    }
                                ]

                    if len(revenue_new_list) >= len(costs_count_list):
                        count = len(costs_count_list)
                        len_difference = len(revenue_new_list) - len(costs_count_list)
                        for le in range(len_difference):
                            costs_count_list += [{
                                "spend": 0,
                                "date_start": revenue_new_list[count+le].get("date_start")
                            }]
                    else:
                        len_difference = len(costs_count_list) - len(revenue_new_list)
                        count = len(revenue_new_list)
                        for le in range(len_difference):
                            revenue_new_list += [{
                                "revenue": '%0.2f'%(float(conversions_count_list[count+le].get("conversions"))*float(price_default)),
                                "date_start": costs_count_list[count+le].get("date_start")
                            }]

                    for r in costs_count_list:
                        date_start = r["date_start"]
                        for j in revenue_new_list:
                            if date_start == j["date_start"]:
                                profit = '%0.2f' % (float(j["revenue"])-float(r["spend"]))
                                profit_list += [
                                    {
                                        "profit": profit,
                                        "date_start": date_start
                                    }
                                ]

                    count_revenue = 0
                    for a in revenue_new_list:
                        count_revenue += float(a["revenue"])

                    data_date_table = {
                        "impressions_list": impressions_count_list,
                        "cost_list": costs_count_list,
                        "clicks_list": clicks_count_list,
                        "conversions_list":conversions_count_list,
                        "ctr_list": ctr_count_list,
                        "cvr_list": cvr_count_list,
                        "cpc_list": cpc_count_list,
                        "cpi_list": cpi_count_list,
                        "revenue_list": revenue_new_list,
                        "profit_list": profit_list,
                        "head": ["Date","Revenue","Profit","Cost","Impressions","Clicks","Conversions","CTR","CVR","CPC","CPI"]
                    }
                    data_geo_table ={}
                    data_geo["revenue"] = str(count_revenue)
                    data_geo["profit"] = '%0.2f'%(float(count_revenue) - float(data_geo["count_cost"]))
                    date_range = []
                    impressions_range = []
                    cost_range = []
                    revenue_range = []
                    clicks_range = []
                    conversions_range = []
                    ctr_range = []
                    cvr_range = []
                    cpc_range = []
                    cpi_range = []
                    profit_range = []
                    for i in revenue_new_list:
                        date_range.append(i["date_start"])
                        revenue_range.append(i["revenue"])
                    for i in impressions_count_list:
                        impressions_range.append(i["impressions"])
                    for i in costs_count_list:
                        cost_range.append(i["spend"])
                    for i in clicks_count_list:
                        clicks_range.append(i["clicks"])
                    for i in conversions_count_list:
                        conversions_range.append(i["conversions"])
                    for i in ctr_count_list:
                        ctr_range.append(i["ctr"])
                    for i in cvr_count_list:
                        cvr_range.append(i["cvr"])
                    for i in cpc_count_list:
                        cpc_range.append(i["cpc"])
                    for i in cpi_count_list:
                        cpi_range.append(i["cpi"])
                    for i in profit_list:
                        profit_range.append(i["profit"])

                    data_range = {
                        "date": date_range[::-1],
                        "revenue": revenue_range[::-1],
                        "impressions": impressions_range[::-1],
                        "costs": cost_range[::-1],
                        "clicks": clicks_range[::-1],
                        "conversions": conversions_range[::-1],
                        "ctr": ctr_range[::-1],
                        "cvr": cvr_range[::-1],
                        "cpc": cpc_range[::-1],
                        "cpi": cpi_range[::-1],
                        "profit": profit_range[::-1]
                    }
                return json.dumps({
                    "code": 200,
                    "data_geo": data_geo,
                    "data_geo_table": data_geo_table,
                    "data_date_table": data_date_table,
                    "data_range": data_range,
                    "message": "success"
                })
            except Exception as e:
                print e
                return json.dumps({
                    "code":500,
                    "message": "no bind data or bind wrong data"
                })