# -*- coding: utf-8 -*-
from __future__ import division
from main.has_permission import *
from flask import Blueprint, Flask
from main import db
from models import Offer, Token
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
