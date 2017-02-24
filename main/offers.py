# -*- coding: utf-8 -*-
from __future__ import division
from main.has_permission import *
from flask import Blueprint, request
from main import db
from models import Offer, History, User, Customers, Country, TimePrice, Advertisers, UserRole, Role,CampaignRelations
import json
import os
import datetime, time
import xlrd
from sqlalchemy import desc

offers = Blueprint('offers', __name__)

@offers.route('/api/customer_select', methods=['POST', 'GET'])
def customerSelect():
    if request.method == "POST":
        data = request.get_json(force=True)
        result = []
        customers = Customers.query.filter(Customers.company_name.ilike('%' + data["name"] + '%'),Customers.status=="Created").all()
        for i in customers:
            data = {
                "id": i.company_name+"("+str(i.id)+")",
                "text": i.company_name
            }
            result += [data]
        response = {
            "code": 200,
            "result": result
        }
        return json.dumps(response)


@offers.route('/api/country_select', methods=["POST", "GET"])
def countrySelect():
    if request.method == "POST":
        data = request.get_json(force=True)
        name_list = data['name'].split(',')
        result_list = []
        result = []
        for name in name_list:
            if name == '':
                countries = Country.query.all()
            else:
                if u'\u4e00' <= name <= u'\u9fff':
                    countries = Country.query.filter(Country.chinese.ilike('%' + name + '%')).all()
                else:
                    countries = Country.query.filter(Country.shorthand.ilike('%' + name + '%')).all()
            if countries and isinstance(countries, list):
                for i in countries:
                    if i.shorthand not in result_list and name not in result_list:
                        if u'\u4e00' <= name <= u'\u9fff':
                            result_list.append(i.shorthand)
                        elif name != '':
                            result_list.append(name)
                    data = {
                        "id": i.shorthand,
                        "text": i.chinese+"("+i.shorthand+")"
                    }
                    result += [data]
        response = {
            "code": 200,
            "result": result,
            "message": "success",
            "namelist": result_list,
        }
        return json.dumps(response)
    else:
        return json.dumps({"code": 500, "message": "The request type wrong!"})


@offers.route('/api/user_select', methods=["POST", "GET"])
def userSelect():
    try:
        role = Role.query.filter_by(name="Sales").first()
        roleId = str(role.id)
        user_roles = UserRole.query.filter().all()
        userIds = []
        for r in user_roles:
            if roleId in r.role_id:
                userIds.append(r.user_id)
        result = []
        for i in userIds:
            user = User.query.filter_by(id=int(i)).first()
            data = {
                "id": i,
                "name": user.name,
                "email": user.email
            }
            result += [data]
        response = {
            "code": 200,
            "result": result,
            "message": "success"
        }
    except Exception as e:
        print e
        response = {
            "code": 500,
            "message": "no sales group"
        }
    return json.dumps(response)


@offers.route('/api/create_offer', methods=['POST', 'GET'])
@Permission.check(models=["offer_create"])
def createOffer():
    if request.method == "POST":
        data = request.get_json(force=True)
        createdTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        updateTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        if data["offer_id"]:
            offer_id = int(data["offer_id"])
            oldOffer = Offer.query.filter_by(id=offer_id).first()
            offer = Offer(oldOffer.user_id,oldOffer.customer_id,oldOffer.status,oldOffer.contract_type,oldOffer.contract_num,oldOffer.contract_scale,oldOffer.os,oldOffer.package_name,oldOffer.app_name,oldOffer.app_type,oldOffer.preview_link,oldOffer.track_link,oldOffer.material,oldOffer.startTime,oldOffer.endTime,oldOffer.platform,oldOffer.country,oldOffer.price,oldOffer.daily_budget,oldOffer.daily_type,oldOffer.total_budget,oldOffer.total_type,oldOffer.distribution,oldOffer.authorized,oldOffer.named_rule,oldOffer.KPI,oldOffer.settlement,oldOffer.period,oldOffer.remark,oldOffer.email_time,oldOffer.email_users,oldOffer.email_template,createdTime,updateTime)
            try:
                db.session.add(offer)
                db.session.commit()
                db.create_all()

                oldHistorty = History.query.filter_by(offer_id=offer_id).all()
                for i in oldHistorty:
                    historty = History(offer.id, i.user_id,"default",createdTime,i.status,i.country,i.country_price,i.price,i.daily_budget,i.daily_type,i.total_budget,i.total_type,i.KPI,i.contract_type,i.contract_scale)
                    db.session.add(historty)
                    db.session.commit()
                    db.create_all()
                return json.dumps({"code":200,"message":"success","offerId":offer.id})
            except Exception as e:
                print e
                return json.dumps({"code":500,"message":"fail"})

        else:
            contract_type = data["contract_type"]

            user_id= data["user_id"].split("(")[1].split(')')[0]
            customer_id = data["customer_id"].split("(")[1].split(')')[0]

            offer = Offer(int(user_id), int(customer_id), data["status"], contract_type,data["contract_num"], float(data["contract_scale"] if data["contract_scale"] else 0), data["os"], data["package_name"],data["app_name"], data["app_type"].encode('utf-8'), data["preview_link"], data["track_link"],data["material"], data["startTime"], data["endTime"], str(data["platform"]), str(data["country"]),float(data["price"] if data["price"] else 0), float(data["daily_budget"] if data["daily_budget"] else 0), data["daily_type"],float(data["total_budget"] if data["total_budget"] else 0), data["total_type"], data["distribution"], data["authorized"],data["named_rule"], data["KPI"].encode('utf-8'), data["settlement"].encode('utf-8'),data["period"].encode('utf-8'), data["remark"].encode('utf-8'), data["email_time"],str(data["email_users"]), int(data["email_tempalte"]), createdTime, updateTime)
            try:
                db.session.add(offer)
                db.session.commit()
                db.create_all()

                for i in data['country_detail']:
                    history = History(offer.id, int(user_id), "default", createdTime, status=data["status"],country=i["country"], country_price=i["price"], price=data["price"],daily_budget=float(data["daily_budget"] if data["daily_budget"] else 0), daily_type=data["daily_type"],total_budget=float(data["total_budget"] if data["total_budget"] else 0),  total_type=data["total_type"],KPI=data["KPI"], contract_type=contract_type,contract_scale=float(data["contract_scale"] if data["contract_scale"] else 0))
                    db.session.add(history)
                    db.session.commit()
                    db.create_all()
                return json.dumps({"code": 200, "message": "success", "offerId":offer.id})
            except Exception as e:
                print e
                return json.dumps({"code": 500, "message": "fail"})


@offers.route('/api/offer_show', methods=["POST", "GET"])
def offerShow():
    if request.method == "POST":
        data = request.get_json(force=True)
        page = data["page"]
        limit = int(data["limit"])
        offers = Offer.query.filter(Offer.status != "deleted").order_by(Offer.id.desc()).paginate(int(page), per_page=limit, error_out = False)
        count = Offer.query.filter(Offer.status != "deleted").count()
        if (count % limit) == 0:
            totalPages = count/limit
        else:
            totalPages = count/limit + 1
        result = []
        for i in offers.items:
            customerId = i.customer_id
            customer = Customers.query.filter_by(id=customerId).first()
            customerName = customer.company_name  # 客户名称
            status = i.status
            contract_type = i.contract_type
            sales = User.query.filter_by(id=int(i.user_id)).first()
            if contract_type == "1":
                contract_type = u"服务费"
            elif contract_type == "2":
                contract_type = "cpa"
            os = i.os
            app_name = i.app_name
            if i.endTime >= (datetime.datetime.now()+datetime.timedelta(days=10950)).strftime("%Y-%m-%d %H:%M:%S"):
                endTime = "TBD"
            else:
                endTime = i.endTime
            data = {
                "offer_id": i.id,
                "status": status,
                "contract_type": contract_type,
                "os": os,
                "customer_id": customerName,
                "app_name": app_name,
                "startTime": i.startTime,
                "endTime": endTime,
                "country": str(i.country),
                "price": i.price,
                "updateTime": i.updateTime,
                "sale_name":sales.name
            }
            result += [data]
        response = {
            "totalPages": int(totalPages),
            "code": 200,
            "result": result,
            "message": "success"
        }
        return json.dumps(response)


@offers.route('/api/offer_detail/<id>', methods=["GET"])
def offerDetail(id):
    offer = Offer.query.filter_by(id=int(id)).first()
    customerId = offer.customer_id
    customer = Customers.query.filter_by(id=customerId).first()
    userId = offer.user_id
    user = User.query.filter_by(id=userId).first()
    contract_type = offer.contract_type
    if contract_type != "1":
        contract_scale = 0
    else:
        contract_scale = offer.contract_scale
    plate = offer.platform

    result = {
        "customer_id": customer.company_name+"("+str(customer.id)+")",
        "status": offer.status,
        "contract_scale": contract_scale,
        "contract_num": offer.contract_num,
        "contract_type": contract_type,
        "user_id": user.name+"("+str(user.id)+")",
        "os": offer.os,
        "package_name": offer.package_name,
        "app_name": offer.app_name,
        "app_type": offer.app_type,
        "preview_link": offer.preview_link,
        "track_link": offer.track_link,
        "material": offer.material,
        "startTime": offer.startTime,
        "endTime": offer.endTime,
        "platform": str(plate),
        "country": str(offer.country),
        "price": offer.price,
        "daily_budget": offer.daily_budget,
        "daily_type": offer.daily_type,
        "total_budget": offer.total_budget,
        "total_type": offer.total_type,
        "distribution": offer.distribution,
        "authorized": offer.authorized,
        "named_rule": offer.named_rule,
        "KPI": offer.KPI,
        "settlement": offer.settlement,
        "period": offer.period,
        "remark": offer.remark,
        "email_time": offer.email_time,
        "email_users": offer.email_users,
        "email_tempalte": offer.email_template
    }
    historties = History.query.filter(History.offer_id == id, History.country != "").all()
    countries = []
    for i in historties:
        country = i.country
        countries.append(country)
    countries = list(set(countries))
    country_detail = []
    for i in countries:
        historty = History.query.filter(History.offer_id == id, History.country == i).order_by(
            desc(History.createdTime)).first()
        country = historty.country
        country_price = historty.country_price
        detail = {
            "country": country,
            "price": country_price
        }
        country_detail += [detail]
    result["country_detail"] = country_detail
    response = {
        "code": 200,
        "result": result,
        "message": "success"
    }
    return json.dumps(response)

#offer国家对应的价钱
@offers.route('/api/country_price/<offerId>', methods=["GET"])
def countryPrice(offerId):
    historties = History.query.filter(History.offer_id == int(offerId), History.country != "").all()
    countries = []
    for i in historties:
        country = i.country
        countries.append(country)
    countries = list(set(countries))
    country_price_list = []
    for i in countries:
        historty = History.query.filter(History.offer_id == int(offerId), History.country == i).order_by(
            desc(History.createdTime)).first()
        country = historty.country
        country_price = historty.country_price
        detail = {
            "country": country,
            "price": country_price
        }
        country_price_list += [detail]
    response = {
        "code": 200,
        "result": country_price_list,
        "message": "success"
    }
    return json.dumps(response)

#更新offer的状态
@offers.route('/api/update_offer_status/<offer_id>', methods=["GET","POST"])
@Permission.check(models=["offer_create","offer_edit","offer_query"])
def updateStatus(offer_id):
    offer = Offer.query.filter_by(id=int(offer_id)).first()
    if request.method == "GET":
        if offer.status == "active":
            offer.status = "inactive"
            status = offer.status
            db.session.add(offer)
            db.session.commit()
            history = History(offer.id, offer.user_id, "update",
                              (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime(
                                  "%Y-%m-%d %H:%M:%S"),
                              price=offer.price,
                              status=status,
                              daily_budget=offer.daily_budget,
                              daily_type=offer.daily_type,
                              total_budget=offer.total_budget,
                              total_type=offer.total_type,
                              KPI=offer.KPI,
                              contract_type=offer.contract_type,
                              contract_scale=offer.contract_scale)
            db.session.add(history)
            db.session.commit()
            db.create_all()
            return json.dumps({"code": 200, "message":"success"})
        elif offer.status == "inactive":
            offer.status = "active"
            status = offer.status
            db.session.add(offer)
            db.session.commit()
            history = History(offer.id, offer.user_id, "update",
                              (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime(
                                  "%Y-%m-%d %H:%M:%S"),
                              price=offer.price,
                              status=status,
                              daily_budget=offer.daily_budget,
                              daily_type=offer.daily_type,
                              total_budget=offer.total_budget,
                              total_type=offer.total_type,
                              KPI=offer.KPI,
                              contract_type=offer.contract_type,
                              contract_scale=offer.contract_scale)
            db.session.add(history)
            db.session.commit()
            db.create_all()
            return json.dumps({"code": 200, "message": "success"})
    else:
        offer.status = "deleted"
        status = offer.status
        db.session.add(offer)
        db.session.commit()
        history = History(offer.id, offer.user_id, "update",
                          (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime(
                              "%Y-%m-%d %H:%M:%S"),
                          price=offer.price,
                          status=status,
                          daily_budget=offer.daily_budget,
                          daily_type=offer.daily_type,
                          total_budget=offer.total_budget,
                          total_type=offer.total_type,
                          KPI=offer.KPI,
                          contract_type=offer.contract_type,
                          contract_scale=offer.contract_scale)
        db.session.add(history)
        db.session.commit()
        db.create_all()
        return json.dumps({"code": 200, "message": "success"})

@offers.route('/api/update_offer', methods=["POST", "GET"])
@Permission.check(models=["offer_create","offer_edit","offer_query"])
def updateOffer():
    if request.method == "POST":
        data = request.get_json(force=True)
        offer = Offer.query.filter_by(id=int(data["offer_id"])).first()
        flag = data["flag"]
        if offer is not None:
            try:
                customer_id = data["customer_id"].split("(")[1].split(')')[0]
                user_id = data["user_id"].split("(")[1].split(')')[0]
                offer.updateTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                offer.status = data["status"] if data["status"] != "" else offer.status
                offer.customer_id = int(customer_id) if data["customer_id"] != "" else offer.customer_id
                offer.user_id = int(user_id) if data['user_id'] != "" else offer.user_id
                offer.contract_type = data["contract_type"] if data["contract_type"] != "" else offer.contract_type
                offer.contract_scale = float(data["contract_scale"]) if data["contract_scale"] != "" else offer.contract_scale
                offer.contract_num = data["contract_num"] if data["contract_num"] != "" else offer.contract_num
                offer.os = data["os"] if data["os"] != "" else offer.os
                offer.package_name = data["package_name"] if data["package_name"] != "" else offer.package_name
                offer.app_name = data["app_name"] if data["app_name"] != "" else offer.app_name
                offer.app_type = data["app_type"] if data["app_type"] != "" else offer.app_type
                offer.preview_link = data["preview_link"] if data["preview_link"] != "" else offer.preview_link
                offer.track_link = data["track_link"] if data["track_link"] != "" else offer.track_link
                offer.material = data["material"] if data["material"] != "" else offer.material
                offer.startTime = data["startTime"] if data["startTime"] != "" else offer.startTime
                offer.endTime = data["endTime"] if data["endTime"] != "" else offer.endTime
                offer.platform = str(data["platform"]) if str(data["platform"]) != "" else offer.platform
                offer.country = str(data["country"]) if str(data["country"]) != "" else offer.country
                offer.price = float(data["price"]) if data["price"] != "" else offer.price
                offer.daily_budget = float(data["daily_budget"]) if data["daily_budget"] != "" else offer.daily_budget
                offer.daily_type = data["daily_type"] if data["daily_type"] != "" else offer.daily_type
                offer.total_budget = float(data["total_budget"]) if data["total_budget"] != "" else offer.total_budget
                offer.total_type = data["total_type"] if data["total_type"] != "" else offer.total_type
                offer.distribution = data["distribution"] if data["distribution"] != "" else offer.distribution
                offer.authorized = data["authorized"] if data['authorized'] != "" else offer.authorized
                offer.named_rule = data["named_rule"] if data["named_rule"] != "" else offer.named_rule
                offer.KPI = data["KPI"].encode('utf-8') if data["KPI"] != "" else offer.KPI
                offer.settlement = data['settlement'].encode('utf-8') if data["settlement"] != "" else offer.settlement
                offer.period = data["period"].encode("utf-8") if data["period"] != "" else offer.period
                offer.remark = data["remark"].encode("utf-8") if data["remark"] != "" else offer.remark
                offer.email_time = data["email_time"]
                offer.email_users = str(data["email_users"]) if str(data["email_users"]) != "" else offer.email_users
                offer.email_template = data["email_tempalte"] if data["email_tempalte"] != "" else offer.email_template
                db.session.add(offer)
                db.session.commit()
                if "country_detail" in flag:
                    if data["country_detail"] != []:
                        for i in data['country_detail']:
                            history = History(int(offer.id), int(offer.user_id), "update",
                                              (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime(
                                                  "%Y-%m-%d %H:%M:%S"), country=i["country"], country_price=i["price"],
                                              price=float(data["price"]) if data["price"] != "" else 0,
                                              status=data["status"],
                                              daily_budget=float(data["daily_budget"]) if data["daily_budget"] != "" else 0,
                                              daily_type=data["daily_type"],
                                              total_budget=float(data["total_budget"]) if data['total_budget'] != "" else 0,
                                              total_type=data["total_type"], KPI=data["KPI"],
                                              contract_type=data["contract_type"],
                                              contract_scale=float(data["contract_scale"] if data["contract_scale"] != "" else 0))
                            db.session.add(history)
                            db.session.commit()
                            db.create_all()
                    else:
                        history = History(int(offer.id), int(offer.user_id), "update",
                                          (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime(
                                              "%Y-%m-%d %H:%M:%S"),
                                          price=float(data["price"]) if data["price"] != "" else 0, status=data["status"],
                                          daily_budget=float(data["daily_budget"]) if data["daily_budget"] != "" else 0,
                                          daily_type=data["daily_type"],
                                          total_budget=float(data["total_budget"]) if data['total_budget'] != "" else 0,
                                          total_type=data["total_type"], KPI=data["KPI"],
                                          contract_type=data["contract_type"],
                                          contract_scale=float(data["contract_scale"]) if data["contract_scale"] != "" else 0)
                        db.session.add(history)
                        db.session.commit()
                        db.create_all()

                return json.dumps({"code": 200, "message": "success"})
            except Exception as e:
                print e
                return json.dumps({"code": 500, "message": "fail"})
        else:
            return json.dumps({"code": 400, "message": "offer is None"})

#bind list
@offers.route("/api/offer_bind", methods=["POST","GET"])
@Permission.check(models=["bind_create","bind_edit","bind_query"])
def offerBind():
    if request.method == "POST":
        data = request.get_json(force=True)
        createdTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        updateTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        token = "EAAHgEYXO0BABABt1QAdnb4kDVpgDv0RcA873EqcNbHFeN8IZANMyXZAU736VKOj1JjSdOPk2WuZC7KwJZBBD76CUbA09tyWETQpOd5OCRSctIo6fuj7cMthZCH6pZA6PZAFmrMgGZChehXreDa3caIZBkBwkyakDAGA4exqgy2sI7JwZDZD"

        advertisers = Advertisers(token,int(data["offer_id"]), type=data["type"], facebook_keywords=data["advertise_series"], facebook_accountId=data["advertise_groups"], createdTime=createdTime, updateTime=updateTime)
        try:
            db.session.add(advertisers)
            db.session.commit()
            db.create_all()
            return json.dumps({"code": 200, "message":"success"})
        except Exception as e:
            print e
            return json.dumps({"code": 500, "message": "fail"})

#show bind
@offers.route("/api/bind_show/<offer_id>", methods=["POST","GET"])
def bindShow(offer_id):
    advertiser_facebook = Advertisers.query.filter_by(offer_id=int(offer_id), type="facebook").first()
    if advertiser_facebook:
        advertise_series_facebook = advertiser_facebook.facebook_keywords
        advertise_groups_facebook = advertiser_facebook.facebook_accountId
        type_facebook = advertiser_facebook.type
        result_facebook = {
            "facebook_id": advertiser_facebook.id,
            "advertise_series": advertise_series_facebook,
            "advertise_groups": advertise_groups_facebook,
            "type": type_facebook
        }
    else:
        result_facebook={}

    advertiser_adwords = Advertisers.query.filter_by(offer_id=int(offer_id), type="adwords").first()
    if advertiser_adwords:
        advertise_series_adwords = advertiser_adwords.adwords_notuac
        advertise_groups_adwords = advertiser_adwords.adwords_uac
        type_adwords = advertiser_adwords.type
        result_adwords = {
            "adwords_id": advertiser_adwords.id,
            "advertise_series": advertise_series_adwords,
            "advertise_groups": advertise_groups_adwords,
            "type": type_adwords
        }
    else:
        result_adwords = {}

    response = {
        "facebook": result_facebook,
        "adwords": result_adwords,
        "code": 200,
        "message": "success"
    }
    return json.dumps(response)

#update bind
@offers.route("/api/bind_update", methods=["POST","GET"])
@Permission.check(models=["bind_create","bind_edit","bind_query"])
def bindUpdate():
    if request.method == "POST":
        data = request.get_json(force=True)
        advertise = Advertisers.query.filter_by(id=int(data["ad_id"])).first()

        updateTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        try:
            advertise.facebook_keywords = data["facebook_keywords"]
            advertise.facebook_accountId = data["facebook_accountId"]
            advertise.type = data["type"]
            advertise.updateTime = updateTime
            db.session.add(advertise)
            db.session.commit()
            return json.dumps({"code":200,"message":"success"})
        except Exception as e:
            print e
            return json.dumps({"code": 500, "message": "fail"})

#显示绑定的所有的campaign name
@offers.route("/api/bind_detail", methods=["POST","GET"])
def bindDetail():
    if request.method == "POST":
        data = request.get_json(force=True)
        offerId = int(data["offer_id"])
        bind_advertisers = Advertisers.query.filter_by(offer_id=offerId).first()
        campaignNames = []
        if bind_advertisers:
            advertisers = bind_advertisers.facebook_keywords
            for i in advertisers.split(','):
                campaigns = CampaignRelations.query.filter(CampaignRelations.campaignName.like(i+'%')).all()
                for j in campaigns:
                    campaignNames.append(j.campaignName)
            return json.dumps({
                "code": 200,
                "campaignNames": campaignNames,
                "message": "success"
            })
        else:
            return json.dumps({
                "code": 200,
                "campaignNames": campaignNames,
                "message": "no bind datas"
            })

@offers.route("/api/history", methods=["POST", "GET"])
def historty():
    if request.method == "POST":
        data = request.get_json(force=True)
        offer_id = int(data["offer_id"])
        flag = data["flag"]
        if flag == "country_detail":
            country = []
            result = []
            history = History.query.filter(History.offer_id == offer_id, History.country != "")
            for i in history:
                country.append(i.country)
            country = list(set(country))
            for i in country:
                detail = []
                history_country = History.query.filter(History.offer_id == offer_id, History.country == i)
                for j in history_country:
                    createdTime = j.createdTime
                    country_price = j.country_price
                    country_data = {
                        "country": i,
                        "country_price": country_price,
                        "createdTime": createdTime
                    }
                    result += [country_data]
            response = {
                "code": 200,
                "result": result
            }
            return json.dumps(response)
        else:
            result = []
            if flag == "status":
                history = History.query.filter(History.offer_id == offer_id, History.status != "")
                for i in history:
                    status = i.status
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = User.query.filter(User.id == user_id).first()
                    detail = {
                        "username": user.name,
                        "status": status,
                        "createdTime": createdTime
                    }
                    result += [detail]
            elif flag == "contract_type":
                history = History.query.filter(History.offer_id == offer_id, History.contract_type != "")
                for i in history:
                    contract_type = i.contract_type
                    if contract_type == "1":
                        contract_type = u"服务费"
                    elif contract_type == "2":
                        contract_type = "cpa"
                    contract_scale = i.contract_scale
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = User.query.filter(User.id == user_id).first()
                    detail = {
                        "username": user.name,
                        "contract_type": contract_type,
                        "contract_scale": contract_scale,
                        "createdTime": createdTime
                    }
                    result += [detail]

            elif flag == "price":
                history = History.query.filter(History.offer_id == offer_id, History.price != "")
                for i in history:
                    price = i.price
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = User.query.filter(User.id == user_id).first()
                    detail = {
                        "username": user.name,
                        "price": price,
                        "createdTime": createdTime
                    }
                    result += [detail]
            elif flag == "daily_budget":
                history = History.query.filter(History.offer_id == offer_id, History.daily_budget != "")
                for i in history:
                    daily_budget = i.daily_budget
                    daily_type = i.daily_type
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = User.query.filter(User.id == user_id).first()
                    detail = {
                        "username": user.name,
                        "daily_budget": daily_budget,
                        "daily_type": daily_type,
                        "createdTime": createdTime
                    }
                    result += [detail]
            elif flag == "total_budget":
                history = History.query.filter(History.offer_id == offer_id, History.total_budget != "")
                for i in history:
                    total_budget = i.total_budget
                    total_type = i.total_type
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = User.query.filter(User.id == user_id).first()
                    detail = {
                        "username": user.name,
                        "total_budget": total_budget,
                        "total_type": total_type,
                        "createdTime": createdTime
                    }
                    result += [detail]
            elif flag == "KPI":
                history = History.query.filter(History.offer_id == offer_id, History.total_budget != "")
                for i in history:
                    KPI = i.KPI
                    createdTime = i.createdTime
                    user_id = i.user_id
                    user = User.query.filter(User.id == user_id).first()
                    detail = {
                        "username": user.name,
                        "KPI": KPI,
                        "createdTime": createdTime
                    }
                    result += [detail]

            f = lambda x, y: x if y in x else x + [y]
            response = {
                "code": 200,
                "result": reduce(f, [[], ] + result)
            }
            return json.dumps(response)

# 导入国家表
@offers.route("/api/country")
def country():
    wb = xlrd.open_workbook("/home/centos/1.xlsx")

    wb.sheet_names()
    sh = wb.sheet_by_name(u'Sheet1')
    count = 0
    for rownum in range(sh.nrows):
        country = Country(sh.row_values(rownum)[0], sh.row_values(rownum)[1], sh.row_values(rownum)[2])
        db.session.add(country)
        db.session.commit()
        db.create_all()
        count += 1

    return json.dumps({
        "code":200,
        "message":"success"
    })
#创建时导入国家对应时间价钱
@offers.route("/api/country_time/create", methods=["POST", "GET"])
def createCountryTime():
    if request.method == "POST":
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_dir = os.path.join(basedir, 'upload')
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        unix_time = int(time.time())
        f = request.files['file']
        new_filename = str(unix_time) + '.xlsx'  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        try:
            data = xlrd.open_workbook(file_dir + "/" + new_filename)
        except Exception, e:
            print e

        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        data = []
        for rownum in range(1, nrows):
            date = []
            timea = []
            for col in range(1, ncols):
                timea.append(xlrd.xldate.xldate_as_datetime(table.row_values(0)[col], 1).strftime("%Y-%m-%d"))
                date.append(table.row_values(rownum)[col])

            result = {
                "country": table.row_values(rownum)[0],
                "date": date,
                "time": timea
            }
            data += [result]

        offerIds = []
        offer_msg = Offer.query.all()

        if offer_msg == []:
            offer_id = 1
        else:
            for i in offer_msg:
                offerIds.append(i.id)
            offer_id = offerIds[-1] + 1

        for i in data:
            for j in range(len(i["time"])):
                time_coun = i["time"][j]
                try:
                    price = '%0.2f' % (i["date"][j])
                except Exception as e:
                    print e
                country = i['country']
                coun = Country.query.filter_by(shorthand=country).first()

                time_Price = TimePrice.query.filter_by(offer_id=int(offer_id), country_id=coun.id, date=time_coun).first()
                if time_Price:
                    time_Price.price = price
                    db.session.add(time_Price)
                    db.session.commit()
                else:
                    timePrice = TimePrice(int(offer_id), coun.id, time_coun, price)
                    db.session.add(timePrice)
                    db.session.commit()
                    db.create_all()

        response = {
            "code": 200,
            "data": data,
            "message": "success"
        }
    else:
        response = {
            "code": 500,
            "message": "fail"
        }
    return json.dumps(response)

# 更新时导入国家对应的时间
@offers.route("/api/country_time/<offerId>", methods=["POST", "GET"])
def importCountry(offerId):
    if request.method == "POST":
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_dir = os.path.join(basedir, 'upload')
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        unix_time = int(time.time())
        f = request.files['file']
        new_filename = str(unix_time) + '.xlsx'  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        try:
            data = xlrd.open_workbook(file_dir + "/" + new_filename)
        except Exception, e:
            print e

        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        data = []
        for rownum in range(1, nrows):
            date = []
            timea = []
            for col in range(1, ncols):
                timea.append(xlrd.xldate.xldate_as_datetime(table.row_values(0)[col], 1).strftime("%Y-%m-%d"))
                date.append(table.row_values(rownum)[col])

            result = {
                "country": table.row_values(rownum)[0],
                "date": date,
                "time": timea
            }
            data += [result]

        for i in data:
            for j in range(len(i["time"])):
                time_coun = i["time"][j]
                try:
                    price = '%0.2f' % (i["date"][j])
                except Exception as e:
                    print e
                country = i['country']
                coun = Country.query.filter_by(shorthand=country).first()

                time_Price = TimePrice.query.filter_by(offer_id=int(offerId),country_id=coun.id,date=time_coun).first()
                if time_Price:
                    time_Price.price = price
                    db.session.add(time_Price)
                    db.session.commit()
                else:
                    timePrice = TimePrice(int(offerId),coun.id, time_coun, price)
                    db.session.add(timePrice)
                    db.session.commit()
                    db.create_all()

        response = {
            "code": 200,
            "data": data,
            "message": "success"
        }
    else:
        response = {
            "code": 500,
            "message": "fail"
        }
    return json.dumps(response)


@offers.route("/api/country_time_show", methods=["POST", "GET"])
def showCountryTime():
    if request.method == "POST":
        data = request.get_json(force=True)
        date = data['date']
        country = data["country"]
        countries = Country.query.filter_by(shorthand=country).first()
        countryId = countries.id
        month = date.split("-", 1)[1]
        year = int(date.split('-', 1)[0])
        if month in ["01", "03", "05", "07", "08", "10", "12"]:
            dateList = [date + "-01", date + "-02", date + "-03", date + "-04", date + "-05", date + "-06",
                        date + "-07", date + "-08", date + "-09", date + "-10", date + "-11", date + "-12",
                        date + "-13", date + "-14", date + "-15", date + "-16", date + "-17", date + "-18",
                        date + "-19", date + "-20", date + "-21", date + "-22", date + "-23", date + "-24",
                        date + "-25", date + "-26", date + "-27", date + "-28", date + "-29", date + "-30",
                        date + "-31"]
        elif month in ["04", "06", "09", "11"]:
            dateList = [date + "-01", date + "-02", date + "-03", date + "-04", date + "-05", date + "-06",
                        date + "-07", date + "-08", date + "-09", date + "-10", date + "-11", date + "-12",
                        date + "-13", date + "-14", date + "-15", date + "-16", date + "-17", date + "-18",
                        date + "-19", date + "-20", date + "-21", date + "-22", date + "-23", date + "-24",
                        date + "-25", date + "-26", date + "-27", date + "-28", date + "-29", date + "-30"]
        else:
            if year % 100 == 0 and year % 400 == 0:
                dateList = [date + "-01", date + "-02", date + "-03", date + "-04", date + "-05", date + "-06",
                            date + "-07", date + "-08",
                            date + "-09", date + "-10", date + "-11", date + "-12", date + "-13", date + "-14",
                            date + "-15", date + "-16",
                            date + "-17", date + "-18", date + "-19", date + "-20", date + "-21", date + "-22",
                            date + "-23", date + "-24",
                            date + "-25", date + "-26", date + "-27", date + "-28", date + "-29"]
            elif year % 100 != 0 and year % 4 == 0:
                dateList = [date + "-01", date + "-02", date + "-03", date + "-04", date + "-05", date + "-06",
                            date + "-07", date + "-08",
                            date + "-09", date + "-10", date + "-11", date + "-12", date + "-13", date + "-14",
                            date + "-15", date + "-16",
                            date + "-17", date + "-18", date + "-19", date + "-20", date + "-21", date + "-22",
                            date + "-23", date + "-24",
                            date + "-25", date + "-26", date + "-27", date + "-28", date + "-29"]
            else:
                dateList = [date + "-01", date + "-02", date + "-03", date + "-04", date + "-05", date + "-06",
                            date + "-07", date + "-08",
                            date + "-09", date + "-10", date + "-11", date + "-12", date + "-13", date + "-14",
                            date + "-15", date + "-16",
                            date + "-17", date + "-18", date + "-19", date + "-20", date + "-21", date + "-22",
                            date + "-23", date + "-24",
                            date + "-25", date + "-26", date + "-27", date + "-28"]
        result = []
        dateCurrent = []
        if data["offer_id"] != "":
            timePrices = TimePrice.query.filter(TimePrice.country_id == countryId, TimePrice.offer_id == int(data["offer_id"])).all()
            for t in timePrices:
                dateCurrent.append(t.date)
            for i in dateList:
                if i in dateCurrent:
                    timePrice = TimePrice.query.filter_by(country_id=countryId, date=i, offer_id=int(data["offer_id"])).first()
                    detail = {
                        "date": i,
                        "price": timePrice.price
                    }
                else:
                    detail = {
                        "date": i,
                        "price": ""
                    }
                result += [detail]
        else:
            for i in dateList:
                detail = {
                    "date": i,
                    "price": ""
                }
                result += [detail]
        response = {
            "code": 200,
            "result": result,
            "message": "success"
        }
        return json.dumps(response)


@offers.route('/api/country_time_update', methods=["POST", "GET"])
def updateContryTime():
    data = request.get_json(force=True)
    result = data["result"]
    countryName = data["country"]
    country = Country.query.filter_by(shorthand=countryName).first()
    countryId = country.id

    if data["offer_id"] == "":
        offerIds = []
        offer_msg = Offer.query.all()

        if offer_msg == []:
            offer_id = 1
        else:
            for i in offer_msg:
                offerIds.append(i.id)
            offer_id = offerIds[-1] + 1
    else:
        offer_id = int(data["offer_id"])
    for i in result:
        if i["price"] != "":
            timePrice = TimePrice.query.filter_by(country_id=countryId, date=i["date"], offer_id=offer_id).first()
            if timePrice:
                timePrice.price = i["price"]
                try:
                    db.session.add(timePrice)
                    db.session.commit()
                except Exception as e:
                    print e
                    return json.dumps({"code": 500, "message": "fail"})
            else:
                timePriceNew = TimePrice(offer_id,countryId, i["date"], i["price"])
                try:
                    db.session.add(timePriceNew)
                    db.session.commit()
                    db.create_all()
                except Exception as e:
                    print e
                    return json.dumps({"code": 500, "message": "fail"})
        else:
            pass
    return json.dumps({"code": 200, "message": "success"})

#offer list search
@offers.route('/api/offer_search', methods=["POST","GET"])
def offerSearch():
    if request.method == "POST":
        data = request.get_json(force=True)
        key = data["key"]
        offer_result_list = []
        appnames = Offer.query.filter(Offer.app_name.like("%"+key+"%"),Offer.status != "deleted").order_by(Offer.id.desc()).all()  #应用名称
        systems = Offer.query.filter(Offer.os.like("%"+key+"%"),Offer.status != "deleted").order_by(Offer.id.desc()).all()   #投放的系统
        customers = Customers.query.filter(Customers.company_name.like("%"+key+"%")).all()   #客户名称
        sales = User.query.filter(User.name.like("%"+key+"%")).all()    #销售名称
        result_appname = offer_search_detail(appnames)
        result_system = offer_search_detail(systems)
        offer_result_list.extend(result_appname)
        offer_result_list.extend(result_system)
        customer_ids = []
        sales_ids = []
        for i in customers:
            customer_ids.append(i.id)
        for i in customer_ids:
            customers_offer = Offer.query.filter(Offer.customer_id==i,Offer.status != "deleted").order_by(Offer.id.desc()).all()
            result_customer = offer_search_detail(customers_offer)
            offer_result_list.extend(result_customer)
        for i in sales:
            sales_ids.append(i.id)
        for i in sales_ids:
            sales_offer = Offer.query.filter(Offer.user_id==i,Offer.status != "deleted").order_by(Offer.id.desc()).all()
            result_sales = offer_search_detail(sales_offer)
            offer_result_list.extend(result_sales)
        offer_result_list_unique = []
        for j in offer_result_list:
            if j not in offer_result_list_unique:
                offer_result_list_unique.append(j)
            else:
                pass
        return json.dumps({
            "code": 200,
            "result": offer_result_list_unique
        })

def offer_search_detail(offers):
    offer_result_list = []
    for i in offers:
        contract_type = i.contract_type
        sales = User.query.filter_by(id=int(i.user_id)).first()
        if contract_type == "1":
            contract_type = u"服务费"
        elif contract_type == "2":
            contract_type = "cpa"
        if i.endTime >= (datetime.datetime.now() + datetime.timedelta(days=10950)).strftime("%Y-%m-%d %H:%M:%S"):
            endTime = "TBD"
        else:
            endTime = i.endTime
        customerId = i.customer_id
        customer = Customers.query.filter_by(id=customerId).first()
        customerName = customer.company_name
        offer_result_list += [
            {
                "offer_id": i.id,
                "status": i.status,
                "contract_type": contract_type,
                "os": i.os,
                "customer_id": customerName,
                "app_name": i.app_name,
                "startTime": i.startTime,
                "endTime": endTime,
                "country": str(i.country),
                "price": i.price,
                "updateTime": i.updateTime,
                "sale_name": sales.name
            }
        ]
    return offer_result_list

# @offers.route('/<path>')
# def today(path):
#     # base_dir = os.path.abspath(__file__)
#     base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
#     resp = make_response(open(os.path.join(base_dir, path)))
#     resp.headers["Content-type"] = "application/json;charset=UTF-8"
#     return resp
