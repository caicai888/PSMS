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
        var id =this.props.params.id?this.props.params.id:"create";
        uploadFile("/api/country_time/"+id,"post","import").then(function (data) {
            var data = JSON.parse(data);
            if(data.code==200){
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
                $("#import").unbind().change(function () {
                    _this.uploadFile();
                });
            }else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
        })
    },
    submit(){
        if(valid("#create_offer","data-required")){
            var data = setForm("#create_offer","data-key");
            data.country=data.country.join(",");
            data.platform=data.platform.join(",");

            if($(".tbd").prop("checked")){
                var newDateArr = data.endTime.toString().split("-");
                newDateArr[0] = parseInt(newDateArr[0])+30;
                data.endTime = newDateArr.join("-");
            }
            console.log(data)

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
                    debugger
                    location.hash = "offer_list";
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
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
            country:_this.state.country,
            offer_id:_this.props.params.id?_this.props.params.id:""
        })).then(function (data) {
            var data = JSON.parse(data);
            if(data.code==200){
                if(!isShow){
                    _this.price();
                }
            }else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
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
            country:e?e.target.dataset.country:_this.state.country,
            offer_id:_this.props.params.id?_this.props.params.id:""
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
                $("#modal").modal("toggle");
            }
        });
    },
    parseFloat(e){
        e.target.value = parseFloat(e.target.value);
    },
    componentDidMount(){
        var _this = this;
        var userSelectPromise = ajax("post","/api/country_select",JSON.stringify({name:""})).then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    tfdq:data.result
                })
            }else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
            return ajax("get","/api/user_select");
        });
        var customerPromise =  userSelectPromise.then(function (data) {
            var data = JSON.parse(data);
            if (data.code == "200") {
                _this.setState({
                    userId: data.result
                })
            } else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
            if(_this.props.params.id){
                return ajax("post","/api/customer_select",JSON.stringify({name:""}))
            }
        });
        if(this.props.params.id){
            sessionStorage.setItem("count","1");
            /*　ｓｅｌｅｃｔ之前为ａｊａｘ获取改为直接调取获取所有的　*/
            customerPromise.then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.setState({
                        khmc:data.result
                    })
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                }
                return ajax("get","/api/offer_detail/"+_this.props.params.id);
            }).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    data.result.platform = data.result.platform.split(",");
                    data.result.country = data.result.country.split(",");
                    getForm("#create_offer",data.result);
                    if(data.result&&data.result.contract_type=="2"){
                        $("#bl").attr("readonly","true").val(0)
                    }else {
                        $("#bl").removeAttr("readonly")
                    }
                    _this.setState({
                        result:data.result.country_detail,
                        country_detail:data.result.country_detail
                    });
                    setTimeout(function () {
                        $(".tfpt").val(data.result.platform.toString().split(",")).trigger("change");
                        $(".tfdq").val(data.result.country.toString().split(",")).trigger("change");
                        $(".khmc").val(data.result.customer_id.toString().split(",")).trigger("change");
                    });
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                }
            });
        }
        function tfdq_price_calendar(arr) {
            let html ="";
            arr.map(function (ele,index,array) {
                html +=`<tr key=${index}>
                    <td>${ele.country}</td>
                    <td><input type="number"  value="${ele.price}" class="tfdq_price form-control" /></td>
                    <td><img  data-country=${ele.country} class="calendar_img" style='cursor:pointer;width:24px' src="./src/img/calender.jpg"/></td>
                </tr>`
            });
            return html;
        }

        $(".tfdq").unbind("change").bind("change",function () {
            var result=_this.state.result;
            var new_result = [];
            var val = $(".tfdq").val();
            for (var i=0;i<val.length;i++){
                for (let ele of result){
                    if(val[i]==ele.country){
                        new_result.push({
                            country:ele.country,
                            price:ele.price?ele.price:""
                        });
                        break;
                    }
                }
                if(!JSON.stringify(result).includes(val[i])) {
                    new_result.push({
                        country: val[i],
                        price: ""
                    });
                }
            }
            $("#tfdq_price_calendar").html(tfdq_price_calendar(new_result));
            $(".calendar_img").unbind("click").bind("click",function (e) {
                _this.price(e);
            });
            $(".tfdq_price").on("change",function () {
                let result=_this.state.result;
                let country_detail =[];
                $("#country_detail tr").map(function (ele,index,array) {
                    var country=$(this).find("td:first").html();
                    var price = $(this).find("input").val();
                    country_detail.push({
                        country:country,
                        price:price
                    });
                });
                _this.setState({
                    result:Object.assign(result,country_detail)
                })
            })
        });
        /*合作方式*/
        $("#hzfs").on("change",function () {
            if($(this).val()=="2"){
                $("#bl").attr("readonly","true").val(0);
            }else {
                $("#bl").removeAttr("readonly");
            }
        })
        /*邮件报告*/
        var html ="";
        for (var i=0;i<24;i++){
            html +=`<option value="${i<10?"0"+i:i}:00">${i<10?"0"+i:i}:00</option><option value="${i<10?"0"+i:i}:30">${i<10?"0"+i:i}:30</option>`
        }
        $("#email_report").html(html);
    },
    bulk_import_save(){
        var text = $("#bulk_import_input").val().toString().toUpperCase()+","+$(".tfdq").val().toString().toUpperCase();
        ajax("post","/api/country_select",JSON.stringify({name:text})).then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                $(".tfdq").val(data.namelist).trigger("change");
            }else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
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
                            <select id="hzfs" className="form-control" data-key="contract_type">
                                <option value="1">服务费</option>
                                <option value="2">CPA</option>
                            </select>
                        </div>
                        <div className="col-sm-3 text-right">
                            比例
                        </div>
                        <div className="col-sm-3">
                            <div className="input-group">
                                <input onBlur={_this.parseFloat} id="bl" type="number" className="form-control"  data-key="contract_scale"/>
                                <div className="input-group-addon">%</div>
                            </div>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            合同编号
                        </div>
                        <div className="col-sm-3">
                            <input type="text" data-required="true" className="form-control"  data-key="contract_num"/>
                        </div>
                        <div className="col-sm-3 text-right">
                            销售
                        </div>
                        <div className="col-sm-3">
                            <select className="form-control"  data-key="user_id">
                                {
                                    this.state.userId.map(function (ele,index,array) {
                                        return <option key={index} value={ele.name+"("+ele.id+")"}>{ele.name+" ("+ele.id+") "}</option>
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
                                <option value="iOS">iOS</option>
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
                            <DateSingle minDate="" maxDate="end_date" id="start_date" require="true" keyword="startTime"/>
                        </div>
                        <div className="col-sm-2 text-right" style={{lineHeight:"34px"}}>
                            投放截止
                        </div>
                        <div className="col-sm-3">
                            <DateSingle maxDate="" minDate="start_date" id="end_date" require="true" keyword="endTime"/>
                        </div>
                        <div className="col-sm-1 text-right">
                            <div className="checkbox" style={{marginTop:"3px"}}>
                                <label>
                                    <input type="checkbox" className="tbd"/> TBD
                                </label>
                            </div>
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
                        <div className="col-sm-6">
                            {
                                <Select  keyword="country"  className="tfdq" placeholder="投放地区．．．"　multiple="true" data={this.state.tfdq}/>
                            }
                            {/*{
                                this.props.params.id?<Select  keyword="country"  className="tfdq" placeholder="投放地区．．．"　multiple="true" data={this.state.tfdq}/>:<AjaxSelect keyword="country" className="tfdq" placeholder="投放地区．．．"　multiple="true" url="/api/country_select" />
                            }*/}
                        </div>
                        <div className="col-md-3">
                            <button data-target="#bulk_import" type="button" className="btn btn-primary" data-toggle="modal" data-target="#bulk_import">
                                批量导入
                            </button>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            投放单价
                        </div>
                        <div className="col-sm-6">
                            <input type="number" data-required="true" className="form-control" data-key="price"/>
                        </div>
                        <div className="col-sm-3">
                            <button type="button" className="btn btn-primary" style={{position:"relative"}}>
                                Import<input type="file" name="file" onChange={this.uploadFile} id="import" style={{position:"absolute",top:0,left:0,right:0,bottom:0,display:'block',opacity:0,zIndex:1}}/>
                            </button>
                        </div>
                    </div>
                    <div className="modal  fade" id="bulk_import">
                        <div className="modal-dialog">
                            <div className="modal-content">
                                <div className="modal-header">
                                    <button type="button" className="close" data-dismiss="modal">
                                        <span aria-hidden="true">&times;</span>
                                        <span className="sr-only">Close</span>
                                    </button>
                                    <h4 className="modal-title">批量导入</h4>
                                </div>
                                <div className="modal-body">
                                    <div className="form-group">
                                        <div className="col-md-2">批量导入</div>
                                        <div className="col-md-10">
                                        <textarea id="bulk_import_input" placeholder=",隔开" className="form-control">

                                        </textarea>
                                        </div>
                                    </div>
                                </div>
                                <div className="modal-footer">
                                    <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
                                    <button onClick={_this.bulk_import_save} type="button" id="bulk_import_save" className="btn btn-primary" data-dismiss="modal">Save</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-sm-10">
                        <div className="col-sm-3"> </div>
                        <div className="col-sm-9 table-responsive">
                            <table className="table table-bordered text-center" id="country_detail">
                                <tbody id="tfdq_price_calendar">
                                    {/*{
                                        this.state.result.map(function (ele,index,array) {
                                            return <tr key={index}>
                                                        <td>{ele.country}</td>
                                                        <td><input type="text" onChange={_this.invalid} defaultValue={ele.price} className="form-control" /></td>
                                                        <td><img onClick={_this.price} data-country={ele.country} className="calendar_img" style={{cursor:"pointer",width:"24px"}} src="./src/img/calender.jpg"/></td>
                                                    </tr>
                                        })
                                    }*/}
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
                            <input type="number" className="form-control" data-key="daily_budget"/>
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
                            <input type="number" className="form-control" data-key="total_budget"/>
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
                            <select type="text" id="email_report" className="form-control" data-key="email_time">

                            </select>
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
                            <a href="javascript:history.go(-1)"  className="btn btn-warning" style={{marginLeft:"20px"}}>Cancel</a>
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
