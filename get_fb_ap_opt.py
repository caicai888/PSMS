#!/usr/bin/env python
#coding: utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb

db = MySQLdb.connect("localhost","root","chizicheng521","psms",charset='utf8')
cursor = db.cursor()

sql = "select id,campaignName from campaignRelations"
cursor.execute(sql)
result = cursor.fetchall()

for i in result:
    id = int(i[0])
    name = i[1]
    campaign_name = name.split('_')
    for j in campaign_name:
        if "66" in j:
            update_opt = "update campaignRelations set optName='%s' where id='%d'" % (j,id)
            cursor.execute(update_opt)
            db.commit()

ap_sql = "select id,campaignName from campaignAppName"
cursor.execute(ap_sql)
ap_result = cursor.fetchall()

for j in ap_result:
    id = int(j[0])
    name = j[1]
    campaign_name = name.split('_')
    for i in campaign_name:
        if "66" in i:
            update_ap_opt = "update campaignAppName set optName='%s' where id='%d'" % (i, id)
            cursor.execute(update_ap_opt)
            db.commit()

print "ok"