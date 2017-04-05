#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


'''
    数据库中字段对应中文翻译。
'''

mapping = {
        'status': u'状态',
        'platform': u'平台',
        'contract_num': u'合同编号',
        'user_id': u'客户名称',
        'track_link': u'Tracking Link',
        'preview_link': u'Preview Link',
        'app_name': u'APP名称',
        'package_name': u'包名',
        'customer_id': u'销售',
        'app_type': u'APP类型',
        'os': u'操作系统',
        'offer_id': u'offer_id',
        'email_tempalte': u'报告模版',
        'email_time': u'邮件定时报告时间',
        'email_users': u'邮件接收者',

        'facebook,adwords,apple': {
            'contract_scale': u'比例',
            'country_detail': u'投放地区单价',
            'country': u'投放地区',
            'daily_budget': u'最高日结算',
            'material': u'制作素材',
            'daily_type': u'日结算类型',
            'total_type': u'总结算类型',
            'authorized': u'授权账户',
            'KPI': u'KPI要求',
            'total_budget': u'最高总预算',
            'contract_type': u'合作方式',
            'startTime': u'投放起始时间', 
            'endTime': u'投放截止时间',
            'remark': u'备注',
            'named_rule': u'命名规则',
            'settlement': u'账期',
            'distribution': u'预算分配',
            'price': u'默认投放单价',
            }
        }

def sub_dic_handler(g_dic, sub_dic):
    temp_dic = {}
    for k, v in g_dic.items():
        if sub_dic.has_key(k):
            map_sub_releations = {sub_dic.get(k): v} 
            temp_dic.update(map_sub_releations)
    return temp_dic

dic_result = {}
def convert_key(res):
    for k , v in res.items():
        if k in 'facebook,adwords,apple':
            sub = sub_dic_handler(res.get(k),mapping.get('facebook,adwords,apple')) 
            dic_result.update({k: sub})
        else:    
            if mapping.has_key(k):
                map_releations = {mapping.get(k): v}
                dic_result.update(map_releations)
    return dic_result           

def entry(template):
    try:
        g_list = []
        for k, v in convert_key(template).items():
            tmp_list = []
            if k in 'facebook,adwords,apple':
                for subk, subv in v.items():
                    tmp_list.append('\t%s:%s' %(subk, subv))
                g_list.append(k+':'+'\n'+'\n'.join(tmp_list))
            else:
                g_list.append('%s: %s' % (k, v))

        return '\n'.join(g_list)
    except Exception as ex:
        print ex
        return False

if __name__ == '__main__':
    entry('./mail.json') 


