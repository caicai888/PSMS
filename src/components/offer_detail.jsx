import React from "react";
import {ajax} from "../lib/ajax";
import {valid,setForm,getForm} from "../lib/form";
import OfferDetailDetail from "./offer_detail_detail";
import {DateSingle,Daterange} from "./daterange";
require("highcharts");
require("../js/FileSaver");
var tableExport = require("../js/tableExport");

var OfferDetail = React.createClass({
    getInitialState() {
        return {
            "isYes":false, /*判断bind_list是update-save*/
            "adwordsIsYes":false,
            "appleIsYes":false,
            "data_geo":[],
                "data_geo_table_head":[],
            "data_geo_table_clicks_list":[],
                "data_geo_table_conversions_list":[],
            "data_geo_table_cost_list":[],
                "data_geo_table_cpc_list":[],
            "data_geo_table_cpi_list":[],
                "data_geo_table_ctr_list":[],
            "data_geo_table_cvr_list":[],
            "data_geo_table_profit_list":[],
                "data_geo_table_revenue_list":[],
            "data_geo_table_impressions_list":[],
            "permissions":sessionStorage.getItem("permissions")
        };
    },
    export_table(){
        tableExport("export_table",'ReportTable', 'csv');
    },
    campaignNames(){
        ajax("post","/api/bind_detail", JSON.stringify({offer_id:this.props.params.id})).then(function (data) {
            var data = JSON.parse(data);
            if (data.code == "200") {
                $("#campaignName").val(data.campaignNames.join(",").replace(/,/g,"\n"))
            } else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
        });
    },
    submit(e){
        var _this = this;
        var id= e.target.dataset.form_id;
        if(valid(id,"data-required")) {
            var data = setForm(id, "data-key");
            data.advertise_series =data.advertise_series&&data.advertise_series.replace(/[\r\n]/g,",").split(",").filter(function (val) {
                if(val){
                    return val;
                }
            }).join(",") || "";
            data.advertise_groups=data.advertise_groups&&data.advertise_groups.replace(/[\r\n]/g,",").split(",").filter(function (val) {
                if(val){
                    return val;
                }
            }).join(",") || "";
            getForm(id,data);
            let url="";
            if(id=="#create_customer"){
                url= this.state.isYes?"/api/bind_update":"/api/offer_bind";
            }else if(id=="#adwords_form") {
                url= this.state.adwordsIsYes?"/api/bind_update":"/api/offer_bind";
            }else if(id=="#apple_form"){
                url= this.state.adwordsIsYes?"/api/bind_update":"/api/offer_bind";
            }
            ajax("post",url, JSON.stringify(data)).then(function (data) {
                var data = JSON.parse(data);
                if (data.code == "200") {
                    let facebook_form_id = id+" .disable";
                    $(facebook_form_id).attr("disabled",true);
                    if(id=="#create_customer"){
                        _this.campaignNames();
                    }
                } else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                }
            });
        }
    },
    edit(e){
        var id= e.target.dataset.form_id+" .disable";
        $(id).removeAttr("disabled");
    },
    componentDidUpdate(){

    },
    componentDidMount(){
        var _this = this;
        if(this.props.params.three){
            $("#myTab li:last a").tab("show");
        }
        _this.campaignNames();
        ajax("post","/api/bind_show/"+this.props.params.id).then(function (data) {
            var data = JSON.parse(data);
            if (data.code == "200") {
                if(data.facebook&&data.facebook.facebook_id){
                    _this.setState({
                        isYes:true
                    });
                    $("#create_customer .disable").attr("disabled",true);
                    $("#create_customer .ad_id").val(data.facebook.facebook_id);
                    getForm("#create_customer", data.facebook)
                }
                if(data.adwords&&data.adwords.adwords_id){
                    _this.setState({
                        adwordsIsYes:true
                    });
                    $("#adwords_form .disable").attr("disabled",true);
                    $("#adwords_form .ad_id").val(data.adwords.adwords_id);
                    getForm("#adwords_form", data.adwords)
                }
                if(data.apple&&data.apple.apple_id){
                    _this.setState({
                        appleIsYes:true
                    });
                    $("#apple_form .disable").attr("disabled",true);
                    $("#apple_form .ad_id").val(data.apple.apple_id);
                    getForm("#apple_form", data.apple)
                }
            } else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
        });
        $(".report_weidu li").on("click",function () {
            let index = parseInt($(this).index()+1);
            if(!$(this).index()){
                return;
            }
            if($(this).hasClass("active") && index != $(".report_weidu li").length){
                $(this).removeClass("active");
            }else if(index != $(".report_weidu li").length){
                $(this).addClass("active")
            }
            _this.getData();
        })
    },
    getData:function () {
        let _this = this;
        let dimension =[];
        for(let ele of $(".report_weidu li.active")){
            dimension.push($(ele).attr("data-key"));
        }
        let reportData ={
            "offer_id":this.props.params.id,
            "type":"facebook",
            "start_date":$(".reportRange").val().split(":")[0],
            "end_date":$(".reportRange").val().split(":")[1],
            "dimension":dimension
        };
        ajax("post","/api/report",JSON.stringify(reportData)).then(function (res) { //googleads
                var data = JSON.parse(res);
                var isEmptyObject = function(obj) {
                    for (let key in obj) {
                        return true;
                    }
                    return false;
                };
                if (data.code == "200") {
                    var data_geo = [data.data_geo];
                    var data_geo_table =isEmptyObject(data.data_geo_table)?data.data_geo_table:data.data_date_table;
                    _this.setState({
                        "data_geo":data_geo,
                        "data_geo_table_head":data_geo_table.head,
                            "data_geo_table_clicks_list":data_geo_table.clicks_list,
                        "data_geo_table_conversions_list":data_geo_table.conversions_list,
                            "data_geo_table_cost_list":data_geo_table.cost_list,
                        "data_geo_table_cpc_list":data_geo_table.cpc_list,
                            "data_geo_table_cpi_list":data_geo_table.cpi_list,
                        "data_geo_table_ctr_list":data_geo_table.ctr_list,
                            "data_geo_table_cvr_list":data_geo_table.cvr_list,
                            "data_geo_table_profit_list":data_geo_table.profit_list,
                        "data_geo_table_revenue_list":data_geo_table.revenue_list,
                        "data_geo_table_impressions_list":data_geo_table.impressions_list
                    });
                } else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                    return;
                }

                var strToInt = function (array) {
                    var newArr=[];
                    for(var i=0;i<array.length;i++){
                        newArr.push(parseFloat(Number(array[i]).toFixed(2)));
                    }
                    return newArr;
                }
                var hightchats = {
                    title: {
                        text: ''
                    },
                    xAxis: {
                        categories: data.data_range && data.data_range.date
                    },
                    yAxis: {
                        plotLines: [{
                            value: 0,
                            width: 1,
                            color: '#808080'
                        }],
                        labels: {
                            enabled: true
                        }
                    },
                    credits: {
                        enabled: false // 禁用版权信息
                    },
                    legend: {
                        enabled:false
                    },
                    series: [{
                        name: 'Revenue',
                        visible:true,
                        data:data.data_range && strToInt(data.data_range.revenue) || []
                    }, {
                        name: 'Profit',
                        visible:false,
                        data: data.data_range && strToInt(data.data_range.profit) || []
                    }, {
                        name: 'Cost',
                        visible:false,
                        data: data.data_range && strToInt(data.data_range.costs) || []
                    }, {
                        name: 'Impressions',
                        visible:false,
                        data: data.data_range && strToInt(data.data_range.impressions) || []
                    }, {
                        name: 'Clicks',
                        visible:false,
                        data:data.data_range && strToInt(data.data_range.clicks) || []
                    }, {
                        name: 'Conversions',
                        visible:false,
                        data:data.data_range && strToInt(data.data_range.conversions) || []
                    }, {
                        name: 'CTR',
                        visible:false,
                        data:data.data_range && strToInt(data.data_range.ctr) || []
                    }, {
                        name: 'CVR',
                        visible:false,
                        data:data.data_range && strToInt(data.data_range.cvr) || []
                    }, {
                        name: 'CPC',
                        visible:false,
                        data:data.data_range && strToInt(data.data_range.cpc) || []
                    }, {
                        name: 'CPA',
                        visible:false,
                        data:data.data_range && strToInt(data.data_range.cpi) || []
                    }]
                };
                $(".report_zhexian ul li").on("click",function () {
                    var _index = $(this).index();
                    $(this).addClass("active").siblings().removeClass("active");
                    hightchats.series.forEach(function (obj,index) {
                        hightchats.series[index].visible = false;
                    });
                    hightchats.series[_index].visible =true;
                    $('#report_zhexian').highcharts(hightchats);
                })
                $('#report_zhexian').highcharts(hightchats);
        })

    },
    render:function () {
        var _this = this;
        return (
            <div>
                <ul id="myTab" className="nav nav-tabs">
                    <li className="active"><a href="#offer_detail" data-toggle="tab">Offer Detail</a></li>
                    <li className={_this.state.permissions.includes("bind_query")?"":"none"}><a href="#bind_list" data-toggle="tab">Bind List</a></li>
                    <li className={_this.state.permissions.includes("report_query")?"":"none"}><a href="#report"  data-toggle="tab">Report</a></li>
                </ul>
                <div id="myTabContent" className="tab-content" style={{marginTop:"10px"}}>
                    <div className="tab-pane fade in active" id="offer_detail">
                        <OfferDetailDetail id={this.props.params.id} />
                    </div>
                    <div className="tab-pane fade" id="bind_list">
                        <form id="create_customer" className="form-horizontal" role="form" noValidate="noValidate">
                            <div className="row" style={{marginTop:"15px"}}>
                                <div className="col-sm-10">
                                    <div className="col-sm-3 text-right">
                                        Facebook 广告系列关键字
                                    </div>
                                    <div className="col-sm-3">
                                        <textarea className="form-control disable" data-key="advertise_series" placeholder="Enter key or comma separated">

                                        </textarea>
                                    </div>
                                    <div className="col-sm-2 text-right">
                                        绑定的campaign name列表
                                    </div>
                                    <div className="col-sm-4">
                                        <textarea disabled="disabled" id="campaignName" className="form-control"  data-key="campaignNames">

                                        </textarea>
                                    </div>
                                </div>
                            </div>
                            <div className="row" style={{marginTop:"15px"}}>
                                <div className="col-sm-10">
                                    <div className="col-sm-3 text-right">
                                        Facebook　AccountId
                                    </div>
                                    <div className="col-sm-9">
                                    <textarea className="form-control disable" data-key="advertise_groups" placeholder="Enter key or comma separated">

                                    </textarea>
                                    </div>
                                </div>
                            </div>
                            <div className="row" style={{marginTop:"15px"}}>
                                <div className="col-sm-10">
                                    <div className="col-sm-3 text-right"></div>
                                    <div className="col-sm-9">
                                        <input type="hidden" data-key="type" value='facebook'/>
                                        <input type="hidden" data-key="offer_id" value={this.props.params.id}/>
                                        <input type="hidden" data-key="ad_id" className="ad_id"/>
                                        <button data-form_id="#create_customer" onClick={this.submit} type="button" className={_this.state.permissions.includes("bind_create")?"btn btn-primary disable":"none"}>Save</button>
                                        <button data-form_id="#create_customer" onClick={this.edit} type="button" className={_this.state.permissions.includes("bind_edit")?"btn btn-primary":"none"} style={{marginLeft:"20px"}}>Edit</button>
                                        <a href={this.props.params.id?"javascript:history.go(-1)":"javascript:void(0)"} type="button" className="btn btn-warning" style={{marginLeft:"20px"}}>Cancel</a>
                                    </div>
                                </div>
                            </div>
                        </form>
                        <hr/>
                        <form id="adwords_form" className="form-horizontal" role="form" noValidate="noValidate">
                            <div className="row" style={{marginTop:"15px"}}>
                                <div className="col-sm-10">
                                    <div className="col-sm-3 text-right">
                                        Adwords 非UAC
                                    </div>
                                    <div className="col-sm-9">
                                    <textarea className="form-control disable"  data-key="advertise_series" placeholder="Enter key or comma separated">

                                    </textarea>
                                    </div>
                                </div>
                            </div>
                            <div className="row" style={{marginTop:"15px"}}>
                                <div className="col-sm-10">
                                    <div className="col-sm-3 text-right">
                                        Adwords　UAC
                                    </div>
                                    <div className="col-sm-9">
                                    <textarea className="form-control disable"  data-key="advertise_groups" placeholder="Enter key or comma separated">

                                    </textarea>
                                    </div>
                                </div>
                            </div>
                            <div className="row" style={{marginTop:"15px"}}>
                                <div className="col-sm-10">
                                    <div className="col-sm-3 text-right"></div>
                                    <div className="col-sm-9">
                                        <input type="hidden" data-key="type" value='adwords'/>
                                        <input type="hidden" data-key="offer_id" value={this.props.params.id}/>
                                        <input type="hidden" data-key="ad_id" className="ad_id"/>
                                        <button data-form_id="#adwords_form" onClick={this.submit} type="button" className={_this.state.permissions.includes("bind_create")?"btn btn-primary disable":"none"}>Save</button>
                                        <button data-form_id="#adwords_form" onClick={this.edit} type="button" className={_this.state.permissions.includes("bind_edit")?"btn btn-primary":"none"} style={{marginLeft:"20px"}}>Edit</button>
                                        <a href={this.props.params.id?"javascript:history.go(-1)":"javascript:void(0)"} type="button" className="btn btn-warning" style={{marginLeft:"20px"}}>Cancel</a>
                                    </div>
                                </div>
                            </div>
                        </form>
                        <hr/>
                        <form id="apple_form" className="form-horizontal" role="form" noValidate="noValidate">
                            <div className="row" style={{marginTop:"15px"}}>
                                <div className="col-sm-10">
                                    <div className="col-sm-3 text-right">
                                        AppName
                                    </div>
                                    <div className="col-sm-9">
                                    <textarea className="form-control disable"  data-key="advertise_series" placeholder="Enter key or comma separated">

                                    </textarea>
                                    </div>
                                </div>
                            </div>
                            <div className="row" style={{marginTop:"15px"}}>
                                <div className="col-sm-10">
                                    <div className="col-sm-3 text-right"></div>
                                    <div className="col-sm-9">
                                        <input type="hidden" data-key="type" value='apple'/>
                                        <input type="hidden" data-key="offer_id" value={this.props.params.id}/>
                                        <input type="hidden" data-key="ad_id" className="ad_id"/>
                                        <button data-form_id="#apple_form" onClick={this.submit} type="button" className={_this.state.permissions.includes("bind_create")?"btn btn-primary disable":"none"}>Save</button>
                                        <button data-form_id="#apple_form" onClick={this.edit} type="button" className={_this.state.permissions.includes("bind_edit")?"btn btn-primary":"none"} style={{marginLeft:"20px"}}>Edit</button>
                                        <a href={this.props.params.id?"javascript:history.go(-1)":"javascript:void(0)"} type="button" className="btn btn-warning" style={{marginLeft:"20px"}}>Cancel</a>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div className="tab-pane fade" id="report">
                        <div className="row">
                            <div className="col-md-3">
                                <input type="hidden" className="reportRange"/>
                                <Daterange onClick={_this.getData} id="reportRange" start="1" end="1" />
                            </div>
                            <div className="col-md-4">
                                <ul className="box-center report_weidu">
                                    <li data-key="date" className="active">Day</li>
                                    <li data-key="geo">Geo</li>
                                    <li data-key="source">Source</li>
                                    <li style={{display:"none"}}>选择日期用这个（最笨的办法）</li>
                                </ul>
                            </div>
                            {/*<div className="col-md-2 pull-right allSlot">
                                <select className="form-control">
                                    <option value="all_slot">All Slot</option>
                                </select>
                            </div>*/}
                        </div>
                        <div className="row dashboard_data">
                            {
                                this.state.data_geo.map(function (ele,index,array) {
                                    return <div className="col-md-12" key={index}>
                                            <div className="box_20">
                                                <p>Revenue($)</p>
                                                <p>{ele.revenue}</p>
                                            </div>
                                            <div className="box_20">
                                                <p>Profit($)</p>
                                                <p>{ele.profit}</p>
                                            </div>
                                            <div className="box_20">
                                                <p>Cost($)</p>
                                                <p>{ele.count_cost}</p>
                                            </div>
                                            <div className="box_20">
                                                <p>Impressions</p>
                                                <p>{ele.count_impressions}</p>
                                            </div>
                                            <div className="box_20">
                                                <p>Clicks</p>
                                                <p>{ele.count_clicks}</p>
                                            </div>
                                            <div className="box_20">
                                                <p>Conversions</p>
                                                <p>{ele.count_conversions}</p>
                                            </div>
                                            <div className="box_20">
                                                <p>CTR(%)</p>
                                                <p>{ele.count_ctr}</p>
                                            </div>
                                            <div className="box_20">
                                                <p>CVR(%)</p>
                                                <p>{ele.count_cvr}</p>
                                            </div>
                                            <div className="box_20">
                                                <p>CPC</p>
                                                <p>{ele.count_cpc}</p>
                                            </div>
                                            <div className="box_20">
                                                <p>CPI($)</p>
                                                <p>{ele.count_cpi}</p>
                                            </div>
                                        </div>
                                })
                            }
                        </div>
                        <div className="row report_report">
                            <div className="col-md-12">
                                <div className="report_zhexian">
                                    <ul>
                                        <li className="active">Revenue</li>
                                        <li>Profit</li>
                                        <li>Cost</li>
                                        <li>Impressions</li>
                                        <li>Clicks</li>
                                        <li>Conversions</li>
                                        <li>CTR</li>
                                        <li>CVR</li>
                                        <li>CPC</li>
                                        <li>CPI</li>
                                        <div className="clear"></div>
                                    </ul>
                                </div>
                            </div>
                            <div className="col-md-12 report_overflow">
                                <div id="report_zhexian">

                                </div>
                            </div>
                        </div>
                        <div className="row" style={{marginTop:"15px"}}>
                            <div className="col-xs-12 date_detail">
                                <div className="col-xs-6" style={{lineHeight:"34px"}}>Details</div>
                                <div className="col-xs-6 text-right">
                                    <button onClick={_this.export_table} className="btn btn-primary">Export</button>
                                </div>
                            </div>
                        </div>
                        <div className="table-responsive" style={{marginTop:"15px"}}>
                            <table id="export_table" className="table table-bordered">
                                <thead>
                                    <tr>
                                    {
                                        _this.state.data_geo_table_head.map(function (ele,index,array) {
                                            return <th key={index}>{ele}</th>
                                        })
                                    }
                                    </tr>
                                </thead>
                                <tbody>
                                {
                                    _this.state.data_geo_table_impressions_list.map(function (ele,index,array) {
                                        return <tr key={index}>
                                                    <td>{ele.date_start}</td>
                                                    {
                                                        ele.country?<td>{ele.country}</td>:""
                                                    }
                                                    {
                                                        ele.source?<td>{ele.source}</td>:""
                                                    }
                                                    <td>{ _this.state.data_geo_table_revenue_list[index].revenue }</td>
                                                    <td>{ _this.state.data_geo_table_profit_list[index].profit }</td>
                                                    <td>{ _this.state.data_geo_table_cost_list[index].spend }</td>
                                                    <td>{ _this.state.data_geo_table_impressions_list[index].impressions }</td>
                                                    <td>{ _this.state.data_geo_table_clicks_list[index].clicks }</td>
                                                    <td>{ _this.state.data_geo_table_conversions_list[index].conversions }</td>
                                                    <td>{ _this.state.data_geo_table_ctr_list[index].ctr }</td>
                                                    <td>{ _this.state.data_geo_table_cvr_list[index].cvr }</td>
                                                    <td>{ _this.state.data_geo_table_cpc_list[index].cpc }</td>
                                                    <td>{ _this.state.data_geo_table_cpi_list[index].cpi }</td>
                                                </tr>
                                    })
                                }
                                </tbody>
                            </table>
                        </div>

                    </div>
                </div>
            </div>
        )
    }
});
module.exports = OfferDetail;
