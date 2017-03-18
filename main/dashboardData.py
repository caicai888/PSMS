# -*- coding: utf-8 -*-
from __future__ import division
from flask import Blueprint, request
from models import Datas, Adwords,Offer, User, DataDetail,UserRole
import json
import datetime
from sqlalchemy import func

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

        adwords = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).all()
        for i in adwords:
            revenue_count += float(i.revenue)
            profit_count += float(i.profit)
            cost_count += float(i.cost)
            impressions_count += int(i.impressions)
            clicks_count += int(i.clicks)
            conversions_count += int(float(i.conversions))

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
            "CPI": cpi_count
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
            datas_list = Datas.query.filter_by(date=date).all()
            for j in datas_list:
                revenue_date += float(j.revenue)
                profit_date += float(j.profit)
                cost_date += float(j.cost)
                impressions_date += int(j.impressions)
                clicks_date += int(j.clicks)
                conversions_date += int(j.conversions)
            adwords_list = Adwords.query.filter_by(date=date).all()
            for j in adwords_list:
                revenue_date += float(j.revenue)
                profit_date += float(j.profit)
                cost_date += float(j.cost)
                impressions_date += int(j.impressions)
                clicks_date += int(j.clicks)
                conversions_date += int(float(j.conversions))
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
                    "Revenue": float(i[2]),
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
                    "Revenue": float(i[1]),
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
            "CPC": cpc_list
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
                dimission = ["Date","appName","Conversions","CPI","Cost","Revenue","Porfit","Rebate","CountProfit","ROI"]
            all_data_list = [
                {
                    "Conversions": 305,
                    "Profit": 523.98,
                    "Cost": 86.02,
                    "CountProfit": 535.44,
                    "appName": "德州扑克",
                    "Date": "2017-02-10",
                    "CPI": 0.28,
                    "Revenue": 610,
                    "ROI": 6.09,
                    "Rebate": 11.46
                },
                {
                    "Conversions": 1565,
                    "Profit": 3289,
                    "Cost": 1406,
                    "CountProfit": 3456.58,
                    "appName": "大乱斗",
                    "Date": "2017-02-10",
                    "CPI": 0.9,
                    "Revenue": 4695,
                    "ROI": 2.34,
                    "Rebate": 167.58
                },
                {
                    "Conversions": 230,
                    "Profit": 381.08,
                    "Cost": 78.92,
                    "CountProfit": 391.72,
                    "appName": "德州扑克",
                    "Date": "2017-02-11",
                    "CPI": 0.34,
                    "Revenue": 460,
                    "ROI": 4.83,
                    "Rebate": 10.64
                },
            ]

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
                key = ele['Date'] + ele['BD']
                if key in tempList:
                    for x in all_data_list_unique:
                        if x['Date'] == ele['Date'] and x['BD'] == ele['BD']:
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
            all_data_list = [
                {
                    "Date": "2017-02-10",
                    "BD": "liyin",
                    "CountProfit": 3456.58,
                    "appName": "大乱斗"
                },
                {
                    "Date": "2017-02-11",
                    "BD": "liyin",
                    "CountProfit": 3501.26,
                    "appName": "大乱斗"
                },
                {
                    "Date": "2017-02-12",
                    "BD": "liyin",
                    "CountProfit": 1401.67,
                    "appName": "大乱斗"
                },
                {
                    "Date": "2017-02-13",
                    "BD": "liyin",
                    "CountProfit": 1881.98,
                    "appName": "大乱斗"
                },
                {
                    "Date": "2017-02-10",
                    "BD": "yinli",
                    "CountProfit": 535.44,
                    "appName": "德州扑克"
                }
            ]

        elif flag == "Offer-1":
            fb_ap_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date).with_entities(Datas.date,Datas.offer_id,func.sum(Datas.revenue),func.sum(Datas.cost),func.sum(Datas.profit),func.sum(Datas.conversions),func.sum(Datas.impressions),func.sum(Datas.clicks))
            fb_ap_result = fb_ap_data.group_by(Datas.date,Datas.offer_id).all()
            for i in fb_ap_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    facebook_apple_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": i[2],
                            "Cost": i[3],
                            "Profit": i[4],
                            "Conversions": i[5],
                            "Impressions": i[6],
                            "Clicks": i[7]
                        }
                    ]
            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date,Adwords.offer_id,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.date,Adwords.offer_id).all()
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
                    adwords_data += [
                        {
                            "Date": i[0],
                            "Offer": i[1],
                            "Revenue": i[2],
                            "Cost": i[3],
                            "Profit": i[4],
                            "Conversions": i[5],
                            "Impressions": i[6],
                            "Clicks": i[7]
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
                dimission = ["Date", "Offer", "Revenue","Cost","Porfit","Conversions", "CPI","CPC","CVR","CTR","Impressions","Clicks"]
            all_data_list = [
                {
                    "CPI": 0.28,
                    "CTR": 2.05,
                    "Profit": 523.98,
                    "CPC": 0.07,
                    "CVR": 24,
                    "Clicks": 1271,
                    "Conversions": 305,
                    "Offer": 2,
                    "Revenue": 610,
                    "Cost": 86.02,
                    "Date": "2017-02-10",
                    "Impressions": 61940
                },
                {
                    "CPI": 0.9,
                    "CTR": 3.03,
                    "Profit": 3289,
                    "CPC": 0.14,
                    "CVR": 15.87,
                    "Clicks": 9863,
                    "Conversions": 1565,
                    "Offer": 3,
                    "Revenue": 4695,
                    "Cost": 1406,
                    "Date": "2017-02-10",
                    "Impressions": 325345
                },
                {
                    "CPI": 0.34,
                    "CTR": 2.05,
                    "Profit": 381.08,
                    "CPC": 0.07,
                    "CVR": 21.2,
                    "Clicks": 1085,
                    "Conversions": 230,
                    "Offer": 2,
                    "Revenue": 460,
                    "Cost": 78.92,
                    "Date": "2017-02-11",
                    "Impressions": 52841
                }
            ]

        elif flag == "Offer-2":
            facebook_data = []
            apple_data = []
            fb_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date, Datas.type == "facebook").with_entities(Datas.date,Datas.offer_id,func.sum(Datas.revenue),func.sum(Datas.cost),func.sum(Datas.profit),func.sum(Datas.conversions),func.sum(Datas.impressions),func.sum(Datas.clicks))
            fb_result = fb_data.group_by(Datas.date,Datas.offer_id).all()
            for i in fb_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
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
                            "Source": "facebook"
                        }
                    ]
            ap_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date, Datas.type == "apple").with_entities(Datas.date,Datas.offer_id,func.sum(Datas.revenue),func.sum(Datas.cost),func.sum(Datas.profit),func.sum(Datas.conversions),func.sum(Datas.impressions),func.sum(Datas.clicks))
            ap_result = ap_data.group_by(Datas.date, Datas.offer_id).all()
            for i in ap_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
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
                            "Source": "apple"
                        }
                    ]
            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date,Adwords.offer_id,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.date,Adwords.offer_id)
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
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
                            "Source": "adwords"
                        }
                    ]

            all_data_list = facebook_data + apple_data + adwords_data
            dimission = ["Date", "Offer","Source", "Revenue","Cost","Porfit","Conversions", "CPI","CPC","CVR","CTR","Impressions","Clicks"]
            all_data_list = [
                {
                    "CPI": 0.28,
                    "CTR": 2.05,
                    "Profit": 523.98,
                    "CPC": 0.07,
                    "CVR": 24,
                    "Source": "facebook",
                    "Clicks": 1271,
                    "Conversions": 305,
                    "Offer": 2,
                    "Revenue": 610,
                    "Cost": 86.02,
                    "Date": "2017-02-10",
                    "Impressions": 61940
                },
                {
                    "CPI": 0.5,
                    "CTR": 2.03,
                    "Profit": 284.46,
                    "CPC": 0.08,
                    "CVR": 15.94,
                    "Source": "facebook",
                    "Clicks": 715,
                    "Conversions": 114,
                    "Offer": 3,
                    "Revenue": 342,
                    "Cost": 57.54,
                    "Date": "2017-02-10",
                    "Impressions": 35246
                },
                {
                    "CPI": 0.34,
                    "CTR": 2.05,
                    "Profit": 381.08,
                    "CPC": 0.07,
                    "CVR": 21.2,
                    "Source": "facebook",
                    "Clicks": 1085,
                    "Conversions": 230,
                    "Offer": 2,
                    "Revenue": 460,
                    "Cost": 78.92,
                    "Date": "2017-02-11",
                    "Impressions": 52841
                },
                {
                    "CPI": 0.59,
                    "CTR": 1.95,
                    "Profit": 209.64,
                    "CPC": 0.09,
                    "CVR": 14.55,
                    "Source": "facebook",
                    "Clicks": 598,
                    "Conversions": 87,
                    "Offer": 3,
                    "Revenue": 261,
                    "Cost": 51.36,
                    "Date": "2017-02-11",
                    "Impressions": 30680
                }
            ]
        elif flag == "Offer-3":
            facebook_data = []
            apple_data = []
            fb_data = Datas.query.filter(Datas.date >= start_date, Datas.date <= end_date, Datas.type == "facebook").with_entities(Datas.date,Datas.offer_id,Datas.country,func.sum(Datas.revenue),func.sum(Datas.cost),func.sum(Datas.profit),func.sum(Datas.conversions),func.sum(Datas.impressions),func.sum(Datas.clicks))
            fb_result = fb_data.group_by(Datas.date, Datas.offer_id,Datas.country).all()
            for i in fb_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
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
                            "CTR": ctr
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
                            "GEO": i[2]
                        }
                    ]
            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date, Adwords.offer_id,Adwords.country,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.date, Adwords.offer_id,Adwords.country)
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
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
                            "GEO": i[2]
                        }
                    ]

            all_data_list = facebook_data + apple_data + adwords_data
            dimission = ["Date", "Offer", "Source","GEO", "Revenue", "Cost", "Porfit", "Conversions", "CPI", "CPC", "CVR", "CTR", "Impressions", "Clicks"]
            all_data_list = [
                {
                    "CPI": 0.15,
                    "CTR": 2.08,
                    "Profit": 353.52,
                    "CPC": 0.05,
                    "CVR": 34.35,
                    "Source": "facebook",
                    "Clicks": 556,
                    "Conversions": 191,
                    "Offer": 2,
                    "Revenue": 382,
                    "Cost": 28.48,
                    "Date": "2017-02-10",
                    "Impressions": 26694,
                    "GEO": "MY"
                },
                {
                    "CPI": 0.5,
                    "CTR": 2.03,
                    "Profit": 170.46,
                    "CPC": 0.08,
                    "CVR": 15.94,
                    "Source": "facebook",
                    "Clicks": 715,
                    "Conversions": 114,
                    "Offer": 2,
                    "Revenue": 228,
                    "Cost": 57.54,
                    "Date": "2017-02-10",
                    "Impressions": 35246,
                    "GEO": "TH"
                },
                {
                    "CPI": 0.5,
                    "CTR": 2.03,
                    "Profit": 284.46,
                    "CPC": 0.08,
                    "CVR": 15.94,
                    "Source": "facebook",
                    "Clicks": 715,
                    "Conversions": 114,
                    "Offer": 3,
                    "Revenue": 342,
                    "Cost": 57.54,
                    "Date": "2017-02-10",
                    "Impressions": 35246,
                    "GEO": "TH"
                }
            ]

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
                            "CTR": ctr
                        }
                    ]
            ap_data = DataDetail.query.filter(DataDetail.date >= start_date, DataDetail.date <= end_date,DataDetail.type == 'apple').with_entities(DataDetail.date, DataDetail.offer_id,DataDetail.optName, func.sum(DataDetail.revenue),func.sum(DataDetail.cost), func.sum(DataDetail.profit),func.sum(DataDetail.conversions),func.sum(DataDetail.impressions),func.sum(DataDetail.clicks))
            ap_result = ap_data.group_by(DataDetail.optName, DataDetail.offer_id, DataDetail.date).all()
            for i in ap_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
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
                            "CTR": ctr
                        }
                    ]

            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date, Adwords.offer_id,Adwords.optName,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.date, Adwords.offer_id, Adwords.optName)
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
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
                            "CTR": ctr
                        }
                    ]
            all_data_list = facebook_data + apple_data + adwords_data
            dimission = ["Date", "Offer", "MB","Source", "Revenue", "Cost", "Porfit", "Conversions", "CPI", "CPC", "CVR", "CTR", "Impressions","Clicks"]

            all_data_list = [
                {
                    "CPI": 0.35,
                    "CTR": 1.72,
                    "Profit": 0.3,
                    "CPC": 0.06,
                    "CVR": 17.82,
                    "Source": "facebook",
                    "Clicks": 275,
                    "MB": "oygd66",
                    "Conversions": 49,
                    "Offer": 2,
                    "Revenue": 18.93,
                    "Cost": 17.21,
                    "Date": "2017-02-10",
                    "Impressions": 16006
                },
                {
                    "CPI": 0.44,
                    "CTR": 1.74,
                    "Profit": 11.42,
                    "CPC": 0.08,
                    "CVR": 17.45,
                    "Source": "facebook",
                    "Clicks": 212,
                    "MB": "oygd66",
                    "Conversions": 37,
                    "Offer": 2,
                    "Revenue": 17.77,
                    "Cost": 16.15,
                    "Date": "2017-02-11",
                    "Impressions": 12176
                },
                {
                    "CPI": 0.26,
                    "CTR": 1.44,
                    "Profit": -19.22,
                    "CPC": 0.08,
                    "CVR": 30.07,
                    "Source": "facebook",
                    "Clicks": 306,
                    "MB": "oygd66",
                    "Conversions": 92,
                    "Offer": 2,
                    "Revenue": 26.03,
                    "Cost": 23.66,
                    "Date": "2017-02-12",
                    "Impressions": 21294
                }
            ]

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
                    cpi = float('%0.2f' % (cData(float(i[5]), float(i[7]))))
                    cpc = float('%0.2f' % (cData(float(i[5]), float(i[8]))))
                    cvr = float('%0.2f' % (cData(float(i[7]), float(i[8])) * 100))
                    ctr = float('%0.2f' % (cData(float(i[8]), float(i[8])) * 100))
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
                            "CTR": ctr
                        }
                    ]
            ap_data = DataDetail.query.filter(DataDetail.date >= start_date, DataDetail.date <= end_date,DataDetail.type == 'apple').with_entities(DataDetail.date, DataDetail.offer_id, DataDetail.optName,DataDetail.country, func.sum(DataDetail.revenue),func.sum(DataDetail.cost), func.sum(DataDetail.profit),func.sum(DataDetail.conversions),func.sum(DataDetail.impressions),func.sum(DataDetail.clicks))
            ap_result = ap_data.group_by(DataDetail.optName, DataDetail.offer_id, DataDetail.date, DataDetail.country).all()
            for i in ap_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
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
                            "CTR": ctr
                        }
                    ]
            adword_data = Adwords.query.filter(Adwords.date >= start_date, Adwords.date <= end_date).with_entities(Adwords.date, Adwords.offer_id,Adwords.optName,Adwords.country,func.sum(Adwords.revenue),func.sum(Adwords.cost),func.sum(Adwords.profit),func.sum(Adwords.conversions),func.sum(Adwords.impressions),func.sum(Adwords.clicks))
            adword_result = adword_data.group_by(Adwords.date, Adwords.offer_id, Adwords.optName,Adwords.country)
            for i in adword_result:
                offer_sql = Offer.query.filter_by(id=i[1]).first()
                if offer_sql.status == "deleted":
                    pass
                else:
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
                            "CTR": ctr
                        }
                    ]
            all_data_list = facebook_data + apple_data + adwords_data
            dimission = ["Date", "Offer", "MB","Source","GEO", "Revenue", "Cost", "Porfit", "Conversions", "CPI", "CPC", "CVR", "CTR", "Impressions","Clicks"]

            all_data_list = [
                {
                    "CPI": 0.35,
                    "CTR": 100,
                    "Profit": 0.3,
                    "CPC": 0,
                    "CVR": 0.31,
                    "Source": "facebook",
                    "Clicks": 275,
                    "MB": "oygd66",
                    "Conversions": 49,
                    "Offer": 2,
                    "Revenue": 18.93,
                    "Cost": 17.21,
                    "Date": "2017-02-10",
                    "Impressions": 16006,
                    "GEO": "TH"
                },
                {
                    "CPI": 0.44,
                    "CTR": 100,
                    "Profit": 11.42,
                    "CPC": 0,
                    "CVR": 0.3,
                    "Source": "facebook",
                    "Clicks": 212,
                    "MB": "oygd66",
                    "Conversions": 37,
                    "Offer": 2,
                    "Revenue": 17.77,
                    "Cost": 16.15,
                    "Date": "2017-02-11",
                    "Impressions": 12176,
                    "GEO": "TH"
                },
                {
                    "CPI": 0.26,
                    "CTR": 100,
                    "Profit": -19.22,
                    "CPC": 0,
                    "CVR": 0.43,
                    "Source": "facebook",
                    "Clicks": 306,
                    "MB": "oygd66",
                    "Conversions": 92,
                    "Offer": 2,
                    "Revenue": 26.03,
                    "Cost": 23.66,
                    "Date": "2017-02-12",
                    "Impressions": 21294,
                    "GEO": "TH"
                }
            ]

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