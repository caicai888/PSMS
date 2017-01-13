# -*- coding: utf-8 -*-
from datetime import datetime
from main import db


# 用户,角色关联表
class UserRole(db.Model):
    __tablename__ = 'user_role'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    role_id = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id


# 角色,权限关联表
class RolePermissions(db.Model):
    __tablename__ = 'role_permissions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    permissions_id = db.Column(db.String(100), nullable=False)

    def __init__(self, role_id, permissions_id):
        self.role_id = role_id
        self.permissions_id = permissions_id


# 用户,权限关联表
class UserPermissions(db.Model):
    __tablename__ = 'user_permissions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    permissions_id = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, permissions_id):
        self.user_id = user_id
        self.permissions_id = permissions_id


# 用户表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    passwd = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    last_datetime = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, email, passwd, phone):
        self.name = name
        self.email = email
        self.passwd = passwd
        self.phone = phone

    def __repr__(self):
        user = ''
        user += 'name: %s\n' % (self.name)
        return user


# 角色表
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    last_datetime = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name):
        self.name = name


# 权限表
class Permissions(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name


# 客户表
class Customers(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(100), nullable=False, unique=True)
    company_name = db.Column(db.String(100), nullable=False, unique=True)
    company_address = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    last_datetime = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(100), nullable=False, default='Created')

    def __init__(self, customer_code, company_name, company_address, comment, status):
        self.customer_code = customer_code
        self.company_name = company_name
        self.company_address = company_address
        self.comment = comment
        self.status = status

    def __repr__(self):
        customer_code = ''
        customer_code += 'name: %s\n' % (self.customer_code)
        return customer_code


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 销售
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))  # 客户
    status = db.Column(db.String(100), default='active')
    contract_type = db.Column(db.String(100))  # 合同模式
    contract_num = db.Column(db.String(100), nullable=False)  # 合同编号
    contract_scale = db.Column(db.Float, default=0)  # 合同模式为服务费时存在
    os = db.Column(db.String(100), nullable=True)  # 操作系统　
    package_name = db.Column(db.String(1000), nullable=True)  # 包名
    app_name = db.Column(db.String(1000), nullable=True)
    app_type = db.Column(db.String(1000), nullable=True)
    preview_link = db.Column(db.String(1000), nullable=True)
    track_link = db.Column(db.String(1000), nullable=True)
    material = db.Column(db.String(100), default="yes")
    startTime = db.Column(db.String(100), nullable=False)  # 投放开始时间
    endTime = db.Column(db.String(100), nullable=False)  # 投放结束时间
    platform = db.Column(db.String(100), nullable=False)  # 投放平台
    country = db.Column(db.String(500), nullable=False)  # 投放国家
    price = db.Column(db.Float, default=0)  # 投放单价
    daily_budget = db.Column(db.Float, default=0)  # 最高日预算
    daily_type = db.Column(db.String(100), default='install')  # 最高日预算的类型
    total_budget = db.Column(db.Float, default=0)  # 最高总预算
    total_type = db.Column(db.String(100), default='cost')  # 最高总预算的类型
    distribution = db.Column(db.String(100), nullable=True)  # 预算分配
    authorized = db.Column(db.String(500), nullable=True)  # 授权账户
    named_rule = db.Column(db.String(1000), nullable=True)  # 命名规则
    KPI = db.Column(db.String(1000), nullable=True)  # kpi要求
    settlement = db.Column(db.String(1000), nullable=True)  # 结算标准
    period = db.Column(db.String(1000), nullable=True)  # 账期
    remark = db.Column(db.String(1000), nullable=True)  # 备注
    email_time = db.Column(db.String(100), nullable=True)  # 邮件发送时间
    email_users = db.Column(db.String(500), nullable=True)  # 邮件收件人
    email_tempalte = db.Column(db.Integer, nullable=True)  # 报告模版
    createdTime = db.Column(db.String(100), nullable=False)
    updateTime = db.Column(db.String(100), nullable=False)
    historys = db.relationship('History', backref='offer', lazy='dynamic')

    def __init__(self, user_id, customer_id, status="active", contract_type=None, contract_num=None, contract_scale=0,
                 os=None, package_name=None, app_name=None, app_type=None, preview_link=None, track_link=None,
                 material="yes", startTime=None, endTime=None, platform=None, country=None, price=0, daily_budget=0,
                 daily_type="install", total_budget=0, total_type="cost", distribution=None, authorized=None,
                 named_rule=None, KPI=None, settlement=None, period=None, remark=None, email_time=None, email_users=None,
                 email_tempalte=1, createdTime=None, updateTime=None):
        self.user_id = user_id
        self.customer_id = customer_id
        self.status = status
        self.contract_type = contract_type
        self.contract_num = contract_num
        self.contract_scale = contract_scale
        self.os = os
        self.package_name = package_name
        self.app_name = app_name
        self.app_type = app_type
        self.preview_link = preview_link
        self.track_link = track_link
        self.material = material
        self.startTime = startTime
        self.endTime = endTime
        self.platform = platform
        self.country = country
        self.price = price
        self.daily_budget = daily_budget
        self.daily_type = daily_type
        self.total_budget = total_budget
        self.total_type = total_type
        self.distribution = distribution
        self.authorized = authorized
        self.named_rule = named_rule
        self.KPI = KPI
        self.settlement = settlement
        self.period = period
        self.remark = remark
        self.email_time = email_time
        self.email_users = email_users
        self.email_tempalte = email_tempalte
        self.createdTime = createdTime
        self.updateTime = updateTime

    def __repr__(self):
        return '<Offer {}>'.format(self.id)


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(100), default='default')
    status = db.Column(db.String(100), nullable=False)
    createdTime = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=True)
    country_price = db.Column(db.Float, nullable=True)
    price = db.Column(db.Float, default=0)
    daily_budget = db.Column(db.Float, default=0)  # 最高日预算
    daily_type = db.Column(db.String(100), nullable=True)
    total_budget = db.Column(db.Float, default=0)
    total_type = db.Column(db.String(100), nullable=True)  # 最高总预算的类型
    KPI = db.Column(db.String(100), nullable=True)  # kpi要求
    contract_type = db.Column(db.String(100), nullable=True)  # 合同模式
    contract_scale = db.Column(db.Float, default=0)  # 合同模式为服务费时存在

    def __init__(self, offer_id, user_id, type, createdTime, status=None, country=None, country_price=0, price=0,
                 daily_budget=0, daily_type=None, total_budget=0, total_type=None, KPI=None, contract_type=None,
                 contract_scale=None):
        self.offer_id = offer_id
        self.user_id = user_id
        self.type = type
        self.createdTime = createdTime
        self.status = status
        self.country = country
        self.country_price = country_price
        self.price = price
        self.daily_budget = daily_budget
        self.daily_type = daily_type
        self.total_type = total_type
        self.total_budget = total_budget
        self.KPI = KPI
        self.contract_scale = contract_scale
        self.contract_type = contract_type

    def __repr__(self):
        return '<History {}>'.format(self.id)


# 国家编码
class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    shorthand = db.Column(db.String(100), nullable=False)  # 两位字母简写
    british = db.Column(db.String(100), nullable=False)  # 英文全称
    chinese = db.Column(db.String(100), nullable=False)  # 中文

    def __init__(self, shorthand, british, chinese):
        self.shorthand = shorthand
        self.british = british
        self.chinese = chinese

    def __repr__(self):
        return '<Country {}>'.format(self.id)


class TimePrice(db.Model):
    __tablename__ = 'timePrice'
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    date = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, offer_id, country_id, date, price):
        self.offer_id = offer_id
        self.country_id = country_id
        self.date = date
        self.price = price

    def __repr__(self):
        return '<TimePrice {}>'.format(self.id)

class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100), nullable=False)
    accessToken = db.Column(db.String(10000), nullable=False)

    def __init__(self, account, accessToken):
        self.account = account
        self.accessToken = accessToken

    def __repr__(self):
        return '<Token {}>'.format(self.id)

class Advertisers(db.Model):
    __tablename__ = 'advertisers'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(10000), nullable=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    type = db.Column(db.String(100), default="facebook")
    advertise_series = db.Column(db.String(100), nullable=True)
    advertise_groups = db.Column(db.String(100), nullable=True)
    createdTime = db.Column(db.String(100), nullable=False)
    updateTime = db.Column(db.String(100), nullable=False)

    def __init__(self, token, offer_id, type="facebook", advertise_series=None, advertise_groups=None,createdTime=None,updateTime=None):
        self.token = token
        self.offer_id = offer_id
        self.type = type
        self.advertise_series = advertise_series
        self.advertise_groups = advertise_groups
        self.createdTime = createdTime
        self.updateTime = updateTime

    def __repr__(self):
        return '<Advertisers {}>'.format(self.id)
