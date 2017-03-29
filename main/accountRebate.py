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
        print 'Get data from web:',data
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
        else:
            oldRebate = Rebate.query.filter_by(id=int(rebateId)).first()
            if oldRebate:
                oldRebate.scale = float(scale)
                db.session.add(oldRebate)
                db.session.commit()
                return json.dumps({"code": 200, "message": "success"})
            else:
                return json.dumps({"code": 500, "message": "not exists"})

@accountRebate.route('/api/rebate/show', methods=['GET','POST'])
def show_rebate():
    rebates = Rebate.query.all()
    rebate_lists = []
    print '************',rebates
    for i in rebates:
        rebate_lists += [
            {
                "accountName": i.accountName,
                "scale": str(i.scale),
                "id": i.id,
                "keywords": i.keywords,
                "companyName": i.companyName,
                "address": i.address,
                "bank_account": i.bank_account,
                "concordat_code": i.concordat_code,
                "remark": i.remark,
                "platform": i.platform
            }
        ]
    print 'Return to webdatas : ', rebate_lists
    return json.dumps({"code":200,"message":"success","results": rebate_lists})
@accountRebate.route('/api/rebate/show/<id>', methods=['GET','POST'])
def show_rebate_detail(id):
    rebate = Rebate.query.filter_by(id=int(id)).first()
    return json.dumps({"code":200,"message":"success", "accountId": rebate.accountId,"scale": str(rebate.scale)})