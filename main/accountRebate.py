# -*- coding: utf-8 -*-
from __future__ import division
from flask import Blueprint, request
from main import db
from main.models import Rebate
import json

accountRebate = Blueprint('accountRebate', __name__)

@accountRebate.route('/api/rebate/create', methods=['POST','GET'])
def create_rebate():
    print request.method
    if request.method == "POST":
        data = request.get_json(force=True)
        accountName = data['accountName']
        scale = data['scale']
        platform = data['platform']
        companyName = data['companyName']
        company_address = data['company_address']
        bank_account = data['bank_account']
        concordat_code = data['concordat_code']
        keywords = data['keywords']
        remark = data['remark']
        rebateId = data['rebateId']

        if rebateId == "":
            rebate = Rebate(accountName, float(scale),keywords,companyName,company_address,bank_account,concordat_code,remark,platform)
            db.session.add(rebate)
            db.session.commit()
            db.create_all()
            return json.dumps({"code": 200, "message": "success", "rebateId": rebate.id})
        else: #修改前端传过来的数据
            oldRebate = Rebate.query.filter_by(id=int(rebateId)).first()
            if oldRebate:
                oldRebate.scale = float(scale)
                oldRebate.platform = platform
                oldRebate.companyName = companyName
                oldRebate.address = company_address
                oldRebate.bank_account = bank_account
                oldRebate.concordat_code = concordat_code
                oldRebate.keywords = keywords
                oldRebate.remark = remark

                db.session.add(oldRebate)
                db.session.commit()
                return json.dumps({"code": 200, "message": "success"})
            else:
                return json.dumps({"code": 500, "message": "not exists"})

#展示数据
@accountRebate.route('/api/rebate/show', methods=['GET','POST'])
def show_rebate():
    rebates = Rebate.query.all()
    rebate_lists = []
    for i in rebates:
        rebate_lists += [
            {
                "accountName": i.accountName,
                "scale": str(i.scale),
                "id": i.id,
                "keywords": i.keywords,
                "companyName": i.companyName,
                "company_address": i.address,
                "bank_account": i.bank_account,
                "concordat_code": i.concordat_code,
                "remark": i.remark,
                "platform": i.platform
            }
        ]
    return json.dumps({"code":200,"message":"success","results": rebate_lists})

#展示详情
@accountRebate.route('/api/rebate/show/<id>', methods=['GET','POST'])
def show_rebate_detail(id):
    rebate = Rebate.query.filter_by(id=int(id)).first()
    return json.dumps({"code": 200, "message": "success", "accountName": rebate.accountName, "scale": str(rebate.scale),
                       "companyName": rebate.companyName, "company_address": rebate.address, "bank_account": rebate.bank_account,
                       "concordat_code": rebate.concordat_code, "remark": rebate.remark, "platform": rebate.platform,
                       "keywords": rebate.keywords})
