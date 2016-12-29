# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from flask import Flask, Blueprint, request

from main import db
from main.models import Customers
import json

customers = Blueprint('customers', __name__)


# 创建客户
@customers.route('/api/customers/create', methods=['POST', 'GET'])
def create_customer():
    if request.method == "POST":
        data = request.get_json(force=True)
        code = uuid.uuid1()
        customer_code = str(code).upper()[:8]
        if db.session.query(Customers).filter_by(company_name=data["company_name"]).first():
            return json.dumps({"code": "500", "message": "customer has exits"})
        customer = Customers(customer_code, data["company_name"], data['company_address'], data['comment'], 'Created')
        db.session.add(customer)
        db.session.commit()
        db.create_all()
        return json.dumps({"code": "200", "message": "success"})
    return json.dumps({"code": "500", "message": "request method error"})


# 查询所有客户
@customers.route('/api/customers', methods=['POST', 'GET'])
def customer():
    if request.method == "GET":
        customers = Customers.query.all()
        msg_list = []
        for customer in customers:
            data = {
                'customers_id': customer.id,
                'customer_code': customer.customer_code,
                'company_name': customer.company_name,
                'company_address': customer.company_address,
                'comment': customer.comment,
                'last_datetime': str(customer.last_datetime),
                'status': customer.status
            }
            msg_list += [data]
        created_list = []
        for msg in msg_list:
            if msg['status'] == 'Created':
                created_list.append(msg)
        data = {}
        data['code'] = '200'
        data['message'] = 'success'
        data['results'] = created_list
        return json.dumps(data)
    return json.dumps({"code": "500", "message": "request method error"})


# 当前客户详情
@customers.route('/api/customers/query/<id>', methods=['POST', 'GET'])
def query_customer(id):
    if request.method == "GET":
        customer = db.session.query(Customers).filter_by(id=id).first()
        data = {}
        data['code'] = '200'
        data['message'] = 'success'
        data['results'] = {'customer_code': customer.customer_code, 'company_name': customer.company_name,
                           'company_address': customer.company_address, 'comment': customer.comment,
                           'last_datetime': str(customer.last_datetime)
                           }
        return json.dumps(data)
    return json.dumps({"code": "500", "message": "request method error"})


# 编辑用户详情
@customers.route('/api/customers/edit/<id>', methods=['POST', 'GET'])
def edit_customer(id):
    if request.method == "POST":
        data = request.get_json(force=True)
        customer = db.session.query(Customers).filter_by(id=id).first()
        if customer:
            customer.company_name = data['company_name']
            customer.company_address = data['company_address']
            customer.comment = data['comment']
            customer.last_datetime = str(datetime.now())
            db.session.commit()
            return json.dumps({"code": "200", "message": "success"})
        else:
            return json.dumps({"code": "500", "message": "don't have this data"})
    return json.dumps({"code": "500", "message": "request method error"})


# 删除当前客户
@customers.route('/api/customers/delete/<id>', methods=['POST', 'GET'])
def delete_customer(id):
    if request.method == "POST":
        customer = db.session.query(Customers).filter_by(id=id).first()
        customer.status = 'Deleted'
        db.session.commit()
        return json.dumps({"code": "200", "message": "success"})
    return json.dumps({"code": "500", "message": "request method error"})
