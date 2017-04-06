# -*- coding: utf-8 -*-

from datetime import datetime,timedelta
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
    optName = db.Column(db.String(100), nullable=False)
    last_datetime = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, email, passwd, optName, phone):
        self.name = name
        self.email = email
        self.passwd = passwd
        self.optName = optName
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
    bank_account = db.Column(db.String(100),nullable=False)
    concordat_code = db.Column(db.String(100),nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    last_datetime = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(100), nullable=False, default='Created')

    def __init__(self, customer_code, company_name, company_address, bank_account=None, concordat_code=None, comment=None, status="Created"):
        self.customer_code = customer_code
        self.company_name = company_name
        self.company_address = company_address
        self.bank_account = bank_account
        self.concordat_code = concordat_code
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
    contract_num = db.Column(db.String(100), nullable=False)  # 合同编号
    os = db.Column(db.String(100), nullable=True)  # 操作系统　
    package_name = db.Column(db.String(1000), nullable=True)  # 包名
    app_name = db.Column(db.String(1000), nullable=True)
    app_type = db.Column(db.String(1000), nullable=True)
    preview_link = db.Column(db.String(1000), nullable=True)
    track_link = db.Column(db.String(1000), nullable=True)
    platform = db.Column(db.String(100), nullable=False)  # 投放平台
    email_time = db.Column(db.String(100), nullable=True)  # 邮件发送时间
    email_users = db.Column(db.String(500), nullable=True)  # 邮件收件人
    email_template = db.Column(db.String(100), nullable=True)  # 报告模版
    createdTime = db.Column(db.String(100), nullable=False)
    updateTime = db.Column(db.String(100), nullable=False)
    historys = db.relationship('History', backref='offer', lazy='dynamic')
    emailaccount = db.Column(db.String(100), nullable=True)  #True

    #邮件账户判断,在offer copy修改的时候不发送邮件，此时为空;创建offer时会包含邮件账户
    def __init__(self, user_id, customer_id, status="active", contract_num=None,os=None, package_name=None, app_name=None, app_type=None,
                 preview_link=None, track_link=None,platform=None,email_time=None, email_users=None,email_template=None, createdTime=None,
                 updateTime=None,emailaccount=None):

        self.user_id = user_id
        self.customer_id = customer_id
        self.status = status
        self.contract_num = contract_num
        self.os = os
        self.package_name = package_name
        self.app_name = app_name
        self.app_type = app_type
        self.preview_link = preview_link
        self.track_link = track_link
        self.platform = platform
        self.email_time = email_time
        self.email_users = email_users
        self.email_template = email_template
        self.createdTime = createdTime
        self.updateTime = updateTime
        self.emailaccount = emailaccount

    def __repr__(self):
        return '<Offer {}>'.format(self.id)

#分平台offer信息
class PlatformOffer(db.Model):
    __tablename__ = "platformOffer"
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    platform = db.Column(db.String(100), nullable=False)  #所属平台
    contract_type = db.Column(db.String(100), nullable=False)  # 合作模式 1代表服务费,2代表CPA
    contract_scale = db.Column(db.Float, default=0)  # 合作模式为服务费时存在,CPA时为0
    material = db.Column(db.String(100), default="yes")
    startTime = db.Column(db.String(100), nullable=False)  # 投放开始时间
    endTime = db.Column(db.String(100), nullable=False)  # 投放结束时间
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
    createdTime = db.Column(db.String(100), nullable=False)
    updateTime = db.Column(db.String(100), nullable=False)

    def __init__(self, offer_id,platform,contract_type,contract_scale,material="yes", startTime=None, endTime=None, country=None, price=0,
                 daily_budget=0,daily_type="install", total_budget=0, total_type="cost", distribution=None, authorized=None,
                 named_rule=None, KPI=None, settlement=None, period=None, remark=None, createdTime=None, updateTime=None):
        self.offer_id = offer_id
        self.platform = platform
        self.contract_type = contract_type
        self.contract_scale = contract_scale
        self.material = material
        self.startTime = startTime
        self.endTime = endTime
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
        self.createdTime = createdTime
        self.updateTime = updateTime

    def __repr__(self):
        return "<PlatformOffer {}>".format(self.id)

#合作模式的日历形式
class CooperationPer(db.Model):
    __tablename__ = "cooperationPer"
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(100), nullable=False)  #所属平台
    contract_type = db.Column(db.String(100), nullable=False)  # 合作模式 1代表服务费,2代表CPA
    contract_scale = db.Column(db.Float, default=0)  # 合作模式为服务费时存在,CPA时为0
    date = db.Column(db.String(100), nullable=False)
    createdTime = db.Column(db.String(100), nullable=False)

    def __init__(self, offer_id, platform, contract_type, contract_scale, date, createdTime):
        self.offer_id = offer_id
        self.platform = platform
        self.contract_type = contract_type
        self.contract_scale = contract_scale
        self.date = date
        self.createdTime = createdTime

    def __repr__(self):
        return '<CooperationPer {}>'.format(self.id)

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    platformOffer_id = db.Column(db.Integer, db.ForeignKey('platformOffer.id'))
    platform = db.Column(db.String(100), nullable=False)
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

    def __init__(self, offer_id, user_id,platformOffer_id,platform, type, createdTime, status=None, country=None, country_price=0, price=0,
                 daily_budget=0, daily_type=None, total_budget=0, total_type=None, KPI=None, contract_type=None,
                 contract_scale=None):
        self.offer_id = offer_id
        self.user_id = user_id
        self.platformOffer_id = platformOffer_id
        self.platform = platform
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
    platform = db.Column(db.String(100),nullable=False)
    date = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, offer_id, country_id, platform, date, price):
        self.offer_id = offer_id
        self.country_id = country_id
        self.platform = platform
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
    facebook_keywords = db.Column(db.Text, nullable=True)
    facebook_accountId = db.Column(db.Text, nullable=True)
    adwords_notuac = db.Column(db.Text, nullable=True)
    adwords_uac = db.Column(db.Text, nullable=True)
    apple_appname = db.Column(db.Text, nullable=True)
    createdTime = db.Column(db.String(100), nullable=False)
    updateTime = db.Column(db.String(100), nullable=False)

    def __init__(self, token, offer_id, type="facebook", facebook_keywords=None, facebook_accountId=None,adwords_notuac=None,adwords_uac=None,apple_appname=None,createdTime=None,updateTime=None):
        self.token = token
        self.offer_id = offer_id
        self.type = type
        self.facebook_keywords = facebook_keywords
        self.facebook_accountId = facebook_accountId
        self.adwords_notuac = adwords_notuac
        self.adwords_uac = adwords_uac
        self.apple_appname = apple_appname
        self.createdTime = createdTime
        self.updateTime = updateTime

    def __repr__(self):
        return '<Advertisers {}>'.format(self.id)

#数据固化
class DataSolidified(db.Model):
    __tablename__ = "dataSolidified"
    id = db.Column(db.Integer,primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    type = db.Column(db.String(100), nullable=False)
    revenue = db.Column(db.Float, nullable=True)
    profit = db.Column(db.Float, nullable=True)
    cost = db.Column(db.Float, nullable=True)
    impressions = db.Column(db.Integer, nullable=True)
    clicks = db.Column(db.Integer, nullable=True)
    conversions = db.Column(db.Integer, nullable=True)
    ctr = db.Column(db.String(100), nullable=True)
    cvr = db.Column(db.String(100), nullable=True)
    cpc = db.Column(db.String(100), nullable=True)
    cpi = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    rebate = db.Column(db.Float, nullable=True)
    createdTime = db.Column(db.String(100), nullable=True)

    def __init__(self,offer_id,type,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi,date,country,rebate,createdTime):
        self.offer_id = offer_id
        self.type = type
        self.revenue = revenue
        self.profit = profit
        self.cost = cost
        self.impressions = impressions
        self.clicks = clicks
        self.conversions = conversions
        self.ctr = ctr
        self.cvr = cvr
        self.cpc = cpc
        self.cpi = cpi
        self.date = date
        self.country = country
        self.rebate = rebate
        self.createdTime = createdTime

    def __repr__(self):
        return '<DataSolidified {}>'.format(self.id)

#拉取facebook,Apple数据到本地
class Datas(db.Model):
    __tablename__ = 'datas'
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    type = db.Column(db.String(100), nullable=False)
    revenue = db.Column(db.Float, nullable=True)
    profit = db.Column(db.Float, nullable=True)
    cost = db.Column(db.Float, nullable=True)
    impressions = db.Column(db.Integer, nullable=True)
    clicks = db.Column(db.Integer, nullable=True)
    conversions = db.Column(db.Integer, nullable=True)
    ctr = db.Column(db.String(100), nullable=True)
    cvr = db.Column(db.String(100), nullable=True)
    cpc = db.Column(db.String(100), nullable=True)
    cpi = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    rebate = db.Column(db.Float, nullable=True)
    updateTime = db.Column(db.String(100), nullable=True)

    def __init__(self,offer_id,type,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi,date,country,rebate,updateTime):
        self.offer_id = offer_id
        self.type = type
        self.revenue = revenue
        self.profit = profit
        self.cost = cost
        self.impressions = impressions
        self.clicks = clicks
        self.conversions = conversions
        self.ctr = ctr
        self.cvr = cvr
        self.cpc = cpc
        self.cpi = cpi
        self.date = date
        self.country = country
        self.rebate = rebate
        self.updateTime = updateTime

    def __repr__(self):
        return '<Dates {}>'.format(self.id)

#fb ap campaign维度data
class DataDetail(db.Model):
    __tablename__ = "dataDetail"
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    account_id = db.Column(db.String(100), nullable=False)
    campaignId = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    revenue = db.Column(db.Float, nullable=True)
    profit = db.Column(db.Float, nullable=True)
    cost = db.Column(db.Float, nullable=True)
    impressions = db.Column(db.Integer, nullable=True)
    clicks = db.Column(db.Integer, nullable=True)
    conversions = db.Column(db.Integer, nullable=True)
    ctr = db.Column(db.Float, nullable=True)
    cvr = db.Column(db.Float, nullable=True)
    cpc = db.Column(db.Float, nullable=True)
    cpi = db.Column(db.Float, nullable=True)
    date = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    rebate = db.Column(db.Float, nullable=True)
    optName = db.Column(db.String(100), nullable=True)
    updateTime = db.Column(db.String(100), nullable=True)

    def __init__(self,offer_id,account_id,campaignId,type,revenue,profit,cost,impressions,clicks,conversions,ctr,cvr,cpc,cpi,date,country,rebate,optName,updateTime):
        self.offer_id = offer_id
        self.account_id = account_id
        self.campaignId = campaignId
        self.type = type
        self.revenue = revenue
        self.profit = profit
        self.cost = cost
        self.impressions = impressions
        self.clicks = clicks
        self.conversions = conversions
        self.ctr = ctr
        self.cvr = cvr
        self.cpc = cpc
        self.cpi = cpi
        self.date = date
        self.country = country
        self.rebate = rebate
        self.optName = optName
        self.updateTime = updateTime

    def __repr__(self):
        return '<DataDetail {}>'.format(self.id)

#fb campaign id与name的对应表
class CampaignRelations(db.Model):
    __tablename__ = "campaignRelations"
    id = db.Column(db.Integer, primary_key=True)
    campaignId = db.Column(db.String(100), nullable=False)
    campaignName = db.Column(db.String(150), nullable=False)
    account_id = db.Column(db.String(100), nullable=False)
    optName = db.Column(db.String(100),nullable=False)  #优化师的代码
    account_name = db.Column(db.String(100),nullable=False)

    def __init__(self,campaignId,campaignName,account_id,optName,accountName):

        self.campaignId = campaignId
        self.campaignName = campaignName
        self.account_id = account_id
        self.optName = optName
        self.account_name = accountName


    def __repr__(self):
        return '<CampaignRelations {}>'.format(self.id)

#Apple search平台campaign与app name的对应表
class CampaignAppName(db.Model):
    __tablename__ = "campaignAppName"
    id = db.Column(db.Integer, primary_key=True)
    campaignId = db.Column(db.String(100), nullable=False)
    campaignName = db.Column(db.String(150), nullable=False)
    appId = db.Column(db.String(100), nullable=False)
    appName = db.Column(db.String(100), nullable=False)
    optName = db.Column(db.String(100), nullable=False)

    def __init__(self,campaignId,campaignName,appId,appName,optName):
        self.campaignId = campaignId
        self.campaignName = campaignName
        self.appId = appId
        self.appName = appName
        self.optName = optName

    def __repr__(self):
        return '<CampaignAppName {}>'.format(self.id)

#adwords平台数据
class Adwords(db.Model):
    __tablename__ = "adwords"
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    account_id = db.Column(db.String(100), nullable=False)
    is_UAC = db.Column(db.Integer,default=1)
    campaignId = db.Column(db.Integer, nullable=False)
    campaignName = db.Column(db.String(150), nullable=False)
    impressions = db.Column(db.String(100), nullable=True)
    clicks = db.Column(db.Integer, nullable=True)
    revenue = db.Column(db.Float, nullable=True)
    cost = db.Column(db.Float, nullable=True)
    profit = db.Column(db.Float, nullable=True)
    conversions = db.Column(db.String(100), nullable=True)
    cpc = db.Column(db.String(100), nullable=True)
    cvr = db.Column(db.String(100), nullable=True)
    cpi = db.Column(db.String(100), nullable=True)
    ctr = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    rebate = db.Column(db.Float, nullable=True)
    optName = db.Column(db.String(100), nullable=True)

    def __init__(self,offer_id,account_id,is_UAC,campaignId,campaignName,impressions,clicks,revenue,cost,profit,conversions,cpc,cvr,cpi,ctr,date,country,rebate,optName):
        self.offer_id = offer_id
        self.account_id = account_id
        self.is_UAC = is_UAC
        self.campaignId = campaignId
        self.campaignName = campaignName
        self.impressions = impressions
        self.clicks = clicks
        self.revenue = revenue
        self.cost = cost
        self.profit = profit
        self.conversions = conversions
        self.cpc = cpc
        self.cvr = cvr
        self.cpi = cpi
        self.ctr = ctr
        self.date = date
        self.country = country
        self.rebate = rebate
        self.optName = optName

    def __repr__(self):
        return '<Adwords {}>'.format(self.id)

#adwords非uac,国家编码对应表
class AdwordsGeo(db.Model):
    __tablename__="adwordsGeo"
    id = db.Column(db.Integer, primary_key=True)
    countryNumber = db.Column(db.String(100), nullable=True)
    countryName = db.Column(db.String(100), nullable=True)

    def __init__(self,countryNumber,countryName):
        self.countryNumber = countryNumber
        self.countryName = countryName

    def __repr__(self):
        return '<AdwordsGeo {}>'.format(self.id)

#Facebook返点的account与返点比列的对应表
class Rebate(db.Model):
    __tablename__="rebate"
    id = db.Column(db.Integer, primary_key=True)
    accountName = db.Column(db.String(100), nullable=True)
    scale = db.Column(db.Float, nullable=True)
    keywords = db.Column(db.String(100), nullable=True)
    companyName = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    bank_account = db.Column(db.String(100), nullable=True)
    concordat_code = db.Column(db.String(100), nullable=True)
    remark = db.Column(db.String(100), nullable=True)
    platform = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=True)
    createdTime = db.Column(db.String(100), nullable=True)


    def __init__(self,accountName, scale,keywords,companyName,address,bank_account,concordat_code,remark,platform,status="default",createdTime=None):
        createdTime = str(datetime.now()+timedelta(hours=8))[:10]
        self.accountName = accountName
        self.scale = scale
        self.keywords = keywords
        self.companyName = companyName
        self.address = address
        self.bank_account = bank_account
        self.concordat_code = concordat_code
        self.remark = remark
        self.platform = platform
        self.status = status
        self.createdTime = createdTime

    def __repr__(self):
        return '<Rebate {}>'.format(self.id)

#Facebook中所有代理以及返点金额
class AccountRebate(db.Model):
    __tablename__ = "accountRebate"
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(200), nullable=True)     #account账户的名字
    accountName = db.Column(db.String(100), nullable=True)   #代理的名字
    cost = db.Column(db.Float, nullable=True)
    rebate = db.Column(db.Float, nullable=True)
    date = db.Column(db.String(100), nullable=True)
    updateTime = db.Column(db.String(100), nullable=True)

    def __init__(self, accountId, name, accountName, cost, rebate, date, updateTime):
        self.accountId = accountId
        self.name = name
        self.accountName = accountName
        self.cost = cost
        self.rebate = rebate,
        self.date = date
        self.updateTime = updateTime

    def __repr__(self):
        return '<AccountRebate {}>'.format(self.id)