# -*- coding: utf-8 -*-
from __future__ import division
from flask import Blueprint, request
from main import db
from main.models import Rebate,Optimization
import json
import datetime

accountRebate = Blueprint('accountRebate', __name__)

@accountRebate.route('/api/rebate/create', methods=['POST','GET'])
def create_rebate():
    if request.method == "POST":
        data = request.get_json(force=True)
        accountId = data['accountId']
        scale = data['scale']
        rebate = Rebate(accountId,float(scale))
        db.session.add(rebate)
        db.session.commit()
        db.create_all()

        return json.dumps({"code": 200, "message": "success", "rebateId":rebate.id})

@accountRebate.route('/api/rebate/update', methods=["POST","GET"])
def update_rebate():
    if request.method == "POST":
        data = request.get_json(force=True)
        rebateId = data['rebateId']
        scale = data['scale']

        oldRebate = Rebate.query.filter_by(id=rebateId).first()
        if oldRebate:
            oldRebate.scale = float(scale)
            db.session.add(oldRebate)
            db.session.commit()

            return json.dumps({"code":200,"message":"success"})
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

#创建优化师对应关系
@accountRebate.route('/api/opt/create', methods=['POST','GET'])
def optCreate():
    if request.method == "POST":
        data = request.get_json(force=True)
        simple = data["simple"]
        name = data["name"]
        time_now = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
        optimiziton = Optimization.query.filter_by(simple=simple).first()
        if optimiziton:
            return json.dumps({"code":500,"message":u"该代码已经被占用!"})
        else:
            optimiziton_add = Optimization(simple=simple,name=name,createdTime=time_now)
            db.session.add(optimiziton_add)
            db.session.commit()
            db.create_all()

            return json.dumps({"code":200,"message":"success","optId":optimiziton_add.id})

#跟新优化师对应关系
@accountRebate.route('/api/opt/update', methods=["POST","GET"])
def optUpdate():
    if request.method == "POST":
        data = request.get_json(force=True)
        optId = data["optId"]
        simple = data["simple"]
        name = data['name']

        simple_sql = Optimization.query.filter_by(simple=simple).first()
        if simple_sql:
            return json.dumps({"code":500,"message":u"该代码已经被占用!"})
        else:
            optimization_new = Optimization.query.filter_by(id=int(optId))
            optimization_new.simple = simple
            optimization_new.name = name
            db.session.add(optimization_new)
            db.session.commit()

            return json.dumps({"code": 200, "message": "success"})