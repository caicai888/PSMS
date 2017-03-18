# -*- coding: utf-8 -*-
from __future__ import division
from flask import Blueprint, request
from main import db
from main.models import Rebate
import json

accountRebate = Blueprint('accountRebate', __name__)

@accountRebate.route('/api/rebate/create', methods=['POST','GET'])
def create_rebate():
    if request.method == "POST":
        data = request.get_json(force=True)
        accountId = data['accountId']
        scale = data['scale']
        rebateId = data['rebateId']
        if rebateId == "":
            rebate = Rebate(accountId,float(scale))
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
    for i in rebates:
        rebate_lists += [
            {
                "accountId": i.accountId,
                "scale": str(i.scale)
            }
        ]

    return json.dumps({"code":200,"message":"success","result": rebate_lists})
@accountRebate.route('/api/rebate/show/<id>', methods=['GET','POST'])
def show_rebate_detail(id):
    rebate = Rebate.query.filter_by(id=int(id)).first()
    return json.dumps({"code":200,"message":"success", "accountId": rebate.accountId,"scale": str(rebate.scale)})