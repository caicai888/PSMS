# -*- coding: utf-8 -*-
from __future__ import division
from main.has_permission import *
from flask import Blueprint, request
from main import db
from models import Offer, History, User, Customers, Country, TimePrice, Advertisers, UserRole, Role,CampaignRelations,PlatformOffer,CooperationPer
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
            if ',' in i.company_name:
                campany_name = i.company_name.replace(',','')
            else:
                campany_name = i.company_name
            data = {
                "id": campany_name+"("+str(i.id)+")",
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
            offer = Offer(oldOffer.user_id,oldOffer.customer_id,oldOffer.status,oldOffer.contract_num,oldOffer.os,oldOffer.package_name,oldOffer.app_name,oldOffer.app_type,oldOffer.preview_link,oldOffer.track_link,oldOffer.platform,oldOffer.email_time,oldOffer.email_users,oldOffer.email_template,createdTime,updateTime)
            try:
                db.session.add(offer)
                db.session.commit()
                db.create_all()
                oldplatformOffers = PlatformOffer.query.filter_by(offer_id=offer_id).all()
                for j in oldplatformOffers:
                    platformOffer = PlatformOffer(offer.id,j.platform,j.contract_type,j.contract_scale,j.material, j.startTime,j.endTime, j.country, j.price,j.daily_budget,j.daily_type, j.total_budget, j.total_type, j.distribution, j.authorized,j.named_rule, j.KPI,j.settlement, j.period, j.remark, createdTime, updateTime)
                    db.session.add(platformOffer)
                    db.session.commit()
                    db.create_all()

                    oldHistorty = History.query.filter_by(offer_id=offer_id,platformOffer_id=j.id).all()
                    for i in oldHistorty:
                        historty = History(offer.id, i.user_id,platformOffer.id,i.platform,"default",createdTime,i.status,i.country,i.country_price,i.price,i.daily_budget,i.daily_type,i.total_budget,i.total_type,i.KPI,i.contract_type,i.contract_scale)
                        db.session.add(historty)
                        db.session.commit()
                        db.create_all()
                return json.dumps({"code":200,"message":"success","offerId":offer.id})
            except Exception as e:
                print e
                return json.dumps({"code":500,"message":"fail"})

        else:
            user_id= data["user_id"].split("(")[1].split(')')[0]
            customer_id = data["customer_id"].split("(")[1].split(')')[0]

            offer = Offer(int(user_id), int(customer_id), data["status"], data["contract_num"], data["os"], data["package_name"],data["app_name"], data["app_type"].encode('utf-8'), data["preview_link"], data["track_link"],str(data["platform"]),data["email_time"],str(data["email_users"]), data["email_tempalte"], createdTime, updateTime)
            try:
                db.session.add(offer)
                db.session.commit()
                db.create_all()
                platforms = data["platform"].split(",")
                if "Facebook" in platforms:
                    fb = data["facebook"]
                    platformOffer = PlatformOffer(offer.id, "facebook",fb["contract_type"],float(fb["contract_scale"] if fb["contract_scale"] else 0),fb["material"], fb["startTime"], fb["endTime"],str(fb["country"]),float(fb["price"] if fb["price"] else 0), float(fb["daily_budget"] if fb["daily_budget"] else 0), fb["daily_type"],float(fb["total_budget"] if fb["total_budget"] else 0), fb["total_type"], fb["distribution"], fb["authorized"],fb["named_rule"], fb["KPI"].encode('utf-8'), fb["settlement"].encode('utf-8'),fb["period"].encode('utf-8'), fb["remark"].encode('utf-8'),createdTime,updateTime)
                    db.session.add(platformOffer)
                    db.session.commit()
                    db.create_all()
                    for i in fb['country_detail']:
                        history = History(offer.id, int(user_id),platformOffer.id,"facebook", "default", createdTime, status=offer.status,country=i["country"], country_price=float(i["price"]), price=platformOffer.price,daily_budget=float(fb["daily_budget"] if fb["daily_budget"] else 0), daily_type=fb["daily_type"],total_budget=float(fb["total_budget"] if fb["total_budget"] else 0),  total_type=fb["total_type"],KPI=fb["KPI"], contract_type=fb["contract_type"],contract_scale=float(fb["contract_scale"] if fb["contract_scale"] else 0))
                        db.session.add(history)
                        db.session.commit()
                        db.create_all()
                if "Adwords" in platforms:
                    ad = data["adwords"]
                    platformOffer = PlatformOffer(offer.id, "adwords", ad["contract_type"],float(ad["contract_scale"] if ad["contract_scale"] else 0), ad["material"], ad["startTime"],ad["endTime"], str(ad["country"]), float(ad["price"] if ad["price"] else 0),float(ad["daily_budget"] if ad["daily_budget"] else 0), ad["daily_type"],float(ad["total_budget"] if ad["total_budget"] else 0), ad["total_type"], ad["distribution"],ad["authorized"], ad["named_rule"], ad["KPI"].encode('utf-8'), ad["settlement"].encode('utf-8'),ad["period"].encode('utf-8'), ad["remark"].encode('utf-8'), createdTime, updateTime)
                    db.session.add(platformOffer)
                    db.session.commit()
                    db.create_all()
                    for i in ad['country_detail']:
                        history = History(offer.id, int(user_id),platformOffer.id,"adwords", "default", createdTime, status=offer.status,country=i["country"], country_price=float(i["price"]), price=platformOffer.price,daily_budget=float(ad["daily_budget"] if ad["daily_budget"] else 0), daily_type=ad["daily_type"],total_budget=float(ad["total_budget"] if ad["total_budget"] else 0),  total_type=ad["total_type"],KPI=ad["KPI"], contract_type=ad["contract_type"],contract_scale=float(ad["contract_scale"] if ad["contract_scale"] else 0))
                        db.session.add(history)
                        db.session.commit()
                        db.create_all()
                if "Apple" in platforms:
                    ap = data["apple"]
                    platformOffer = PlatformOffer(offer.id, "apple", ap["contract_type"],float(ap["contract_scale"] if ap["contract_scale"] else 0), ap["material"], ap["startTime"],ap["endTime"], str(ap["country"]), float(ap["price"] if ap["price"] else 0),float(ap["daily_budget"] if ap["daily_budget"] else 0), ap["daily_type"],float(ap["total_budget"] if ap["total_budget"] else 0), ap["total_type"], ap["distribution"],ap["authorized"], ap["named_rule"], ap["KPI"].encode('utf-8'), ap["settlement"].encode('utf-8'),ap["period"].encode('utf-8'), ap["remark"].encode('utf-8'), createdTime, updateTime)
                    db.session.add(platformOffer)
                    db.session.commit()
                    db.create_all()
                    for i in ap['country_detail']:
                        history = History(offer.id, int(user_id),platformOffer.id,"apple", "default", createdTime, status=offer.status,country=i["country"], country_price=float(i["price"]), price=platformOffer.price,daily_budget=float(ap["daily_budget"] if ap["daily_budget"] else 0), daily_type=ap["daily_type"],total_budget=float(ap["total_budget"] if ap["total_budget"] else 0),  total_type=ap["total_type"],KPI=ap["KPI"], contract_type=ap["contract_type"],contract_scale=float(ap["contract_scale"] if ap["contract_scale"] else 0))
                        db.session.add(history)
                        db.session.commit()
                        db.create_all()
                return json.dumps({"code": 200, "message": "success", "offerId":offer.id})
            except Exception as e:
                return json.dumps({"code": 500, "message": e})

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
            sales = User.query.filter_by(id=int(i.user_id)).first()
            fb_offer = PlatformOffer.query.filter_by(offer_id=i.id,platform="facebook").all()
            contract_type = "cpa"
            startTime = "2017-01-01"
            endTime = "2017-12-31"
            country = "CN"
            price = 0
            for j in fb_offer:
                contract_type = j.contract_type
                if contract_type == "1":
                    contract_type = u"服务费"
                elif contract_type == "2":
                    contract_type = "cpa"
                if j.endTime >= (datetime.datetime.now() + datetime.timedelta(days=10950)).strftime("%Y-%m-%d %H:%M:%S"):
                    endTime = "TBD"
                else:
                    endTime = j.endTime
                startTime = j.startTime
                country = j.country
                price = j.price
            os = i.os
            app_name = i.app_name

            data = {
                "offer_id": i.id,
                "status": status,
                "contract_type": contract_type,
                "os": os,
                "customer_id": customerName,
                "app_name": app_name,
                "startTime": startTime,
                "endTime": endTime,
                "country": country,
                "price": price,
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
    plate = offer.platform

    fb_offer = PlatformOffer.query.filter_by(offer_id=int(id),platform="facebook").first()
    if fb_offer is not None:
        contract_type = fb_offer.contract_type
        if contract_type != "1":
            contract_scale = 0
        else:
            contract_scale = fb_offer.contract_scale
        facebook = {
            "contract_type": contract_type,
            "contract_scale": contract_scale,
            "material": fb_offer.material,
            "startTime": fb_offer.startTime,
            "endTime": fb_offer.endTime,
            "country": fb_offer.country,
            "price": fb_offer.price,
            "daily_budget": fb_offer.daily_budget,
            "daily_type": fb_offer.daily_type,
            "total_budget": fb_offer.total_budget,
            "total_type": fb_offer.total_type,
            "distribution": fb_offer.distribution,
            "authorized": fb_offer.authorized,
            "named_rule": fb_offer.named_rule,
            "KPI": fb_offer.KPI,
            "settlement": fb_offer.settlement,
            "period": fb_offer.period,
            "remark": fb_offer.remark
        }
        plate_country = PlatformOffer.query.filter_by(id=fb_offer.id).first()
        countries = plate_country.country
        countries = countries.split(',')
        countries = list(set(countries))
        country_detail = []
        for i in countries:
            historty = History.query.filter(History.offer_id == id, History.country == i, History.platformOffer_id == fb_offer.id).order_by(
                desc(History.createdTime)).first()
            if historty:
                country = historty.country
                country_price = historty.country_price
                detail = {
                    "country": country,
                    "price": country_price
                }
                country_detail += [detail]
        facebook["country_detail"] = country_detail
    else:
        facebook = {}

    ad_offer = PlatformOffer.query.filter_by(offer_id=int(id),platform="adwords").first()
    if ad_offer is not None:
        contract_type = ad_offer.contract_type
        if contract_type != "1":
            contract_scale = 0
        else:
            contract_scale = ad_offer.contract_scale
        adwords = {
            "contract_type": contract_type,
            "contract_scale": contract_scale,
            "material": ad_offer.material,
            "startTime": ad_offer.startTime,
            "endTime": ad_offer.endTime,
            "country": ad_offer.country,
            "price": ad_offer.price,
            "daily_budget": ad_offer.daily_budget,
            "daily_type": ad_offer.daily_type,
            "total_budget": ad_offer.total_budget,
            "total_type": ad_offer.total_type,
            "distribution": ad_offer.distribution,
            "authorized": ad_offer.authorized,
            "named_rule": ad_offer.named_rule,
            "KPI": ad_offer.KPI,
            "settlement": ad_offer.settlement,
            "period": ad_offer.period,
            "remark": ad_offer.remark
        }
        plate_country = PlatformOffer.query.filter_by(id=ad_offer.id).first()
        countries = plate_country.country
        countries = countries.split(',')
        countries = list(set(countries))
        country_detail = []
        for i in countries:
            historty = History.query.filter(History.offer_id == id, History.country == i, History.platformOffer_id == ad_offer.id).order_by(
                desc(History.createdTime)).first()
            country = historty.country
            country_price = historty.country_price
            detail = {
                "country": country,
                "price": country_price
            }
            country_detail += [detail]
        adwords["country_detail"] = country_detail
    else:
        adwords = {}

    ap_offer = PlatformOffer.query.filter_by(offer_id=int(id), platform="apple").first()
    if ap_offer is not None:
        contract_type = ap_offer.contract_type
        if contract_type != "1":
            contract_scale = 0
        else:
            contract_scale = ap_offer.contract_scale
        apple = {
            "contract_type": contract_type,
            "contract_scale": contract_scale,
            "material": ap_offer.material,
            "startTime": ap_offer.startTime,
            "endTime": ap_offer.endTime,
            "country": ap_offer.country,
            "price": ap_offer.price,
            "daily_budget": ap_offer.daily_budget,
            "daily_type": ap_offer.daily_type,
            "total_budget": ap_offer.total_budget,
            "total_type": ap_offer.total_type,
            "distribution": ap_offer.distribution,
            "authorized": ap_offer.authorized,
            "named_rule": ap_offer.named_rule,
            "KPI": ap_offer.KPI,
            "settlement": ap_offer.settlement,
            "period": ap_offer.period,
            "remark": ap_offer.remark
        }
        plate_country = PlatformOffer.query.filter_by(id=ap_offer.id).first()
        countries = plate_country.country
        countries = countries.split(',')
        countries = list(set(countries))
        country_detail = []
        for i in countries:
            historty = History.query.filter(History.offer_id == id, History.country == i, History.platformOffer_id == ap_offer.id).order_by(
                desc(History.createdTime)).first()
            country = historty.country
            country_price = historty.country_price
            detail = {
                "country": country,
                "price": country_price
            }
            country_detail += [detail]
        apple["country_detail"] = country_detail
    else:
        apple = {}

    result = {
        "customer_id": customer.company_name+"("+str(customer.id)+")",
        "status": offer.status,
        "contract_num": offer.contract_num,
        "user_id": user.name+"("+str(user.id)+")",
        "os": offer.os,
        "package_name": offer.package_name,
        "app_name": offer.app_name,
        "app_type": offer.app_type,
        "preview_link": offer.preview_link,
        "track_link": offer.track_link,
        "platform": str(plate),
        "email_time": offer.email_time,
        "email_users": offer.email_users,
        "email_tempalte": offer.email_template,
        "facebook": facebook,
        "adwords": adwords,
        "apple": apple
    }
    response = {
        "code": 200,
        "result": result,
        "message": "success"
    }
    return json.dumps(response)

#offer国家对应的价钱
@offers.route('/api/country_price/<offerId>', methods=["GET"])
def countryPrice(offerId):
    platform_offer = PlatformOffer.query.filter_by(offer_id=int(offerId),platform='facebook').first()
    countries = platform_offer.country
    countries = countries.split(',')
    countries = list(set(countries))
    country_price_list = []
    for i in countries:
        historty = History.query.filter(History.offer_id == int(offerId), History.country == i, History.platformOffer_id==platform_offer.id).order_by(desc(History.createdTime)).first()
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

#修改offer状态时对应的history的变化
def statusHistory(offer_id,platform_id,platform,status):
    offer = Offer.query.filter_by(id=offer_id).first()
    time_now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    platform_offer = PlatformOffer.query.filter_by(id=platform_id).first()
    historty = History(offer_id,offer.user_id,platform_id,platform,"update",time_now,status,price=platform_offer.price,daily_budget=platform_offer.daily_budget,daily_type=platform_offer.daily_type,total_budget=platform_offer.total_budget,total_type=platform_offer.total_type,KPI=platform_offer.KPI,contract_type=platform_offer.contract_type,contract_scale=platform_offer.contract_scale)
    db.session.add(historty)
    db.session.commit()
    db.create_all()
    return historty

#更新offer的状态
@offers.route('/api/update_offer_status/<offer_id>', methods=["GET","POST"])
@Permission.check(models=["offer_create","offer_edit","offer_query"])
def updateStatus(offer_id):
    offer = Offer.query.filter_by(id=int(offer_id)).first()
    if request.method == "GET":
        if offer.status == "active":
            offer.status = "inactive"
            db.session.add(offer)
            db.session.commit()

            return json.dumps({"code": 200, "message":"success"})
        elif offer.status == "inactive":
            offer.status = "active"
            db.session.add(offer)
            db.session.commit()

        platform_offer = PlatformOffer.query.filter_by(offer_id=offer.id).all()
        for i in platform_offer:
            platform = i.platform
            platform_id = i.id
            status = offer.status
            historty = statusHistory(offer.id, platform_id, str(platform), status)

        return json.dumps({"code": 200, "message": "success"})
    else:
        offer.status = "deleted"
        status = offer.status
        db.session.add(offer)
        db.session.commit()
        platform_offer = PlatformOffer.query.filter_by(offer_id=offer.id).all()
        for i in platform_offer:
            history = statusHistory(offer_id,i.id,str(i.platform),status)
        return json.dumps({"code": 200, "message": "success"})

#分平台更新offer信息
def updatePlatformOffer(offer_id,platform,data):
    platform_offer = PlatformOffer.query.filter_by(offer_id=int(offer_id),platform=platform).first()
    time_now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    offer = Offer.query.filter_by(id=offer_id).first()
    user_id = offer.user_id
    if data["price"] != "":
        price = float(data["price"])
    else:
        price = 0
    if data['daily_budget'] != "":
        daily_budget = float(data['daily_budget'])
    else:
        daily_budget = 0
    if data['total_budget'] != "":
        total_budget = float(data["total_budget"])
    else:
        total_budget = 0

    if platform_offer is not None:
        platform_offer.contract_type = data['contract_type']
        platform_offer.contract_scale = float(data['contract_scale'])
        platform_offer.material = data['material']
        platform_offer.startTime = data['startTime']
        platform_offer.endTime = data['endTime']
        platform_offer.country = data['country']
        platform_offer.price = price
        platform_offer.daily_budget = daily_budget
        platform_offer.daily_type = data['daily_type']
        platform_offer.total_budget = total_budget
        platform_offer.total_type = data['total_type']
        platform_offer.distribution = data['distribution']
        platform_offer.authorized = data['authorized']
        platform_offer.named_rule = data['named_rule']
        platform_offer.KPI = data['KPI']
        platform_offer.settlement = data['settlement']
        platform_offer.period = data['period']
        platform_offer.remark = data['remark']
        platform_offer.updateTime = time_now
        db.session.add(platform_offer)
        db.session.commit()

    else:
        platform_offer = PlatformOffer(int(offer_id),platform,data['contract_type'],float(data['contract_scale']),data['material'],data['startTime'],data['endTime'],data['country'],price,daily_budget,data['daily_type'],total_budget,data['total_type'],data['distribution'],data['authorized'],data['named_rule'],data['KPI'],data['settlement'],data['period'],data['remark'],time_now,time_now)
        db.session.add(platform_offer)
        db.session.commit()
        db.create_all()
    if data["country_detail"] != []:
        for i in data['country_detail']:
            history = History(offer_id, user_id,platform_offer.id,platform, "update",
                              time_now,offer.status, country=i["country"], country_price=float(i["price"]),
                              price=float(data["price"]) if data["price"] != "" else 0,
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
        history = History(offer_id, user_id,platform_offer.id, "update",time_now,offer.status,
                          price=float(data["price"]) if data["price"] != "" else 0,
                          daily_budget=float(data["daily_budget"]) if data["daily_budget"] != "" else 0,
                          daily_type=data["daily_type"],
                          total_budget=float(data["total_budget"]) if data['total_budget'] != "" else 0,
                          total_type=data["total_type"], KPI=data["KPI"],
                          contract_type=data["contract_type"],
                          contract_scale=float(data["contract_scale"]) if data["contract_scale"] != "" else 0)
        db.session.add(history)
        db.session.commit()
        db.create_all()
    return platform_offer

#编辑offer
@offers.route('/api/update_offer', methods=["POST", "GET"])
@Permission.check(models=["offer_create","offer_edit","offer_query"])
def updateOffer():
    if request.method == "POST":
        data = request.get_json(force=True)
        offer = Offer.query.filter_by(id=int(data["offer_id"])).first()
        if offer is not None:
            try:
                customer_id = data["customer_id"].split("(")[1].split(')')[0]
                user_id = data["user_id"].split("(")[1].split(')')[0]
                offer.updateTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                offer.status = data["status"] if data["status"] != "" else offer.status
                offer.customer_id = int(customer_id) if data["customer_id"] != "" else offer.customer_id
                offer.user_id = int(user_id) if data['user_id'] != "" else offer.user_id
                offer.contract_num = data["contract_num"] if data["contract_num"] != "" else offer.contract_num
                offer.os = data["os"] if data["os"] != "" else offer.os
                offer.package_name = data["package_name"] if data["package_name"] != "" else offer.package_name
                offer.app_name = data["app_name"] if data["app_name"] != "" else offer.app_name
                offer.app_type = data["app_type"] if data["app_type"] != "" else offer.app_type
                offer.preview_link = data["preview_link"] if data["preview_link"] != "" else offer.preview_link
                offer.track_link = data["track_link"] if data["track_link"] != "" else offer.track_link
                offer.platform = str(data["platform"]) if str(data["platform"]) != "" else offer.platform
                offer.email_time = data["email_time"]
                offer.email_users = str(data["email_users"]) if str(data["email_users"]) != "" else offer.email_users
                offer.email_template = data["email_tempalte"] if data["email_tempalte"] != "" else offer.email_template

                platforms = data["platform"].split(',')
                if 'Facebook' in platforms:
                    fb_data = data['facebook']
                    fb_offer = updatePlatformOffer(int(data["offer_id"]),'facebook',fb_data)
                if 'Adwords' in platforms:
                    ad_data = data['adwords']
                    ad_offer = updatePlatformOffer(int(data['offer_id']),'adwords',ad_data)
                if 'Apple' in platforms:
                    ap_data = data['apple']
                    ap_offer = updatePlatformOffer(int(data['offer_id']),'apple',ap_data)

                db.session.add(offer)
                db.session.commit()

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
        if data["type"] == "facebook":
            token = "EAAHgEYXO0BABABt1QAdnb4kDVpgDv0RcA873EqcNbHFeN8IZANMyXZAU736VKOj1JjSdOPk2WuZC7KwJZBBD76CUbA09tyWETQpOd5OCRSctIo6fuj7cMthZCH6pZA6PZAFmrMgGZChehXreDa3caIZBkBwkyakDAGA4exqgy2sI7JwZDZD"

            advertisers = Advertisers(token,int(data["offer_id"]), type=data["type"], facebook_keywords=data["advertise_series"], facebook_accountId=data["advertise_groups"], createdTime=createdTime, updateTime=updateTime)
        elif data["type"] == "apple":
            advertisers = Advertisers("",int(data["offer_id"]),"apple",apple_appname=data["advertise_series"],createdTime=createdTime,updateTime=updateTime)
        else:
            advertisers = Advertisers("", int(data["offer_id"]), "adwords", adwords_notuac=data["advertise_series"], adwords_uac=data["advertise_groups"],createdTime=createdTime,updateTime=updateTime)
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

    advertiser_apple = Advertisers.query.filter_by(offer_id=int(offer_id), type="apple").first()
    if advertiser_apple:
        advertise_series_apple = advertiser_apple.apple_appname
        advertise_groups_apple = ""
        type_apple = advertiser_apple.type
        result_apple = {
            "apple_id": advertiser_apple.id,
            "advertise_series": advertise_series_apple,
            "advertise_groups": advertise_groups_apple,
            "type": type_apple
        }
    else:
        result_apple = {}

    response = {
        "facebook": result_facebook,
        "adwords": result_adwords,
        "apple": result_apple,
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
        advertise = Advertisers.query.filter_by(id=int(data["ad_id"]),type=data["type"]).first()

        updateTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        try:
            if data["type"] == "facebook":
                advertise.facebook_keywords = data["advertise_series"]
                advertise.facebook_accountId = data["advertise_groups"]
            elif data["type"] == "adwords":
                advertise.adwords_notuac = data["advertise_series"]
                advertise.adwords_uac = data["advertise_groups"]
            else:
                advertise.apple_appname = data['advertise_series']
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
        bind_advertisers = Advertisers.query.filter_by(offer_id=offerId,type="facebook").first()
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
        platform = data["platform"]
        if flag == "country_detail":
            country = []
            result = []
            history = History.query.filter(History.offer_id == offer_id, History.country != "", History.platform == platform)
            for i in history:
                country.append(i.country)
            country = list(set(country))
            for i in country:
                history_country = History.query.filter(History.offer_id == offer_id, History.country == i, History.platform == platform)
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
                history = History.query.filter(History.offer_id == offer_id, History.contract_type != "",History.platform == platform)
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
                history = History.query.filter(History.offer_id == offer_id, History.price != "",History.platform == platform)
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
                history = History.query.filter(History.offer_id == offer_id, History.daily_budget != "",History.platform == platform)
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
                history = History.query.filter(History.offer_id == offer_id, History.total_budget != "",History.platform == platform)
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
                history = History.query.filter(History.offer_id == offer_id, History.total_budget != "",History.platform == platform)
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
@offers.route("/api/country_time/create/<platform>", methods=["POST", "GET"])
def createCountryTime(platform):
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

                time_Price = TimePrice.query.filter_by(offer_id=int(offer_id), country_id=coun.id, date=time_coun, platform=platform).first()
                if time_Price:
                    time_Price.price = price
                    db.session.add(time_Price)
                    db.session.commit()
                else:
                    timePrice = TimePrice(int(offer_id), coun.id, platform, time_coun, price)
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
        offer_platform = offerId.split("_")
        offer_id = offer_platform[0]
        platform = offer_platform[1]
        for i in data:
            for j in range(len(i["time"])):
                time_coun = i["time"][j]
                try:
                    price = '%0.2f' % (i["date"][j])
                except Exception as e:
                    print e
                country = i['country']
                coun = Country.query.filter_by(shorthand=country).first()

                time_Price = TimePrice.query.filter_by(offer_id=int(offer_id),country_id=coun.id,date=time_coun,platform=platform).first()
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
            timePrices = TimePrice.query.filter(TimePrice.country_id == countryId, TimePrice.offer_id == int(data["offer_id"]), TimePrice.platform == data["platform"]).all()
            for t in timePrices:
                dateCurrent.append(t.date)
            for i in dateList:
                if i in dateCurrent:
                    timePrice = TimePrice.query.filter_by(country_id=countryId, date=i, offer_id=int(data["offer_id"]),platform=data["platform"]).first()
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
    platform = data["platform"]
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
            timePrice = TimePrice.query.filter_by(country_id=countryId, date=i["date"], offer_id=offer_id, platform=platform).first()
            if timePrice:
                timePrice.price = i["price"]
                try:
                    db.session.add(timePrice)
                    db.session.commit()
                except Exception as e:
                    print e
                    return json.dumps({"code": 500, "message": "fail"})
            else:
                timePriceNew = TimePrice(offer_id,countryId, platform, i["date"], i["price"])
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

#合作模式日历部分
@offers.route('/api/contract', methods=["POST","GET"])
def contract():
    data = request.get_json(force=True)
    result = data["result"]
    platform = data["platform"]
    contract_type = data["contract_type"]
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
            cooperation = CooperationPer.query.filter_by( date=i["date"], offer_id=int(offer_id), platform=platform).first()
            if cooperation:
                cooperation.contract_scale = float(i["price"])
                cooperation.contract_type = contract_type
                try:
                    db.session.add(cooperation)
                    db.session.commit()
                except Exception as e:
                    print e
                    return json.dumps({"code": 500, "message": "fail"})
            else:
                createdTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                cooperation = CooperationPer(int(offer_id), platform, contract_type, float(i["price"]),i["date"],createdTime)
                try:
                    db.session.add(cooperation)
                    db.session.commit()
                    db.create_all()
                except Exception as e:
                    print e
                    return json.dumps({"code": 500, "message": "fail"})
        else:
            pass
    return json.dumps({"code": 200, "message": "success"})

@offers.route("/api/contract_show", methods=["POST", "GET"])
def showContract():
    if request.method == "POST":
        data = request.get_json(force=True)
        date = data['date']
        platform = data['platform']
        contract_type = data['contract_type']
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
            cooperation = CooperationPer.query.filter(CooperationPer.platform == platform, CooperationPer.offer_id == int(data["offer_id"]), CooperationPer.contract_type == contract_type).all()
            for t in cooperation:
                dateCurrent.append(t.date)
            for i in dateList:
                if i in dateCurrent:
                    cooperate = CooperationPer.query.filter_by(date=i, offer_id=int(data["offer_id"]),platform=platform,contract_type=contract_type).first()
                    detail = {
                        "date": i,
                        "price": cooperate.contract_scale
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
        sales = User.query.filter_by(id=int(i.user_id)).first()
        platform_offer = PlatformOffer.query.filter_by(offer_id=i.id,platform="facebook").first()
        if platform_offer:
            contract_type = platform_offer.contract_type
            if contract_type == "1":
                contract_type = u"服务费"
            elif contract_type == "2":
                contract_type = "cpa"
            if platform_offer.endTime >= (datetime.datetime.now() + datetime.timedelta(days=10950)).strftime("%Y-%m-%d %H:%M:%S"):
                endTime = "TBD"
            else:
                endTime = platform_offer.endTime
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
                    "startTime": platform_offer.startTime,
                    "endTime": endTime,
                    "country": str(platform_offer.country),
                    "price": platform_offer.price,
                    "updateTime": i.updateTime,
                    "sale_name": sales.name
                }
            ]
    return offer_result_list
