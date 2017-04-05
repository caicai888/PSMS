# _*_ coding: utf-8 _*_
import random
import string
import os
import sys


def random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

PREFIX = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..'
    )
)

if PREFIX not in sys.path:
    sys.path.append(PREFIX)

class Config:
    SECRET_KEY = random_string()

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEBUG = True
    MYSQL_USER = "root"
    MYSQL_PASS = "chizicheng521"
    MYSQL_HOST = "localhost"
    MYSQL_PORT = "3306"
    MYSQL_DB = "psms"

config = {
    "default": ProductionConfig,
}

template_cvs_config = {
    'headers': ['Status', 'Offer ID', u'应用名称',u'系统', u'客户名称', u'合作模式', u'投放地区', u'单价', u'投放起始', u'投放截止', u'销售名称', u'最后修改'],
    'filename': 'ReportTable.csv',
    'csv_store_path': os.path.join(os.path.dirname(__file__), 'CSV')
}

