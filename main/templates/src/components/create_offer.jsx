import React from "react";
import {Select,AjaxSelect} from "./select";
import {DateSingle,Daterange} from "./daterange";
require("../lib/price-calendar");
import {valid,setForm,getForm} from "../lib/form";
import {ajax} from "../lib/ajax";
import {uploadFile} from "../lib/uploadFile";
import moment from "moment";

var CreateOffer = React.createClass({
    getInitialState() {
        return {
            result:[],
            tfpt:[{
                id:"Facebook",
                text:"Facebook"
            },{
                id:"Adwords",
                text:"Adwords"
            }],
            khmc:[],
            tfdq:[],
            country:"",
            date:"",
            country_detail:[],
            userId:[]
        };
    },
    uploadFile:function () {
        var _this = this;
        uploadFile("/api/country_time","post","import").then(function (data) {
            var data = JSON.stringify(data);
            if(data.code==200){
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
                $("#import").unbind().change(function () {
                    _this.uploadFile();
                });
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        })
    },
    submit(){
        if(valid("#create_offer","data-required")){
            var data = setForm("#create_offer","data-key");
            var country_detail=[];
            $("#country_detail tr").map(function (ele,index,array) {
                var country=$(this).find("td:first").html();
                var price = $(this).find("input").val();
                country_detail.push({
                    country:country,
                    price:price
                });
            });
            var data = Object.assign(data,{country_detail:country_detail,flag:["country_detail"]});
            var url = this.props.params.id?"/api/update_offer":"/api/create_offer";
            ajax("post",url,JSON.stringify(data)).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    location.hash = "offer_list";
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                }
            });
        }else {
            $(".has-error input:first").focus();
        }
    },
    savePrice(isShow){
        var _this = this;
        var result=[];
        var dd = $(".price-calendar dd");
        for(var i =0;i<dd.length;i++){
            result.push({
                date:$(".cal-year").html()+"-"+($(".cal-month").html().toString().length<2?"0"+$(".cal-month").html():$(".cal-month").html())+"-"+($(dd[i]).find(".cal-day").html().toString().length<2?"0"+$(dd[i]).find(".cal-day").html():$(dd[i]).find(".cal-day").html()),
                price:$(dd[i]).find(".cal-price").html().length>0?$(dd[i]).find(".cal-price").html().toString().substring(1):""
            })
        }
        ajax("post","/api/country_time_update",JSON.stringify({
            result:result,
            country:_this.state.country
        })).then(function (data) {
            var data = JSON.parse(data);
            if(data.code==200){
                if(!isShow){
                    _this.price();
                }
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        })
    },
    price(e){
        var _this = this;
        if(e){
            _this.setState({
                country:e.target.dataset.country
            })
        }
        ajax("post","/api/country_time_show",JSON.stringify({
            date:(_this.state.date&&moment(this.state.date).format("YYYY-MM")) || moment().format("YYYY-MM"),
            country:e?e.target.dataset.country:_this.state.country
        })).then(function (data) {
            var data = JSON.parse(data);
            if(data.code==200){
                $("#price-calendar").priceCalendar({
                    date:_this.state.date || moment()._d
                },data.result);
                $(".price-calendar").show();

                $(".cal-prev").on('click',function () {
                    var year = +$(".cal-year").text();
                    var month = $(".cal-month").text() - 1;
                    if (month < 1) {
                        year -= 1;
                        month = 12;
                    }
                    var date = new Date(year, month-1,1);
                    _this.setState({date:date});
                    _this.savePrice();
                });

                // 下一月
                $(".cal-next").on('click',function () {
                    var year = +$(".cal-year").text();
                    var month = +$(".cal-month").text() + 1;
                    if (month > 12) {
                        year += 1;
                        month = 1;
                    }
                    var date = new Date(year, month-1,1);
                    _this.setState({date:date});
                    _this.savePrice();
                });
                $(".cal-save").on("click",function () {
                    _this.savePrice(true);
                    $(".price-calendar").hide();
                });
                $(".cal-cancel").on("click",function () {
                    $(".price-calendar").hide();
                });
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        });
    },
    componentDidMount(){
        var _this = this;
        ajax("get","/api/user_select").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    userId:data.result
                })
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        });
        if(this.props.params.id){
            sessionStorage.setItem("count","1");
            /*　ｓｅｌｅｃｔ之前为ａｊａｘ获取改为直接调取获取所有的　*/
            ajax("post","/api/country_select",JSON.stringify({name:""})).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.setState({
                        tfdq:data.result
                    })
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                }
                return ajax("post","/api/customer_select",JSON.stringify({name:""}));
            }).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.setState({
                        khmc:data.result
                    })
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                }
                return ajax("get","/api/offer_detail/"+_this.props.params.id);
            }).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    var strToarr = function (arr,newArr) {
                        for(var i=0;i<arr.length;i++){
                            var indexOf =arr[i].indexOf("'")+1;
                            var lastIndexOf = arr[i].lastIndexOf("'");
                            newArr.push(arr[i].substring(indexOf,lastIndexOf));
                        }
                    };
                    //转换ｓｅｌｅｃｔ框
                    var platform = [];
                    var dataPlatform =data.result.platform.split(",");
                    strToarr(dataPlatform,platform);
                    var country =[];
                    var dataCountry = data.result.country.split(",");
                    strToarr(dataCountry,country);

                    data.result.platform = platform;
                    data.result.country = country;
                    getForm("#create_offer",data.result);
                    _this.setState({
                        result:data.result.country_detail,
                        country_detail:data.result.country_detail
                    });
                    setTimeout(function () {
                        $(".tfpt").val(data.result.platform).trigger("change");
                        $(".tfdq").val(data.result.country).trigger("change");
                    });
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                }
            });
        }

        $(".tfdq").on("change",function () {
            var result=_this.state.result;
            var new_result = [];
            var val = $(".tfdq").val();
            for (var i=0;i<val.length;i++){
                new_result.push({
                    country:val[i],
                    price:(result.length>i)&&result[i].price?result[i].price:""
                })
            }
            setTimeout(function () {
                _this.setState({
                    result:new_result
                });
            });
        });

    },
    render:function () {
        var _this = this;
        return (
            <form id="create_offer" className="form-horizontal" role="form" noValidate="noValidate">
                <div id="create_offer" className="row">
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            客户名称
                        </div>
                        <div className="col-sm-3" id="khmc">
                            {
                                this.props.params.id?<Select keyword="customer_id" value="" className="khmc" placeholder="客户名称．．．"　multiple="false" data={this.state.khmc}/>:<AjaxSelect keyword="customer_id"  className="khmc" placeholder="客户名称．．．"　multiple="false" url="/api/customer_select" />
                            }
                        </div>
                        <div className="col-sm-3 text-right">
                            Status
                        </div>
                        <div className="col-sm-3">
                            <select className="form-control" data-key="status">
                                <option value="inactive">Inactive</option>
                                <option value="active">Active</option>
                            </select>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            合作方式
                        </div>
                        <div className="col-sm-3">
                            <select className="form-control" data-key="contract_type">
                                <option value="服务费">服务费</option>
                                <option value="cpa">cpa</option>
                            </select>
                        </div>
                        <div className="col-sm-3 text-right">
                            比例
                        </div>
                        <div className="col-sm-3">
                            <input type="number" className="form-control"  data-key="contract_scale"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            合同编号
                        </div>
                        <div className="col-sm-3">
                            <input type="text" className="form-control"  data-key="contract_num"/>
                        </div>
                        <div className="col-sm-3 text-right">
                            销售
                        </div>
                        <div className="col-sm-3">
                            <select className="form-control"  data-key="user_id">
                                {
                                    this.state.userId.map(function (ele,index,array) {
                                        return <option key={index} value={ele.id}>{ele.name+" ("+ele.id+") "}</option>
                                    })
                                }
                            </select>
                        </div>
                    </div>
                    <div className="col-sm-12">
                        <hr/>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            操作系统
                        </div>
                        <div className="col-sm-3">
                            <select className="form-control" data-key="os">
                                <option value="ios">IOS</option>
                                <option value="android">Android</option>
                            </select>
                        </div>
                        <div className="col-sm-3 text-right">
                            包名
                        </div>
                        <div className="col-sm-3">
                            <input type="text" className="form-control" data-key="package_name"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            APP 名称
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="app_name"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            APP 类型
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="app_type"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            Preview Link
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="preview_link"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            Tracking Link
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="track_link"/>
                        </div>
                    </div>
                    <div className="col-sm-12">
                        <hr/>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            制作素材
                        </div>
                        <div className="col-sm-3">
                            <select　className="form-control" data-key="material">
                                <option value="yes">Yes</option>
                                <option value="no">No</option>
                            </select>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            投放起始
                        </div>
                        <div className="col-sm-3">
                            <DateSingle id="start_date" keyword="startTime"/>
                        </div>
                        <div className="col-sm-3 text-right">
                            投放截止
                        </div>
                        <div className="col-sm-3">
                            <DateSingle id="end_date" keyword="endTime"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            投放平台
                        </div>
                        <div className="col-sm-9">
                            <Select keyword="platform" className="tfpt" placeholder="投放平台"　multiple="true" data={this.state.tfpt}/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            投放地区
                        </div>
                        <div className="col-sm-9">
                            {
                                this.props.params.id?<Select  keyword="country"  className="tfdq" placeholder="投放地区．．．"　multiple="true" data={this.state.tfdq}/>:<AjaxSelect keyword="country" className="tfdq" placeholder="投放地区．．．"　multiple="true" url="/api/country_select" />
                            }
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            投放单价
                        </div>
                        <div className="col-sm-6">
                            <input type="number" className="form-control" data-key="price"/>
                        </div>
                        <div className="col-sm-3" style={{position:"relative"}}>
                            <input type="file" name="file" onChange={this.uploadFile} id="import" style={{position:"absolute",top:0,left:0,right:0,bottom:0,display:'block',opacity:0,zIndex:1}}/>
                            <button type="button" className="btn btn-primary">Import</button>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3"> </div>
                        <div className="col-sm-9 table-responsive">
                            <table className="table table-bordered text-center" id="country_detail">
                                <tbody>
                                    {
                                        this.state.result.map(function (ele,index,array) {
                                            return <tr key={index}>
                                                        <td>{ele.country}</td>
                                                        <td><input type="number" defaultValue={ele.price} className="form-control" /></td>
                                                        <td><img onClick={_this.price} data-country={ele.country} className="calendar_img" style={{cursor:"pointer",width:"24px"}} src="./src/img/calender.jpg"/></td>
                                                    </tr>
                                        })
                                    }
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            最高日预算
                        </div>
                        <div className="col-sm-3">
                            <select className="form-control" data-key="daily_type">
                                <option value="install">Install</option>
                                <option value="cost">Cost($)</option>
                            </select>
                        </div>
                        <div className="col-sm-3">
                            <input type="text" className="form-control" data-key="daily_budget"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            最高总预算
                        </div>
                        <div className="col-sm-3">
                            <select className="form-control" data-key="total_type">
                                <option value="install">Install</option>
                                <option value="cost">Cost($)</option>
                            </select>
                        </div>
                        <div className="col-sm-3">
                            <input type="text" className="form-control" data-key="total_budget"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            预算分配
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="distribution"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            授权账户
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="authorized"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            命名规则
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="named_rule"/>
                        </div>
                    </div>
                    <div className="col-sm-12">
                        <hr/>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            KPI　要求
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="KPI"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            结算标准
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="settlement"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            账期
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="period"/>
                        </div>
                    </div>
                    <div className="col-sm-12">
                        <hr/>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            备注
                        </div>
                        <div className="col-sm-9">
                        <textarea className="form-control" data-key="remark">

                        </textarea>
                        </div>
                    </div>
                    <div className="col-sm-12">
                        <hr/>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            邮件报告
                        </div>
                        <div className="col-sm-9">
                            <input type="text" className="form-control" data-key="email_time"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">

                        </div>
                        <div className="col-sm-9">
                            <input type="text" data-key="email_users" className="form-control" placeholder="xx@xx.com,xx@xx.com"/>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            报告模板
                        </div>
                        <div className="col-sm-9">
                            <select className="form-control" data-key="email_tempalte">
                                <option value="1">最全数据模板</option>
                            </select>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">

                        </div>
                        <div className="col-sm-9">
                            <input type="hidden" data-key="offer_id" value={this.props.params.id}/>
                            <button type="button" onClick={this.submit} className="btn btn-primary">Create/Update</button>
                            <a href={this.props.params.id?"javascript:history.go(-1)":"javascript:void(0)"}  className="btn btn-warning" style={{marginLeft:"20px"}}>Cancel</a>
                        </div>
                    </div>
                    <div className="price-calendar">
                        <div className="mask_mask box-center">
                            <div id="price-calendar"></div>
                        </div>
                    </div>
                </div>
            </form>
        )
    }
});
export default  CreateOffer;
