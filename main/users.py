# -*- coding: utf-8 -*-
import base64
from datetime import datetime

from flask import Flask, Blueprint, request, session
import json

from main import db
from main.models import User, Role, UserRole, RolePermissions, UserPermissions

users = Blueprint('users', __name__)


# 获取所有用户
@users.route('/api/users', methods=['POST', 'GET'])
def get_users():
    if request.method == "GET":
        users = User.query.all()
        result = []
        for user in users:
            role = ''
            role_list = db.session.query(UserRole).filter_by(user_id=user.id).first()
            for role_id in role_list.role_id.split(','):
                role += db.session.query(Role).filter_by(id=int(role_id)).first().name + ','
            data = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": role[:-1],
                "phone": user.phone,
                "last_datetime": str(user.last_datetime)
            }
            result += [data]
        return json.dumps({"code": "200", "message": "success", "results": result})
    return json.dumps({"code": "500", "message": "request method error"})


# 创建用户
@users.route('/api/user/create', methods=['POST', 'GET'])
def create_user():
    if request.method == "POST":
        data = request.get_json(force=True)
        if db.session.query(User).filter_by(email=data["email"]).first():
            return json.dumps({"code": "500", "message": "user has exist"})
        user = User(data["name"], data["email"], base64.encodestring(data["passwd"]), data["phone"])
        db.session.add(user)
        db.session.commit()
        userid = db.session.query(User).filter_by(email=data["email"]).first().id
        session["user_id"] = userid

        # 存用户权限表
        user_permission = UserPermissions(userid, data['permission_ids'])
        db.session.add(user_permission)
        db.session.commit()
        # 存用户角色表
        user_permission = UserRole(userid, data['role_ids'])
        db.session.add(user_permission)
        db.session.commit()
        return json.dumps({"code": "200", "message": "success", "results": session["user_id"]})
    return json.dumps({"code": "500", "message": "request method error"})


# 编辑用户
@users.route('/api/user/do_edit/<id>', methods=['POST', 'GET'])
def do_edit_user(id):
    if request.method == "POST":
        user = db.session.query(User).filter_by(id=id).first()
        msg = {}
        msg['id'] = user.id
        msg['name'] = user.name
        msg['email'] = user.email
        msg['passwd'] = base64.decodestring(user.passwd)
        msg['phone'] = user.phone
        msg['role_ids'] = db.session.query(UserRole).filter_by(user_id=id).first().role_id
        msg['permission_ids'] = db.session.query(UserPermissions).filter_by(user_id=id).first().permissions_id
        return json.dumps({"code": "200", "message": "success", "results": msg})
    return json.dumps({"code": "500", "message": "request method error"})


# 编辑用户
@users.route('/api/user/edit/<id>', methods=['POST', 'GET'])
def edit_user(id):
    if request.method == "POST":
        data = request.get_json(force=True)
        if not db.session.query(User).filter_by(id=id).first():
            return json.dumps({"code": "500", "message": "user name is not exist"})
        user = db.session.query(User).filter_by(id=id).first()
        user.name = data["name"]
        user.email = data["email"]
        user.passwd = base64.encodestring(data["passwd"])
        user.phone = data["phone"]
        db.session.add(user)
        db.session.commit()

        # 用户角色表
        user_role = db.session.query(UserRole).filter_by(user_id=id).first()
        db.session.add(user_role)
        user_role.role_id = data['role_ids']
        db.session.commit()
        # 用户权限表
        user_permission = db.session.query(UserPermissions).filter_by(user_id=id).first()
        user_permission.permissions_id = data['permission_ids']
        db.session.commit()
        return json.dumps({"code": "200", "message": "success"})
    return json.dumps({"code": "500", "message": "request method error"})


# 用户登录
@users.route('/api/user/login', methods=['POST', 'GET'])
def login_in():
    if request.method == "POST":
        data = request.get_json(force=True)
        user = db.session.query(User).filter_by(email=data["email"]).first()
        if user:
            user_id = db.session.query(User).filter_by(email=data["email"]).first().id
            user.last_datetime = str(datetime.now())
            if data["passwd"] == base64.decodestring(user.passwd):
                session["user_id"] = user_id
                # 查出用户的所有信息
                datas = {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'passwd': base64.decodestring(user.passwd),
                    'phone': user.phone,
                    'last_datetime': str(datetime.now())
                }
                user.last_datetime = str(datetime.now())
                db.session.add(user)
                db.session.commit()
                return json.dumps({"code": "200", "message": "success", "results": datas})
            else:
                return json.dumps({"code": "500", "message": "password error!"})
        else:
            return json.dumps({"code": "500", "message": "user has not register"})


# 用户登出
@users.route('/api/user/logout', methods=['POST', 'GET'])
def login_out():
    if request.method == "GET":
        session.pop('user_id', None)
        return json.dumps({"code": "200", "message": "success"})
    return json.dumps({"code": "500", "message": "request method error"})


# 给前端用的接口,判断当前用户是否在登录状态
@users.route('/api/user/verify_session', methods=['POST', 'GET'])
def verify_session():
    if 'user_id' in session:
        user_id = session['user_id']
        user = db.session.query(User).filter_by(id=user_id).first()
        data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
        return json.dumps({"code": "200", "message": "success", "results": data})
    else:
        return json.dumps({"code": "500", "message": "please login in"})


# 给出所有权限的 json,前端需要,后期加新权限了,在这里增加一条
@users.route('/api/permissions', methods=['POST', 'GET'])
def get_all_permissions():
    data_dict = dict()
    data = {
        'dashboard': {'create': 11, 'delete': 12, 'edit': 13, 'query': 14},
        'report': {'create': 15, 'delete': 16, 'edit': 17, 'query': 18},
        'offer': {'create': 19, 'delete': 20, 'edit': 21, 'query': 22},
        'advertiser': {'create': 23, 'delete': 24, 'edit': 25, 'query': 26}
    }
    data_dict['code'] = '200'
    data_dict['message'] = 'success'
    data_dict['results'] = data
    return json.dumps(data_dict)


# 创建用户组
@users.route('/api/role/create', methods=['POST', 'GET'])
def create_role():
    if request.method == "POST":
        data = request.get_json(force=True)
        print data
        role = Role(data["name"])
        if db.session.query(Role).filter_by(name=data["name"]).first():
            return json.dumps({"code": "500", "message": "role had exits"})
        db.session.add(role)
        db.session.commit()
        role_id = role.id
        role_permissions = RolePermissions(role_id, data['permission_ids'])
        db.session.add(role_permissions)
        db.session.commit()
        return json.dumps({"code": "200", "message": "success"})
    return json.dumps({"code": "500", "message": "request method error"})


# 查出所有的用户组
@users.route('/api/roles', methods=['POST', 'GET'])
def get_all_roles():
    roles = Role.query.all()
    msg_dict = {}
    msg_list = []
    for role in roles:
        data = {
            'id': role.id,
            'name': role.name,
            'last_datetime': str(role.last_datetime)
        }
        msg_list += [data]
    msg_dict['code'] = '200'
    msg_dict['message'] = 'success'
    msg_dict['results'] = msg_list
    return json.dumps(msg_dict)


# 编辑用户组
@users.route('/api/role/do_edit/<id>', methods=['POST', 'GET'])
def do_edit_role(id):
    if request.method == "POST":
        msg_dict = dict()
        role = db.session.query(Role).filter_by(id=id).first()
        role_permission = db.session.query(RolePermissions).filter_by(role_id=id).first()
        msg_dict['code'] = '200'
        msg_dict['message'] = 'success'
        msg_dict['results'] = {}
        msg_dict['results']['id'] = id
        msg_dict['results']['name'] = role.name
        msg_dict['results']['permission_ids'] = role_permission.permissions_id
        return json.dumps(msg_dict)
    else:
        return json.dumps({"code": "500", "message": "request method error"})


# 编辑用户组
@users.route('/api/role/edit/<id>', methods=['POST', 'GET'])
def edit_role(id):
    if request.method == "POST":
        data = request.get_json(force=True)
        role = db.session.query(Role).filter_by(id=id).first()
        role.name = data['name']
        role_permission = db.session.query(RolePermissions).filter_by(role_id=id).first()
        role_permission.permissions_id = data['permission_ids']
        role.last_datetime = str(datetime.now())
        db.session.commit()
        return json.dumps({"code": "200", "message": "success"})
    else:
        return json.dumps({"code": "500", "message": "request method error"})


# 查出当前组所有的权限
@users.route('/api/role_permissions/<id>', methods=['POST', 'GET'])
def get_role_permissions(id):
    permissions = db.session.query(RolePermissions).filter_by(role_id=id).first()
    permissions_list = permissions.permissions_id
    data = {
        'code': '200',
        'message': 'success',
        'results': {'permission_ids': permissions_list}
    }
    return json.dumps(data)
