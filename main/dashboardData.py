# -*- coding: utf-8 -*-
from __future__ import division
from flask import Blueprint, request
from models import Datas, Adwords,Offer, User, DataDetail,UserRole,CampaignRelations
import json
import datetime
from sqlalchemy import func
import MySQLdb

dashboardData = Blueprint('dashboardData', __name__)

@dashboardData.route('/api/dashboard', methods=['POST','GET'])
def dashboard():
    if request.method == "POST":
        data = request.get_json(force=True)
        start_date = data["start_date"]
        end_date = data["end_date"]
        revenue_count = 0
        profit_count = 0
        cost_count = 0
        impressions_count = 0
        clicks_count = 0
        conversions_count = 0
        ctr_count = 0
        cvr_count = 0
        cpc_count = 0
        cpi_count = 0
        rebate_count = 0

        table_list = []

        all_date = []
        all_date.append(start_date)
        date_timelta = datetime.timedelta(days=1)
        date1 = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        date2 = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        while date_timelta < (date2 - date1):
            all_date.append((date1 + date_timelta).strftime("%Y-%m-%d"))
            date_timelta += datetime.timedelta(days=1)
        all_date.append(end_date)

        datas = Datas.query.filter(Datas.date >= start_date,Datas.date <= end_date).all()
        for i in datas:
            revenue_count += float(i.revenue)
            profit_count += float(i.profit)
            cost_count += float(i.cost)
            impressions_count += int(i.impressions)
            clicks_count += int(i.clicks)
            conversions_count += int(i.conversions)
            if i.rebate == "":
                rebate_count += 0
            else:
                rebate_count += float(i.rebate)

        adwords = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).all()
        for i in adwords:
            revenue_count += float(i.revenue)
            profit_count += float(i.profit)
            cost_count += float(i.cost)
            impressions_count += int(i.impressions)
            clicks_count += int(i.clicks)
            conversions_count += int(float(i.conversions))
            if i.rebate == "":
                rebate_count += 0
            else:
                rebate_count += float(i.rebate)

        if conversions_count != 0:
            cpi_count = float('%0.2f' % (cost_count / float(conversions_count)))
        if clicks_count != 0:
            cvr_count = float('%0.2f' % (float(conversions_count) / float(clicks_count) * 100))
            cpc_count = float('%0.2f' % (float(cost_count) / float(clicks_count)))
        if impressions_count != 0:
            ctr_count = float('%0.2f' % (clicks_count / impressions_count * 100))

        result_count = {
            "Renvenue": float('%0.2f'%(revenue_count)),
            "Profit": float('%0.2f'%(profit_count)),
            "Cost": float('%0.2f'%(cost_count)),
            "Impressions": impressions_count,
            "Clicks": clicks_count,
            "Conversions": conversions_count,
            "CTR": ctr_count,
            "CVR": cvr_count,
            "CPC": cpc_count,
            "CPI": cpi_count,
            "Rebate": float('%0.2f'%(rebate_count))
        }

        #折线图
        revenue_list = []
        cost_list = []
        profit_list = []
        impressions_list = []
        clicks_list = []
        conversions_list = []
        ctr_list = []
        cvr_list = []
        cpc_list = []
        cpi_list = []
        rebate_list = []

        for date in all_date:
            revenue_date = 0
            profit_date = 0
            cost_date = 0
            impressions_date = 0
            clicks_date = 0
            conversions_date = 0
            ctr_date = 0
            cvr_date = 0
            cpc_date = 0
            cpi_date = 0
            rebate_date = 0
            datas_list = Datas.query.filter_by(date=date).all()
            for j in datas_list:
                revenue_date += float(j.revenue)
                profit_date += float(j.profit)
                cost_date += float(j.cost)
                impressions_date += int(j.impressions)
                clicks_date += int(j.clicks)
                conversions_date += int(j.conversions)
                rebate_date += float(j.rebate)
            adwords_list = Adwords.query.filter_by(date=date).all()
            for j in adwords_list:
                revenue_date += float(j.revenue)
                profit_date += float(j.profit)
                cost_date += float(j.cost)
                impressions_date += int(j.impressions)
                clicks_date += int(j.clicks)
                conversions_date += int(float(j.conversions))
                rebate_date += float(j.rebate)
            if conversions_date != 0:
                cpi_date = float('%0.2f' % (cost_date / float(conversions_date)))
            if clicks_date != 0:
                cvr_date = float('%0.2f' % (float(conversions_date) / float(clicks_date) * 100))
                cpc_date = float('%0.2f' % (float(cost_date) / float(clicks_date)))
            if impressions_date != 0:
                ctr_date = float('%0.2f' % (clicks_date / impressions_date * 100))

            revenue_list.append(revenue_date)
            cost_list.append(cost_date)
            profit_list.append(float('%0.2f'%(profit_date)))
            impressions_list.append(impressions_date)
            clicks_list.append(clicks_date)
            conversions_list.append(conversions_date)
            ctr_list.append(ctr_date)
            cvr_list.append(cvr_date)
            cpc_list.append(cpc_date)
            cpi_list.append(cpi_date)
            rebate_list.append(float('%0.2f'%(rebate_date)))

        #table数据
        facebook_apple_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date).with_entities(Datas.date,Datas.type,func.sum(Datas.revenue),func.sum(Datas.cost),func.sum(Datas.profit),func.sum(Datas.impressions),func.sum(Datas.clicks),func.sum(Datas.conversions),func.sum(Datas.rebate))
        facebook_apple_data_count = facebook_apple_data.group_by(Datas.date,Datas.type).all()
        for i in facebook_apple_data_count:
            rebate = 0
            if float(i[7]) != 0:
                cpi = float('%0.2f' % (float(i[3]) / float(i[7])))
            else:
                cpi = 0
            if float(i[6]) != 0:
                cvr = float('%0.2f' % (float(i[7]) / float(i[6]) * 100))
                cpc = float('%0.2f' % (float(i[3]) / float(i[6])))
            else:
                cvr = 0
                cpc = 0
            if int(i[5]) != 0:
                ctr = float('%0.2f' % (float(i[6]) / float(i[5]) * 100))
            else:
                ctr = 0
            if i[8] is not None:
                rebate += float(i[8])
            else:
                rebate += 0
            table_list += [
                {
                    "Date": i[0],
                    "Source": i[1],
                    "Revenue": float('%0.2f'%(float(i[2]))),
                    "Cost": float('%0.2f'%(float(i[3]))),
                    "Profit": float('%0.2f'%(float(i[4]))),
                    "Impressions": int(i[5]),
                    "Clicks": int(i[6]),
                    "Conversions": int(i[7]),
                    "Rebate": float('%0.2f'%(rebate)),
                    "CPI": cpi,
                    "CVR": cvr,
                    "CPC": cpc,
                    "CTR": ctr
                }
            ]

        adwords_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.impressions),func.sum(Adwords.clicks),func.sum(Adwords.conversions))
        adwords_data_count = adwords_data.group_by(Adwords.date).all()
        for i in adwords_data_count:
            if float(i[6]) != 0:
                cpi = float('%0.2f' % (float(i[2]) / float(i[6])))
            else:
                cpi = 0
            if float(i[5]) != 0:
                cvr = float('%0.2f' % (float(i[6]) / float(i[5]) * 100))
                cpc = float('%0.2f' % (float(i[2]) / float(i[5])))
            else:
                cvr = 0
                cpc = 0
            if int(i[4]) != 0:
                ctr = float('%0.2f' % (float(i[5]) / float(i[4]) * 100))
            else:
                ctr = 0
            table_list += [
                {
                    "Date": i[0],
                    "Source": "adwords",
                    "Revenue": float('%0.2f'%(float(i[1]))),
                    "Cost": float('%0.2f'%(float(i[2]))),
                    "Profit": float('%0.2f'%(float(i[3]))),
                    "Impressions": int(i[4]),
                    "Clicks": int(i[5]),
                    "Conversions": int(i[6]),
                    "Rebate": 0,
                    "CPI": cpi,
                    "CVR": cvr,
                    "CPC": cpc,
                    "CTR": ctr
                }
            ]

        result_range = {
            "Date": all_date,
            "Revenue": revenue_list,
            "Profit": profit_list,
            "Cost": cost_list,
            "Impressions": impressions_list,
            "Clicks": clicks_list,
            "Conversions": conversions_list,
            "CPI": cpi_list,
            "CTR": ctr_list,
            "CVR": cvr_list,
            "CPC": cpc_list,
            "Rebate": rebate_list
        }
        result = {
            "count": result_count,
            "range": result_range,
            "table": table_list,
            "dimission":["Date","Source","Revenue","Cost","Profit","Impressions","Conversions","Clicks","Rebate","CVR","CPC","CTR","CPI"],
            "code": 200,
            "message": "success"
        }
        return json.dumps(result)

#dashboard中表格数据
@dashboardData.route('/api/dashboard/table', methods=["POST","GET"])
def dbTable():
    if request.method == "POST":
        data = request.get_json(force=True)
        start_date = data['start_date']
        end_date = data['end_date']
        flag = data['flag']
        facebook_apple_data = []
        adwords_data = []
        all_data = []
        if flag == "PM-Data":
            fb_ap_data = Datas.query.filter(Datas.date >= start_date,Datas.date <= end_date).with_entities(Datas.offer_id,Datas.date,func.sum(Datas.conversions),func.sum(Datas.cost),func.sum(Datas.revenue),func.sum(Datas.profit),func.sum(Datas.rebate))
            fb_ap_result = fb_ap_data.group_by(Datas.date,Datas.offer_id).all()
            for i in fb_ap_result:
                offer_sql = Offer.query.filter_by(id=i[0]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    if i[6] == None:
                        rebate = 0
                    else:
                        rebate = i[6]
                    facebook_apple_data += [
                        {
                            "appName": appName,
                            "Date": i[1],
                            "Conversions": int(i[2]),
                            "Cost": i[3],
                            "Revenue": i[4],
                            "Profit": i[5],
                            "Rebate": rebate,
                            "CountProfit": i[5]+rebate,
                        }
                    ]
            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.offer_id,Adwords.date,func.sum(Adwords.conversions),func.sum(Adwords.cost),func.sum(Adwords.revenue),func.sum(Adwords.profit),func.sum(Adwords.rebate))
            adword_result = adword_data.group_by(Adwords.date,Adwords.offer_id).all()
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[0]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    if i[6] == None:
                        rebate = 0
                    else:
                        rebate = i[6]
                    adwords_data += [
                        {
                            "appName": appName,
                            "Date": i[1],
                            "Conversions": int(i[2]),
                            "Cost": i[3],
                            "Revenue": i[4],
                            "Profit": i[5],
                            "Rebate": rebate,
                            "CountProfit": i[5] + rebate,
                        }
                    ]

            all_data = facebook_apple_data + adwords_data
            tempList = []
            all_data_list_unique = []
            for ele in all_data:
                key = ele['Date'] + ele['appName']
                if key in tempList:
                    for x in all_data_list_unique:
                        if x['Date'] == ele['Date'] and x['appName'] == ele['appName']:
                            x['Conversions'] += int(ele['Conversions'])
                            x['Revenue'] += float('%0.2f'%(float(ele['Revenue'])))
                            x['Cost'] += float('%0.2f'%(float(ele['Cost'])))
                            x['Profit'] += float('%0.2f'%(float(ele['Profit'])))
                            x['Rebate'] += float('%0.2f'%(float(ele['Rebate'])))
                            x['CountProfit'] += float('%0.2f'%(float(ele['CountProfit'])))

                else:
                    ele['Conversions'] = int(ele['Conversions'])
                    ele['Revenue'] = float(ele['Revenue'])
                    ele['Cost'] = float('%0.2f'%(float(ele['Cost'])))
                    ele['Profit'] = float('%0.2f'%(float(ele['Profit'])))
                    ele['Rebate'] = float('%0.2f'%(float(ele['Rebate'])))
                    ele['CountProfit'] = float('%0.2f'%(float(ele['CountProfit'])))

                    tempList.append(key)
                    all_data_list_unique.append(ele)

            all_data_list = []
            for l in all_data_list_unique:
                cpi = float('%0.2f' % (cData(float(l['Cost']), float(l['Conversions']))))
                l['CPI'] = cpi
                l['Revenue'] = float('%0.2f'%(l["Revenue"]))
                l['Cost'] = float('%0.2f'%(l["Cost"]))
                l["Profit"] = float('%0.2f'%(l['Profit']))
                l["Rebate"] = float('%0.2f'%(l['Rebate']))
                l["CountProfit"] = float('%0.2f'%(l['CountProfit']))
                l["ROI"] = float('%0.2f'%(cData(float(l["Profit"]),float(l["Cost"]))))
                all_data_list.append(l)
            dimission = ["Date","appName","Conversions","CPI","Cost","Revenue","Profit","Rebate","CountProfit","ROI"]

        elif flag == "PM-BD":
            role = UserRole.query.filter(UserRole.role_id == 4).all()
            for r in role:
                users = User.query.filter_by(id=r.user_id).first()
                BD = users.name
                offerIds = Offer.query.filter(Offer.user_id == r.user_id).all()
                for d in offerIds:
                    if d.status == "deleted":
                        pass
                    else:
                        offer_id = d.id
                        appName = d.app_name
                        fb_ap_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date,Datas.offer_id == offer_id).with_entities(Datas.offer_id,Datas.date,func.sum(Datas.profit),func.sum(Datas.rebate))
                        fb_ap_result = fb_ap_data.group_by(Datas.date, Datas.offer_id).all()
                        if fb_ap_result:
                            for i in fb_ap_result:
                                if i[3] == None:
                                    rebate = 0
                                else:
                                    rebate = i[3]
                                facebook_apple_data += [
                                    {
                                        "Date": i[1],
                                        "BD": BD,
                                        "appName": appName,
                                        "CountProfit": i[2]+rebate
                                    }
                                ]
                        adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date, Adwords.offer_id == offer_id).with_entities(Adwords.offer_id,Adwords.date,func.sum(Adwords.profit),func.sum(Adwords.rebate))
                        adword_result = adword_data.group_by(Adwords.date, Adwords.offer_id).all()
                        if adword_result:
                            for i in adword_result:
                                if i[3] == None:
                                    rebate = 0
                                else:
                                    rebate = i[3]
                                adwords_data += [
                                    {
                                        "Date": i[1],
                                        "BD": BD,
                                        "appName": appName,
                                        "CountProfit": i[2]+rebate
                                    }
                                ]
            all_data = facebook_apple_data + adwords_data
            tempList = []
            all_data_list_unique = []
            for ele in all_data:
                key = ele['Date'] + ele['BD'] + ele['appName']
                if key in tempList:
                    for x in all_data_list_unique:
                        if x['Date'] == ele['Date'] and x['BD'] == ele['BD'] and x['appName'] == ele['appName']:
                            x['CountProfit'] += float('%0.2f' % (float(ele['CountProfit'])))

                else:
                    ele['CountProfit'] = float('%0.2f' % (float(ele['CountProfit'])))

                    tempList.append(key)
                    all_data_list_unique.append(ele)

            all_data_list = []
            for l in all_data_list_unique:
                l["CountProfit"] = float('%0.2f' % (l['CountProfit']))
                all_data_list.append(l)
            dimission = ["Date", "BD", "appName", "CountProfit"]

        elif flag == "PM-AG":
            all_data_list = []
            data_detail = DataDetail.query.filter(DataDetail.date >= start_date,DataDetail.date <= end_date, DataDetail.type=='facebook').with_entities(DataDetail.date,DataDetail.account_id,func.sum(DataDetail.cost))
            detail_result = data_detail.group_by(DataDetail.date,DataDetail.account_id).all()
            for i in detail_result:
                accountName = CampaignRelations.query.filter_by(account_id=i[1]).first()
                account_name = accountName.account_name
                all_data_list += [
                    {
                        "Date": i[0],
                        "AccountName": account_name,
                        "AccountId": i[1],
                        "Cost": float('%0.2f'%(float(i[2])))
                    }
                ]
            dimission = ["Date", "AccountId", "AccountName", "Cost"]

        elif flag == "Offer":
            fb_ap_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date).with_entities(Datas.date,Datas.offer_id,func.sum(Datas.revenue),func.sum(Datas.cost),func.sum(Datas.profit),func.sum(Datas.conversions),func.sum(Datas.impressions),func.sum(Datas.clicks))
            fb_ap_result = fb_ap_data.group_by(Datas.date,Datas.offer_id).all()
            for i in fb_ap_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    facebook_apple_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": i[2],
                            "Cost": i[3],
                            "Profit": i[4],
                            "Conversions": i[5],
                            "Impressions": i[6],
                            "Clicks": i[7],
                            "AppName": appName
                        }
                    ]
            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date,Adwords.offer_id,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.date,Adwords.offer_id).all()
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    adwords_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": i[2],
                            "Cost": i[3],
                            "Profit": i[4],
                            "Conversions": i[5],
                            "Impressions": i[6],
                            "Clicks": i[7],
                            "AppName": appName
                        }
                    ]
            all_data = facebook_apple_data + adwords_data
            tempList = []
            all_data_list_unique = []
            for ele in all_data:
                key = ele['Date'] + str(ele['Offer'])
                if key in tempList:
                    for x in all_data_list_unique:
                        if x['Date'] == ele['Date'] and x['Offer'] == ele['Offer']:
                            x['Conversions'] += int(ele['Conversions'])
                            x['Revenue'] += float('%0.2f' % (float(ele['Revenue'])))
                            x['Cost'] += float('%0.2f' % (float(ele['Cost'])))
                            x['Profit'] += float('%0.2f' % (float(ele['Profit'])))
                            x['Clicks'] += int(ele['Clicks'])
                            x['Impressions'] += int(ele['Impressions'])

                else:
                    ele['Conversions'] = int(ele['Conversions'])
                    ele['Revenue'] = float(ele['Revenue'])
                    ele['Cost'] = float('%0.2f' % (float(ele['Cost'])))
                    ele['Profit'] = float('%0.2f' % (float(ele['Profit'])))
                    ele['Impressions'] = int(ele['Impressions'])
                    ele['Clicks'] = int(ele['Clicks'])

                    tempList.append(key)
                    all_data_list_unique.append(ele)

            all_data_list = []
            for l in all_data_list_unique:
                cpi = float('%0.2f' % (cData(float(l['Cost']), float(l['Conversions']))))
                cpc = float('%0.2f' % (cData(float(l['Cost']), float(l['Clicks']))))
                cvr = float('%0.2f' % (cData(float(l['Conversions']), float(l['Clicks']))*100))
                ctr = float('%0.2f' % (cData(float(l['Clicks']), float(l['Impressions']))*100))
                l['CPI'] = cpi
                l['CPC'] = cpc
                l['CVR'] = cvr
                l['CTR'] = ctr
                l['Revenue'] = float('%0.2f' % (l["Revenue"]))
                l['Cost'] = float('%0.2f' % (l["Cost"]))
                l["Profit"] = float('%0.2f' % (l['Profit']))
                all_data_list.append(l)
            dimission = ["Date", "Offer","AppName", "Revenue","Cost","Profit","Conversions", "CPI","CPC","CVR","CTR","Impressions","Clicks"]

        elif flag == "Offer-1":
            facebook_data = []
            apple_data = []
            fb_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date, Datas.type == "facebook").with_entities(Datas.date,Datas.offer_id,func.sum(Datas.revenue),func.sum(Datas.cost),func.sum(Datas.profit),func.sum(Datas.conversions),func.sum(Datas.impressions),func.sum(Datas.clicks))
            fb_result = fb_data.group_by(Datas.date,Datas.offer_id).all()
            for i in fb_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[3]), float(i[5]))))
                    cpc = float('%0.2f' % (cData(float(i[3]), float(i[7]))))
                    cvr = float('%0.2f' % (cData(float(i[5]), float(i[7])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[7]), float(i[6])) * 100))
                    facebook_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f'%(float(i[2]))),
                            "Cost": float('%0.2f'%(float(i[3]))),
                            "Profit": float('%0.2f'%(float(i[4]))),
                            "Conversions": int(i[5]),
                            "Impressions": int(i[6]),
                            "Clicks": int(i[7]),
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "Source": "facebook",
                            "AppName": appName
                        }
                    ]
            ap_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date, Datas.type == "apple").with_entities(Datas.date,Datas.offer_id,func.sum(Datas.revenue),func.sum(Datas.cost),func.sum(Datas.profit),func.sum(Datas.conversions),func.sum(Datas.impressions),func.sum(Datas.clicks))
            ap_result = ap_data.group_by(Datas.date, Datas.offer_id).all()
            for i in ap_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[3]), float(i[5]))))
                    cpc = float('%0.2f' % (cData(float(i[3]), float(i[7]))))
                    cvr = float('%0.2f' % (cData(float(i[5]), float(i[7])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[7]), float(i[6])) * 100))
                    apple_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f'%(float(i[2]))),
                            "Cost": float('%0.2f'%(float(i[3]))),
                            "Profit": float('%0.2f'%(float(i[4]))),
                            "Conversions": int(i[5]),
                            "Impressions": int(i[6]),
                            "Clicks": int(i[7]),
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "Source": "apple",
                            "AppName": appName
                        }
                    ]
            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date,Adwords.offer_id,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.date,Adwords.offer_id)
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[3]), float(i[5]))))
                    cpc = float('%0.2f' % (cData(float(i[3]), float(i[7]))))
                    cvr = float('%0.2f' % (cData(float(i[5]), float(i[7])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[7]), float(i[6])) * 100))
                    adwords_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f'%(float(i[2]))),
                            "Cost": float('%0.2f'%(float(i[3]))),
                            "Profit": float('%0.2f'%(float(i[4]))),
                            "Conversions": int(i[5]),
                            "Impressions": int(i[6]),
                            "Clicks": int(i[7]),
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "Source": "adwords",
                            "AppName": appName
                        }
                    ]

            all_data_list = facebook_data + apple_data + adwords_data
            dimission = ["Date", "Offer","AppName","Source", "Revenue","Cost","Profit","Conversions", "CPI","CPC","CVR","CTR","Impressions","Clicks"]

        elif flag == "Offer-2":
            facebook_data = []
            apple_data = []
            fb_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date, Datas.type == "facebook").with_entities(Datas.date,Datas.offer_id,Datas.country,func.sum(Datas.revenue),func.sum(Datas.cost),func.sum(Datas.profit),func.sum(Datas.conversions),func.sum(Datas.impressions),func.sum(Datas.clicks))
            fb_result = fb_data.group_by(Datas.date, Datas.offer_id,Datas.country).all()
            for i in fb_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[4]), float(i[6]))))
                    cpc = float('%0.2f' % (cData(float(i[4]), float(i[8]))))
                    cvr = float('%0.2f' % (cData(float(i[6]), float(i[8])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[8]), float(i[7])) * 100))
                    facebook_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f' % (float(i[3]))),
                            "Cost": float('%0.2f' % (float(i[4]))),
                            "Profit": float('%0.2f' % (float(i[5]))),
                            "Conversions": int(i[6]),
                            "Impressions": int(i[7]),
                            "Clicks": int(i[8]),
                            "Source": "facebook",
                            "GEO": i[2],
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "AppName": appName
                        }
                    ]
            ap_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date, Datas.type == "apple").with_entities(Datas.date,
 Datas.offer_id,Datas.country,func.sum(Datas.revenue),func.sum(Datas.cost),func.sum(Datas.profit),func.sum(Datas.conversions),func.sum(Datas.impressions),func.sum(Datas.clicks))
            ap_result = ap_data.group_by(Datas.date, Datas.offer_id,Datas.country).all()
            for i in ap_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[4]), float(i[6]))))
                    cpc = float('%0.2f' % (cData(float(i[4]), float(i[8]))))
                    cvr = float('%0.2f' % (cData(float(i[6]), float(i[8])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[8]), float(i[7])) * 100))
                    apple_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f' % (float(i[3]))),
                            "Cost": float('%0.2f' % (float(i[4]))),
                            "Profit": float('%0.2f' % (float(i[5]))),
                            "Conversions": int(i[6]),
                            "Impressions": int(i[7]),
                            "Clicks": int(i[8]),
                            "Source": "apple",
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "GEO": i[2],
                            "AppName": appName
                        }
                    ]
            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date, Adwords.offer_id,Adwords.country,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.date, Adwords.offer_id,Adwords.country)
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[4]), float(i[6]))))
                    cpc = float('%0.2f' % (cData(float(i[4]), float(i[8]))))
                    cvr = float('%0.2f' % (cData(float(i[6]), float(i[8])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[8]), float(i[7])) * 100))
                    adwords_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f' % (float(i[3]))),
                            "Cost": float('%0.2f' % (float(i[4]))),
                            "Profit": float('%0.2f' % (float(i[5]))),
                            "Conversions": int(i[6]),
                            "Impressions": int(i[7]),
                            "Clicks": int(i[8]),
                            "Source": "adwords",
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "GEO": i[2],
                            "AppName": appName
                        }
                    ]

            all_data_list = facebook_data + apple_data + adwords_data
            dimission = ["Date", "Offer","AppName", "Source","GEO", "Revenue", "Cost", "Profit", "Conversions", "CPI", "CPC", "CVR", "CTR", "Impressions", "Clicks"]

        elif flag == "MB-1":
            facebook_data = []
            apple_data = []
            fb_data = DataDetail.query.filter(DataDetail.date >= start_date, DataDetail.date <= end_date,DataDetail.type=='facebook').with_entities(DataDetail.date,DataDetail.offer_id,DataDetail.optName,func.sum(DataDetail.revenue),func.sum(DataDetail.cost),func.sum(DataDetail.profit),func.sum(DataDetail.conversions),func.sum(DataDetail.impressions),func.sum(DataDetail.clicks))
            fb_result = fb_data.group_by(DataDetail.optName,DataDetail.offer_id,DataDetail.date).all()
            for i in fb_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[4]), float(i[6]))))
                    cpc = float('%0.2f' % (cData(float(i[4]), float(i[8]))))
                    cvr = float('%0.2f' % (cData(float(i[6]), float(i[8])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[8]), float(i[7])) * 100))
                    facebook_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f' % (float(i[3]))),
                            "Cost": float('%0.2f' % (float(i[4]))),
                            "Profit": float('%0.2f' % (float(i[5]))),
                            "Conversions": int(i[6]),
                            "Impressions": int(i[7]),
                            "Clicks": int(i[8]),
                            "Source": "facebook",
                            "MB": i[2],
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "AppName": appName
                        }
                    ]
            ap_data = DataDetail.query.filter(DataDetail.date >= start_date, DataDetail.date <= end_date,DataDetail.type == 'apple').with_entities(DataDetail.date, DataDetail.offer_id,DataDetail.optName, func.sum(DataDetail.revenue),func.sum(DataDetail.cost), func.sum(DataDetail.profit),func.sum(DataDetail.conversions),func.sum(DataDetail.impressions),func.sum(DataDetail.clicks))
            ap_result = ap_data.group_by(DataDetail.optName, DataDetail.offer_id, DataDetail.date).all()
            for i in ap_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[4]), float(i[6]))))
                    cpc = float('%0.2f' % (cData(float(i[4]), float(i[8]))))
                    cvr = float('%0.2f' % (cData(float(i[6]), float(i[8])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[8]), float(i[7])) * 100))
                    apple_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f' % (float(i[3]))),
                            "Cost": float('%0.2f' % (float(i[4]))),
                            "Profit": float('%0.2f' % (float(i[5]))),
                            "Conversions": int(i[6]),
                            "Impressions": int(i[7]),
                            "Clicks": int(i[8]),
                            "Source": "apple",
                            "MB": i[2],
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "AppName": appName
                        }
                    ]

            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date, Adwords.offer_id,Adwords.optName,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.date, Adwords.offer_id, Adwords.optName)
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[4]), float(i[6]))))
                    cpc = float('%0.2f' % (cData(float(i[4]), float(i[8]))))
                    cvr = float('%0.2f' % (cData(float(i[6]), float(i[8])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[8]), float(i[7])) * 100))
                    adwords_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f' % (float(i[3]))),
                            "Cost": float('%0.2f' % (float(i[4]))),
                            "Profit": float('%0.2f' % (float(i[5]))),
                            "Conversions": int(i[6]),
                            "Impressions": int(i[7]),
                            "Clicks": int(i[8]),
                            "Source": "adwords",
                            "MB": i[2],
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "AppName": appName
                        }
                    ]
            all_data_list = facebook_data + apple_data + adwords_data
            dimission = ["Date", "Offer","AppName", "MB","Source", "Revenue", "Cost", "Profit", "Conversions", "CPI", "CPC", "CVR", "CTR", "Impressions","Clicks"]

        elif flag == "MB-2":
            facebook_data = []
            apple_data = []
            fb_data = DataDetail.query.filter(DataDetail.date >= start_date, DataDetail.date <= end_date,DataDetail.type=='facebook').with_entities(DataDetail.date,DataDetail.offer_id,DataDetail.optName,DataDetail.country,func.sum(DataDetail.revenue),func.sum(DataDetail.cost),func.sum(DataDetail.profit),func.sum(DataDetail.conversions),func.sum(DataDetail.impressions),func.sum(DataDetail.clicks))
            fb_result = fb_data.group_by(DataDetail.optName, DataDetail.offer_id, DataDetail.date, DataDetail.country).all()
            for i in fb_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[5]), float(i[7]))))
                    cpc = float('%0.2f' % (cData(float(i[5]), float(i[9]))))
                    cvr = float('%0.2f' % (cData(float(i[7]), float(i[9])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[9]), float(i[8])) * 100))
                    facebook_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f' % (float(i[4]))),
                            "Cost": float('%0.2f' % (float(i[5]))),
                            "Profit": float('%0.2f' % (float(i[6]))),
                            "Conversions": int(i[7]),
                            "Impressions": int(i[8]),
                            "Clicks": int(i[9]),
                            "Source": "facebook",
                            "MB": i[2],
                            "GEO": i[3],
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "AppName": appName
                        }
                    ]
            ap_data = DataDetail.query.filter(DataDetail.date >= start_date, DataDetail.date <= end_date,DataDetail.type == 'apple').with_entities(DataDetail.date, DataDetail.offer_id, DataDetail.optName,DataDetail.country, func.sum(DataDetail.revenue),func.sum(DataDetail.cost), func.sum(DataDetail.profit),func.sum(DataDetail.conversions),func.sum(DataDetail.impressions),func.sum(DataDetail.clicks))
            ap_result = ap_data.group_by(DataDetail.optName, DataDetail.offer_id, DataDetail.date, DataDetail.country).all()
            for i in ap_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[5]), float(i[7]))))
                    cpc = float('%0.2f' % (cData(float(i[5]), float(i[9]))))
                    cvr = float('%0.2f' % (cData(float(i[7]), float(i[9])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[9]), float(i[8])) * 100))
                    apple_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f' % (float(i[4]))),
                            "Cost": float('%0.2f' % (float(i[5]))),
                            "Profit": float('%0.2f' % (float(i[6]))),
                            "Conversions": int(i[7]),
                            "Impressions": int(i[8]),
                            "Clicks": int(i[9]),
                            "Source": "apple",
                            "MB": i[2],
                            "GEO": i[3],
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "AppName": appName
                        }
                    ]
            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date, Adwords.offer_id,Adwords.optName,Adwords.country,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.date, Adwords.offer_id, Adwords.optName,Adwords.country)
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    appName = offer_sql.app_name
                    cpi = float('%0.2f' % (cData(float(i[5]), float(i[7]))))
                    cpc = float('%0.2f' % (cData(float(i[5]), float(i[9]))))
                    cvr = float('%0.2f' % (cData(float(i[7]), float(i[9])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[9]), float(i[8])) * 100))
                    adwords_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": float('%0.2f' % (float(i[4]))),
                            "Cost": float('%0.2f' % (float(i[5]))),
                            "Profit": float('%0.2f' % (float(i[6]))),
                            "Conversions": int(i[7]),
                            "Impressions": int(i[8]),
                            "Clicks": int(i[9]),
                            "Source": "adwords",
                            "MB": i[2],
                            "GEO":i[3],
                            "CPI": cpi,
                            "CPC": cpc,
                            "CVR": cvr,
                            "CTR": ctr,
                            "AppName": appName
                        }
                    ]
            all_data_list = facebook_data + apple_data + adwords_data
            dimission = ["Date", "Offer","AppName", "MB","Source","GEO", "Revenue", "Cost", "Profit", "Conversions", "CPI", "CPC", "CVR", "CTR", "Impressions","Clicks"]


        elif flag == "MB":
            fb_ap_data = DataDetail.query.filter(DataDetail.date >= start_date, DataDetail.date <= end_date).with_entities(DataDetail.date,DataDetail.optName,func.sum(DataDetail.revenue),func.sum(DataDetail.cost),func.sum(DataDetail.profit),func.sum(DataDetail.conversions),func.sum(DataDetail.impressions),func.sum(DataDetail.clicks))
            fb_ap_result = fb_ap_data.group_by(DataDetail.optName,DataDetail.date).all()
            for i in fb_ap_result:
                facebook_apple_data += [
                    {
                        "Date": i[0],
                        "Revenue": float('%0.2f' % (float(i[2]))),
                        "Cost": float('%0.2f' % (float(i[3]))),
                        "Profit": float('%0.2f' % (float(i[4]))),
                        "Conversions": int(i[5]),
                        "Impressions": int(i[6]),
                        "Clicks": int(i[7]),
                        "MB": i[1]
                    }
                ]
            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date,Adwords.optName,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.optName,Adwords.date).all()
            for i in adword_result:
                adwords_data += [
                    {
                        "Date": i[0],
                        "Revenue": float('%0.2f' % (float(i[2]))),
                        "Cost": float('%0.2f' % (float(i[3]))),
                        "Profit": float('%0.2f' % (float(i[4]))),
                        "Conversions": int(i[5]),
                        "Impressions": int(i[6]),
                        "Clicks": int(i[7]),
                        "MB": i[1]
                    }
                ]

            all_data_list = facebook_apple_data + adwords_data
            tempList = []
            all_data_list_unique = []
            for ele in all_data_list:
                if ele['MB'] is None:
                    pass
                else:
                    key = ele['Date'] + ele['MB']
                    if key in tempList:
                        for x in all_data_list_unique:
                            if x['Date'] == ele['Date'] and x['MB'] == ele['MB']:
                                x['Revenue'] += float('%0.2f' % (float(ele['Revenue'])))
                                x['Cost'] += float('%0.2f' % (float(ele['Cost'])))
                                x['Profit'] += float('%0.2f' % (float(ele['Profit'])))
                                x['Conversions'] += int(ele['Conversions'])
                                x['Impressions'] += int(ele['Impressions'])
                                x['Clicks'] += int(ele['Clicks'])

                    else:
                        ele['Revenue'] = float('%0.2f' % (float(ele['Revenue'])))
                        ele['Cost'] = float('%0.2f' % (float(ele['Cost'])))
                        ele['Profit'] = float('%0.2f' % (float(ele['Profit'])))
                        ele['Conversions'] = float('%0.2f' % (float(ele['Conversions'])))
                        ele['Impressions'] = float('%0.2f' % (float(ele['Impressions'])))
                        ele['Clicks'] = float('%0.2f' % (float(ele['Clicks'])))

                        tempList.append(key)
                        all_data_list_unique.append(ele)

            all_data_list = []
            for l in all_data_list_unique:
                l['CPI'] = float('%0.2f' % (cData(float(l['Cost']), float(l['Conversions']))))
                l['CPC'] = float('%0.2f' % (cData(float(l['Cost']), float(l['Clicks']))))
                l['CVR'] = float('%0.2f' % (cData(float(l['Conversions']), float(l['Clicks'])) * 100))
                l['CTR'] = float('%0.2f' % (cData(float(l['Clicks']), float(l['Impressions'])) * 100))
                l['Revenue'] = float('%0.2f' % (l["Revenue"]))
                l['Cost'] = float('%0.2f' % (l["Cost"]))
                l['Profit'] = float('%0.2f' % (l["Profit"]))
                all_data_list.append(l)
            dimission = ["Date", "MB", "Revenue", "Cost", "Profit", "Conversions", "CPI", "CPC", "CVR", "CTR", "Impressions","Clicks"]

        response = {
            "code": 200,
            "message": "success",
            "results":all_data_list,
            "dimission": dimission
        }
        return json.dumps(response)

def cData(denominator,molecular):
    if float(molecular)==0:
        result = 0
    else:
        result = float(denominator/molecular)
    return result

#soloERP系统的接口
@dashboardData.route('/api/soloERP/<start_date>', methods=["POST","GET"])
def erpData(start_date):
    psms_db = MySQLdb.connect("localhost", "root", "chizicheng521", "psms", charset='utf8')
    psms_cursor = psms_db.cursor()
    time_now = datetime.datetime.now() + datetime.timedelta(hours=8)
    end_date = datetime.datetime.strftime(time_now, '%Y-%m-%d')

    all_date = []
    date2 = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    all_date.append(start_date)
    date_timelta = datetime.timedelta(days=1)
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')

    while date_timelta < (date2 - start_date):
        all_date.append((start_date + date_timelta).strftime("%Y-%m-%d"))
        date_timelta += datetime.timedelta(days=1)
    all_date.append(end_date)

    adwords_result = []
    facebook_result = []
    apple_result = []
    count_result = []
    for i in all_date:
        revenue = 0
        profit = 0
        cost = 0
        ad_revenue = 0
        ad_cost = 0
        ad_profit = 0

        fb_revenue = 0
        fb_cost = 0
        fb_profit = 0

        ap_revenue = 0
        ap_cost = 0
        ap_profit = 0
        # adwords 部分
        adwords_data = "select revenue,cost,profit from adwords where date='%s'" % i
        psms_cursor.execute(adwords_data)
        result = psms_cursor.fetchall()
        for j in result:
            ad_revenue += j[0]
            ad_cost += j[1]
            ad_profit += j[2]
        revenue += ad_revenue
        cost += ad_cost
        profit += ad_profit
        adwords_result += [
            {
                "date": i,
                "cost": ad_cost,
                "revenue": ad_revenue,
                "profit": ad_profit
            }
        ]

        fb_data = "select revenue,cost,profit from datas where date='%s' and type='facebook'" % i
        psms_cursor.execute(fb_data)
        fb_result = psms_cursor.fetchall()
        for j in fb_result:
            fb_revenue += j[0]
            fb_cost += j[1]
            fb_profit += j[2]
        revenue += fb_revenue
        cost += fb_cost
        profit += fb_profit
        facebook_result += [
            {
                "date": i,
                "revenue": fb_revenue,
                "cost": fb_cost,
                "profit": fb_profit
            }
        ]

        ap_data = "select revenue,cost,profit from datas where date='%s' and type='apple'" % i
        psms_cursor.execute(ap_data)
        ap_result = psms_cursor.fetchall()
        for j in ap_result:
            ap_revenue += j[0]
            ap_cost += j[1]
            ap_profit += j[2]
        revenue += ap_revenue
        cost += ap_cost
        profit += ap_profit
        apple_result += [
            {
                "date": i,
                "revenue": ap_revenue,
                "cost": ap_cost,
                "profit": ap_profit
            }
        ]

        count_result += [
            {
                "date": i,
                "revenue": revenue,
                "cost": cost,
                "profit": profit
            }
        ]
    response = {
        "apple": apple_result,
        "facebook": facebook_result,
        "adwords": adwords_result,
        "count": count_result
    }
    return json.dumps(response)