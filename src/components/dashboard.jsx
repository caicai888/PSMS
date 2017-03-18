import React from "react";
import {ajax} from "../lib/ajax";
import {DateSingle,Daterange} from "./daterange";
require("highcharts");
require("../js/FileSaver");
var tableExport = require("../js/tableExport");

var Dashboard = React.createClass({
    getInitialState() {
        return {
            data_geo:[],
            data_geo_table_head:[],
            data_geo_table_body:[]
        };
    },
    export_table(){
        tableExport("export_table",'ReportTable', 'csv');
    },
    table:function () {
        let _this = this;
        ajax("post","/api/dashboard/table",JSON.stringify({
            start_date:$(".reportRange").val().split(":")[0],
            end_date:$(".reportRange").val().split(":")[1],
            flag:$(".email_tempalte input:checked").val()
        })).then(function (res) {
            var data = JSON.parse(res) || [];
            if (data.code == "200") {
                _this.setState({
                    "data_geo_table_head":data.dimission || [],
                    "data_geo_table_body":data.results || []
                });
            } else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
        });
    },
    getData:function () {
        let _this = this;
        ajax("post","/api/dashboard",JSON.stringify({
            start_date:$(".reportRange").val().split(":")[0],
            end_date:$(".reportRange").val().split(":")[1]
        })).then(function (res) {
            var data = JSON.parse(res) || [];
            if (data.code == "200") {
                var data_geo = [data.count];
                _this.setState({
                    "data_geo":data_geo,
                    "data_geo_table_head":data.dimission || [],
                    "data_geo_table_body":data.table || []
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
            };
            var hightchats = {
                title: {
                    text: ''
                },
                xAxis: {
                    categories: data.range && data.range.date
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
                    data:data.range && strToInt(data.range.Revenue) || []
                }, {
                    name: 'Profit',
                    visible:false,
                    data: data.range && strToInt(data.range.Profit) || []
                }, {
                    name: 'Cost',
                    visible:false,
                    data: data.range && strToInt(data.range.Cost) || []
                }, {
                    name: 'Impressions',
                    visible:false,
                    data: data.range && strToInt(data.range.Impressions) || []
                }, {
                    name: 'Clicks',
                    visible:false,
                    data:data.range && strToInt(data.range.Clicks) || []
                }, {
                    name: 'Conversions',
                    visible:false,
                    data:data.range && strToInt(data.range.Conversions) || []
                }, {
                    name: 'CTR',
                    visible:false,
                    data:data.range && strToInt(data.range.CTR) || []
                }, {
                    name: 'CVR',
                    visible:false,
                    data:data.range && strToInt(data.range.CVR) || []
                }, {
                    name: 'CPC',
                    visible:false,
                    data:data.range && strToInt(data.range.CPC) || []
                }, {
                    name: 'CPI',
                    visible:false,
                    data:data.range && strToInt(data.range.CPI) || []
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


        });
    },
    componentDidMount(){

    },
    render:function () {
        let _this = this;

        /*遍历table_body*/
        let table_body="";
        let body =_this.state.data_geo_table_body||[];
        let head = _this.state.data_geo_table_head;
        body.map(function (obj) {
            table_body+="<tr>"
            head.map(function (key) {
                table_body+="<td>"+obj[key]+"</td>";
            });
            table_body+="</tr>"
        });
        $("#table_body").html(table_body)
        /*遍历table_body*/

        return (
            <div id="report">
                <div className="row">
                    <div className="col-md-3">
                        <input type="hidden" className="reportRange"/>
                        <Daterange onClick={_this.getData} id="reportRange" start="6" end="0" />
                    </div>
                </div>
                <div className="row dashboard_data" style={{marginTop:"15px"}}>
                    {
                        this.state.data_geo.map(function (ele,index,array) {
                            return <div className="col-md-12" key={index}>
                                <div className="box_20">
                                    <p>Revenue($)</p>
                                    <p>{ele.Renvenue}</p>
                                </div>
                                <div className="box_20">
                                    <p>Profit($)</p>
                                    <p>{ele.Profit}</p>
                                </div>
                                <div className="box_20">
                                    <p>Cost($)</p>
                                    <p>{ele.Cost}</p>
                                </div>
                                <div className="box_20">
                                    <p>Impressions</p>
                                    <p>{ele.Impressions}</p>
                                </div>
                                <div className="box_20">
                                    <p>Clicks</p>
                                    <p>{ele.Clicks}</p>
                                </div>
                                <div className="box_20">
                                    <p>Conversions</p>
                                    <p>{ele.Conversions}</p>
                                </div>
                                <div className="box_20">
                                    <p>CTR(%)</p>
                                    <p>{ele.CTR}</p>
                                </div>
                                <div className="box_20">
                                    <p>CVR(%)</p>
                                    <p>{ele.CVR}</p>
                                </div>
                                <div className="box_20">
                                    <p>CPC</p>
                                    <p>{ele.CPC}</p>
                                </div>
                                <div className="box_20">
                                    <p>CPI($)</p>
                                    <p>{ele.CPI}</p>
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
                        <div className="col-xs-6" style={{lineHeight:"34px"}}>
                            Details
                            <button style={{marginLeft:"20px"}} type="button" className="btn btn-warning" data-toggle="modal" data-target="#myModal_detail">
                               <i className="glyphicon glyphicon-plus"> </i> Dimension
                            </button>
                        </div>
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
                        <tbody id="table_body">

                        </tbody>
                    </table>
                </div>
                <div className="modal fade" id="myModal_detail"  role="dialog">
                    <div className="modal-dialog" role="document">
                        <div className="modal-content">
                            <div className="modal-header">
                                <button type="button" className="close" data-dismiss="modal" ><span aria-hidden="true">&times;</span></button>
                                <h4 className="modal-title" id="myModalLabel">Dimension</h4>
                            </div>
                            <div className="modal-body">
                               <div className="row email_tempalte">
                                   <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                       <div className="checkbox">
                                           <label>
                                               <input type="radio" name="Optimization" value={"PM-Data"}　/> PM-Data
                                           </label>
                                       </div>
                                   </div>
                                   <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                       <div className="checkbox">
                                           <label>
                                               <input type="radio" name="Optimization" value={"PM-BD"}　/> PM-BD
                                           </label>
                                       </div>
                                   </div>
                                   <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                       <div className="checkbox">
                                           <label>
                                               <input type="radio" name="Optimization" value={"Offer-1"}　/> Offer-1
                                           </label>
                                       </div>
                                   </div>
                                   <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                       <div className="checkbox">
                                           <label>
                                               <input type="radio" name="Optimization" value={"Offer-2"}　/> Offer-2
                                           </label>
                                       </div>
                                   </div>
                                   <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                       <div className="checkbox">
                                           <label>
                                               <input type="radio" name="Optimization" value={"Offer-3"}　/> Offer-3
                                           </label>
                                       </div>
                                   </div>
                                   <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                       <div className="checkbox">
                                           <label>
                                               <input type="radio" name="Optimization" value={"MB-1"}　/> MB-1
                                           </label>
                                       </div>
                                   </div>
                                   <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                       <div className="checkbox">
                                           <label>
                                               <input type="radio" name="Optimization" value={"MB-2"}　/> MB-2
                                           </label>
                                       </div>
                                   </div>
                               </div>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
                                <button type="button" className="btn btn-primary" data-dismiss="modal" onClick={_this.table}>Save changes</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});
export default  Dashboard;
