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
            facebook_tfdj:[],
            adwords_tfdj:[],
            apple_tfdj:[],
            tfpt:[{
                id:"Facebook",
                text:"Facebook"
            },{
                id:"Adwords",
                text:"Adwords"
            },{
                id:"Apple",
                text:"Apple"
            }],
            pt:"",//区分是在哪个平台下的批量导入
            khmc:[],
            tfdq:[],
            country:"",
            date:"",
            userId:[],
            hzfs:""
        };
    },
    uploadFile:function (e) {
        var _this = this;
        var pt = _this.state.pt;
        var id =this.props.params.id?this.props.params.id+"_"+pt:"create"+"/"+pt;
        var fileId="";
        if(pt=="facebook"){
            fileId = "import"
        }
        if(pt=="adwords"){
            fileId = "import1"
        }
        if(pt=="apple"){
            fileId = "import2"
        }
        uploadFile("/api/country_time/"+id,"post",fileId).then(function (data) {
            var data = JSON.parse(data);
            if(data.code==200){
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
                $("."+pt+" input[type=file]").unbind().change(function () {
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
            data.platform=data.platform.join(",");
            var classList =["facebook","adwords","apple"];
            for (let i in classList){
                //data[classList[i]]["country"]=data[classList[i]]["country"].join(",");
                if($("."+classList[i]).find(".tbd").prop("checked")){
                    let endTime = data[classList[i]]["endTime"] ;
                    let newDateArr = endTime.split("-");
                    newDateArr[0] = parseInt(newDateArr[0])+30;
                    data[classList[i]]["endTime"] =newDateArr.join("-");
                }
                var country_detail=[];
                $("."+classList[i]+" #country_detail tr").map(function (ele,index,array) {
                    var country=$(this).find("td:first").html();
                    var price = $(this).find("input").val();
                    country_detail.push({
                        country:country,
                        price:price
                    });
                });
                data[classList[i]]["country_detail"] = country_detail;
            }
            /*报告模板*/
            var checked="";
            $(".email_tempalte input:checked").each(function () {
                checked +=$(this).val()+","
            });
            data.email_tempalte =checked.substring(0,checked.length-1);
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
    savePrice(isShow,hzfs){
        var _this = this;
        var result=[];
        var dd = $(".price-calendar dd");
        for(var i =0;i<dd.length;i++){
            var html=$(dd[i]).find(".cal-price").html().toString();
            result.push({
                date:$(".cal-year").html()+"-"+($(".cal-month").html().toString().length<2?"0"+$(".cal-month").html():$(".cal-month").html())+"-"+($(dd[i]).find(".cal-day").html().toString().length<2?"0"+$(dd[i]).find(".cal-day").html():$(dd[i]).find(".cal-day").html()),
                price:html.length>0?(html.indexOf("￥")>-1?html.substring(1):html):""
            })
        }
        var platform="";
        var pt = _this.state.pt;
        if(pt=="facebook"){
            platform="facebook"
        }
        if(pt=="adwords"){
            platform="adwords"
        }
        if(pt=="apple"){
            platform="apple"
        }
        var url="";
        if(Boolean(hzfs)){
            url="/api/contract"
        }else {
            url= "/api/country_time_update"
        }
        ajax("post",url,JSON.stringify({
            result:result,
            country:_this.state.country,
            offer_id:_this.props.params.id?_this.props.params.id:"",
            platform:platform,
            contract_type:$("."+platform+" .hzfs").val()
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
        var pt = e&&e.target.dataset.pt || _this.state.pt;
        _this.setState({
            pt:pt
        });
        var platform="";
        if(pt=="facebook"){
            platform="facebook"
        }
        if(pt=="adwords"){
            platform="adwords"
        }
        if(pt=="apple"){
            platform="apple"
        }
        var url ="/api/country_time_show";
        var hzfs= _this.state.hzfs || e&&e.target.dataset.hzfs || "";
        if(Boolean(hzfs)){
            url="/api/contract_show";
            _this.setState({
                hzfs:"true"
            })
            sessionStorage.setItem("isPrice",true);
        }
        if(e&&e.target.dataset.country){
            url ="/api/country_time_show";
            _this.setState({
                hzfs:""
            })
            sessionStorage.removeItem("isPrice");
        }
        ajax("post",url,JSON.stringify({
            date:(_this.state.date&&moment(this.state.date).format("YYYY-MM")) || moment().format("YYYY-MM"),
            country:e?e.target.dataset.country:_this.state.country,
            offer_id:_this.props.params.id?_this.props.params.id:"",
            platform:platform,
            contract_type:$("."+platform+" .hzfs").val()
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
                    _this.savePrice(false,Boolean(hzfs)?true:"");
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
                    _this.savePrice(false,Boolean(hzfs)?true:"");
                });
                $(".cal-save").on("click",function () {
                    _this.savePrice(true,Boolean(hzfs)?true:"");
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
                });
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
            }else {
                $(".facebook,.adwords,.apple").hide();
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

                    getForm("#create_offer",data.result);

                    //判断合作模式
                    var classList =["facebook","adwords","apple"];
                    for (let i in classList){
                        if(data.result[classList[i]]["contract_type"]==2){
                            $("."+[classList[i]]+" .bl").attr("readonly","true").val(0)
                        }else {
                            $("."+[classList[i]]+" .bl").removeAttr("readonly")
                        }
                    }
                    //判断报告模板
                    $(".email_tempalte input").each(function () {
                        var val = $(this).val();
                        if(data.result.email_tempalte.includes(val)){
                            $(this).prop("checked",true);
                        }
                    })

                    _this.setState({
                        facebook_tfdj:data.result.facebook.country_detail,
                        adwords_tfdj:data.result.adwords.country_detail,
                        apple_tfdj:data.result.apple.country_detail
                    });
                    setTimeout(function () {
                        $(".tfpt").val(data.result.platform.toString().split(",")).trigger("change");
                        $(".facebook .tfdq").val(data.result.facebook.country.toString().split(",")).trigger("change");
                        $(".adwords .tfdq").val(data.result.adwords.country.toString().split(",")).trigger("change");
                        $(".apple .tfdq").val(data.result.apple.country.toString().split(",")).trigger("change");
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
        $(".tfpt").unbind("change").bind("change",function () {
             var val = $(this).val();
             $(".facebook,.adwords,.apple").hide();
             if(val.includes("Facebook")){
                 $(".facebook").show();
             }
             if(val.includes("Adwords")){
                 $(".adwords").show();
             }
             if(val.includes("Apple")){
                 $(".apple").show();
             }
        });

        $(".tfdq").unbind("change").bind("change",function () {
            var result=[];
            if($(this).parents(".tfpt_content").hasClass("facebook")){
                result = _this.state.facebook_tfdj;
                setTimeout(function () {
                    _this.setState({
                        pt:"facebook"
                    })
                })
            }else if($(this).parents(".tfpt_content").hasClass("adwords")){
                result = _this.state.adwords_tfdj;
                setTimeout(function () {
                    _this.setState({
                        pt:"adwords"
                    })
                })
            }else if($(this).parents(".tfpt_content").hasClass("apple")){
                result = _this.state.apple_tfdj;
                setTimeout(function () {
                    _this.setState({
                        pt:"apple"
                    })
                })
            }

            var new_result = [];
            var val = $(this).val();
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
            $(this).parents(".fc_ad_ap").nextAll().find(".tfdq_price_calendar").html(tfdq_price_calendar(new_result));

            $(".calendar_img").unbind("click").bind("click",function (e) {
                _this.price(e);
            });

            $(".tfdq_price").on("change",function () {
                let result=[];
                let tfdq_price＿parent = "";
                if($(this).parents("#country_detail").hasClass("facebook_tfdj")){
                    console.log("facebook")
                    result = _this.state.facebook_tfdj;
                    tfdq_price＿parent ="facebook";
                }else if($(this).parents("#country_detail").hasClass("adwords_tfdj")){
                    console.log("adwords")
                    result = _this.state.adwords_tfdj;
                    tfdq_price＿parent ="adwords";
                }else if($(this).parents("#country_detail").hasClass("apple_tfdj")){
                    console.log("apple")
                    result = _this.state.apple_tfdj;
                    tfdq_price＿parent ="apple";
                }
                let country_detail =[];
                $("."+tfdq_price＿parent+" #country_detail tr").map(function (ele,index,array) {
                    var country = $(this).find("td:first").html();
                    var price = $(this).find("input").val();
                    country_detail.push({
                        country:country,
                        price:price
                    });
                });
                if($(this).parents("#country_detail").hasClass("facebook_tfdj")){
                    _this.setState({
                        facebook_tfdj:Object.assign(result,country_detail)
                    })
                }else if($(this).parents("#country_detail").hasClass("adwords_tfdj")){
                    _this.setState({
                        adwords_tfdj:Object.assign(result,country_detail)
                    })
                }else if($(this).parents("#country_detail").hasClass("apple_tfdj")){
                    _this.setState({
                        apple_tfdj:Object.assign(result,country_detail)
                    })
                }
            })

        });

        /*合作方式*/
        $(".hzfs").on("change",function () {
            if($(this).val()=="2"){
                $(this).parent().nextAll().find(".bl").attr("readonly","true").val(0);
            }else {
                $(this).parent().nextAll().find(".bl").removeAttr("readonly");
            }
        })
        /*报告模板*/
        $(".email_tempalte input").on("click",function () {
            var val = $(this).val();
            if(val==0){
                let flag = false;
                if($(this).prop("checked")){
                    flag=true;
                }
                $(".email_tempalte input").each(function () {
                    $(this).prop("checked",flag);
                })
            }else{
                $(".email_tempalte input:first").prop("checked",false);
            }
        });
        /*邮件报告*/
        var html ="";
        for (var i=0;i<24;i++){
            html +=`<option value="${i<10?"0"+i:i}:00">${i<10?"0"+i:i}:00</option><option value="${i<10?"0"+i:i}:30">${i<10?"0"+i:i}:30</option>`
        }
        $("#email_report").html(html);
    },
    bulk_import_save(){
        var _this = this;
        var text = $("#bulk_import_input").val().toString().toUpperCase()+","+$("."+_this.state.pt+" .tfdq").val().toString().toUpperCase();
        ajax("post","/api/country_select",JSON.stringify({name:text})).then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                $("."+_this.state.pt+" .tfdq").val(data.namelist).trigger("change");
            }else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
        });
    },
    pt(e){
      this.setState({
          pt:e.target.dataset.pt
      })
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
                            合同编号
                        </div>
                        <div className="col-sm-3">
                            <input type="text"  className="form-control"  data-key="contract_num"/>
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
                                <option value="Android">Android</option>
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
                    <div className="col-sm-10">
                        <div className="col-sm-3 text-right">
                            投放平台
                        </div>
                        <div className="col-sm-9">
                            <Select keyword="platform" className="tfpt" placeholder="投放平台"　multiple="true" data={this.state.tfpt}/>
                        </div>
                    </div>
                    <div className="col-sm-12">
                        <hr/>
                    </div>
                    <div className="facebook tfpt_content">
                        <div className="col-sm-12 text-center">
                            Facebook
                        </div>
                        <div className="col-sm-12">
                            <hr/>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                合作方式
                            </div>
                            <div className="col-sm-3">
                                <select  className="form-control hzfs" data-key="facebook.contract_type">
                                    <option value="1">服务费</option>
                                    <option value="2">CPA</option>
                                </select>
                            </div>
                            <div className="col-sm-2 text-right" style={{lineHeight:"34px"}}>
                                比例
                            </div>
                            <div className="col-sm-3">
                                <div className="input-group">
                                    <input onBlur={_this.parseFloat}  type="number" className="form-control bl"  data-key="facebook.contract_scale"/>
                                    <div className="input-group-addon">%</div>
                                </div>
                            </div>
                            <div className="col-sm-1 ">
                                <img onClick={_this.price} data-pt="facebook" data-hzfs="true" style={{cursor:"pointer",width:"24px",marginTop:"5px"}} src="./src/img/calender.jpg"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                制作素材
                            </div>
                            <div className="col-sm-3">
                                <select　className="form-control" data-key="facebook.material">
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
                                <DateSingle minDate="" maxDate="end_date" class="start_date"  keyword="facebook.startTime"/>
                            </div>
                            <div className="col-sm-2 text-right" style={{lineHeight:"34px"}}>
                                投放截止
                            </div>
                            <div className="col-sm-3">
                                <DateSingle maxDate="" minDate="start_date" class="end_date"  keyword="facebook.endTime"/>
                            </div>
                            <div className="col-sm-1 tbd_time">
                                <div className="checkbox" style={{marginTop:"3px"}}>
                                    <label>
                                        <input type="checkbox" className="tbd"/> TBD
                                    </label>
                                </div>
                            </div>
                        </div>
                        <div className="col-sm-10 fc_ad_ap">
                            <div className="col-sm-3 text-right">
                                投放地区
                            </div>
                            <div className="col-sm-6">
                                {
                                    <Select  keyword="facebook.country" style="width:100%" className="tfdq" placeholder="投放地区．．．"　multiple="true" data={this.state.tfdq}/>
                                }
                                {/*{
                                 this.props.params.id?<Select  keyword="country"  className="tfdq" placeholder="投放地区．．．"　multiple="true" data={this.state.tfdq}/>:<AjaxSelect keyword="country" className="tfdq" placeholder="投放地区．．．"　multiple="true" url="/api/country_select" />
                                 }*/}
                            </div>
                            <div className="col-md-3">
                                <button data-target="#bulk_import" data-pt="facebook"　onClick={_this.pt} type="button" className="btn btn-primary" data-toggle="modal" data-target="#bulk_import">
                                    批量导入
                                </button>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                投放单价
                            </div>
                            <div className="col-sm-6">
                                <input type="number"  className="form-control" data-key="facebook.price"/>
                            </div>
                            <div className="col-sm-3">
                                <button type="button" className="btn btn-primary" style={{position:"relative"}}>
                                    Import<input data-pt="facebook" onClick={_this.pt} type="file" name="file" onChange={this.uploadFile} id="import" style={{position:"absolute",top:0,left:0,right:0,bottom:0,display:'block',opacity:0,zIndex:1}}/>
                                </button>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3"> </div>
                            <div className="col-sm-9 table-responsive">
                                <table className="table table-bordered text-center facebook_tfdj" id="country_detail">
                                    <tbody className="tfdq_price_calendar">
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
                                <select className="form-control" data-key="facebook.daily_type">
                                    <option value="install">Install</option>
                                    <option value="cost">Cost($)</option>
                                </select>
                            </div>
                            <div className="col-sm-3">
                                <input type="number" className="form-control" data-key="facebook.daily_budget"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                最高总预算
                            </div>
                            <div className="col-sm-3">
                                <select className="form-control" data-key="facebook.total_type">
                                    <option value="install">Install</option>
                                    <option value="cost">Cost($)</option>
                                </select>
                            </div>
                            <div className="col-sm-3">
                                <input type="number" className="form-control" data-key="facebook.total_budget"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                预算分配
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="facebook.distribution"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                授权账户
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="facebook.authorized"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                命名规则
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="facebook.named_rule"/>
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
                                <input type="text" className="form-control" data-key="facebook.KPI"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                结算标准
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="facebook.settlement"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                账期
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="facebook.period"/>
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
                        <textarea className="form-control" data-key="facebook.remark">

                        </textarea>
                            </div>
                        </div>
                        <div className="col-sm-12">
                            <hr/>
                        </div>
                    </div>
                    <div className="adwords tfpt_content">
                        <div className="col-sm-12 text-center">
                            Adwords
                        </div>
                        <div className="col-sm-12">
                            <hr/>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                合作方式
                            </div>
                            <div className="col-sm-3">
                                <select  className="form-control hzfs" data-key="adwords.contract_type">
                                    <option value="1">服务费</option>
                                    <option value="2">CPA</option>
                                </select>
                            </div>
                            <div className="col-sm-2 text-right" style={{lineHeight:"34px"}}>
                                比例
                            </div>
                            <div className="col-sm-3">
                                <div className="input-group">
                                    <input onBlur={_this.parseFloat}  type="number" className="form-control bl"  data-key="adwords.contract_scale"/>
                                    <div className="input-group-addon">%</div>
                                </div>
                            </div>
                            <div className="col-sm-1 ">
                                <img  onClick={_this.price} data-pt="adwords"  data-hzfs="true" style={{cursor:"pointer",width:"24px",marginTop:"5px"}} src="./src/img/calender.jpg"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                制作素材
                            </div>
                            <div className="col-sm-3">
                                <select　className="form-control" data-key="adwords.material">
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
                                <DateSingle minDate="" maxDate="end_date" class="start_date1" require="true" keyword="adwords.startTime"/>
                            </div>
                            <div className="col-sm-2 text-right" style={{lineHeight:"34px"}}>
                                投放截止
                            </div>
                            <div className="col-sm-3">
                                <DateSingle maxDate="" minDate="start_date" class="end_date1" require="true" keyword="adwords.endTime"/>
                            </div>
                            <div className="col-sm-1 tbd_time">
                                <div className="checkbox" style={{marginTop:"3px"}}>
                                    <label>
                                        <input type="checkbox" className="tbd"/> TBD
                                    </label>
                                </div>
                            </div>
                        </div>
                        <div className="col-sm-10 fc_ad_ap">
                            <div className="col-sm-3 text-right">
                                投放地区
                            </div>
                            <div className="col-sm-6">
                                {
                                    <Select  keyword="adwords.country"  className="tfdq" placeholder="投放地区．．．"　multiple="true" data={this.state.tfdq_adwords}/>
                                }
                                {/*{
                                 this.props.params.id?<Select  keyword="country"  className="tfdq" placeholder="投放地区．．．"　multiple="true" data={this.state.tfdq}/>:<AjaxSelect keyword="country" className="tfdq" placeholder="投放地区．．．"　multiple="true" url="/api/country_select" />
                                 }*/}
                            </div>
                            <div className="col-md-3">
                                <button data-target="#bulk_import" data-pt="adwords"　onClick={_this.pt} type="button" className="btn btn-primary" data-toggle="modal" data-target="#bulk_import">
                                    批量导入
                                </button>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                投放单价
                            </div>
                            <div className="col-sm-6">
                                <input type="number"  className="form-control" data-key="adwords.price"/>
                            </div>
                            <div className="col-sm-3">
                                <button type="button" className="btn btn-primary" style={{position:"relative"}}>
                                    Import<input data-pt="adwords" type="file" onClick={_this.pt} name="file" onChange={this.uploadFile} id="import1" style={{position:"absolute",top:0,left:0,right:0,bottom:0,display:'block',opacity:0,zIndex:1}}/>
                                </button>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3"> </div>
                            <div className="col-sm-9 table-responsive">
                                <table className="table table-bordered text-center adwords_tfdj" id="country_detail">
                                    <tbody className="tfdq_price_calendar">
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
                                <select className="form-control" data-key="adwords.daily_type">
                                    <option value="install">Install</option>
                                    <option value="cost">Cost($)</option>
                                </select>
                            </div>
                            <div className="col-sm-3">
                                <input type="number" className="form-control" data-key="adwords.daily_budget"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                最高总预算
                            </div>
                            <div className="col-sm-3">
                                <select className="form-control" data-key="adwords.total_type">
                                    <option value="install">Install</option>
                                    <option value="cost">Cost($)</option>
                                </select>
                            </div>
                            <div className="col-sm-3">
                                <input type="number" className="form-control" data-key="adwords.total_budget"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                预算分配
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="adwords.distribution"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                授权账户
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="adwords.authorized"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                命名规则
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="adwords.named_rule"/>
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
                                <input type="text" className="form-control" data-key="adwords.KPI"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                结算标准
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="adwords.settlement"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                账期
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="adwords.period"/>
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
                        <textarea className="form-control" data-key="adwords.remark">

                        </textarea>
                            </div>
                        </div>
                        <div className="col-sm-12">
                            <hr/>
                        </div>
                    </div>
                    <div className="apple tfpt_content">
                        <div className="col-sm-12 text-center">
                            Apple
                        </div>
                        <div className="col-sm-12">
                            <hr/>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                合作方式
                            </div>
                            <div className="col-sm-3">
                                <select  className="form-control hzfs" data-key="apple.contract_type">
                                    <option value="1">服务费</option>
                                    <option value="2">CPA</option>
                                </select>
                            </div>
                            <div className="col-sm-2 text-right" style={{lineHeight:"34px"}}>
                                比例
                            </div>
                            <div className="col-sm-3">
                                <div className="input-group">
                                    <input onBlur={_this.parseFloat}  type="number" className="form-control bl"  data-key="apple.contract_scale"/>
                                    <div className="input-group-addon">%</div>
                                </div>
                            </div>
                            <div className="col-sm-1 ">
                                <img  onClick={_this.price} data-pt="apple" data-hzfs="true" style={{cursor:"pointer",width:"24px",marginTop:"5px"}} src="./src/img/calender.jpg"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                制作素材
                            </div>
                            <div className="col-sm-3">
                                <select　className="form-control" data-key="apple.material">
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
                                <DateSingle minDate="" maxDate="end_date" class="start_date2" require="true" keyword="apple.startTime"/>
                            </div>
                            <div className="col-sm-2 text-right" style={{lineHeight:"34px"}}>
                                投放截止
                            </div>
                            <div className="col-sm-3">
                                <DateSingle maxDate="" minDate="start_date" class="end_date2" require="true" keyword="apple.endTime"/>
                            </div>
                            <div className="col-sm-1 tbd_time">
                                <div className="checkbox" style={{marginTop:"3px"}}>
                                    <label>
                                        <input type="checkbox" className="tbd"/> TBD
                                    </label>
                                </div>
                            </div>
                        </div>
                        <div className="col-sm-10 fc_ad_ap">
                            <div className="col-sm-3 text-right">
                                投放地区
                            </div>
                            <div className="col-sm-6">
                                {
                                    <Select  keyword="apple.country"  className="tfdq" placeholder="投放地区．．．"　multiple="true" data={this.state.tfdq_apple}/>
                                }
                                {/*{
                                 this.props.params.id?<Select  keyword="country"  className="tfdq" placeholder="投放地区．．．"　multiple="true" data={this.state.tfdq}/>:<AjaxSelect keyword="country" className="tfdq" placeholder="投放地区．．．"　multiple="true" url="/api/country_select" />
                                 }*/}
                            </div>
                            <div className="col-md-3">
                                <button data-target="#bulk_import" type="button" data-pt="apple"　onClick={_this.pt} className="btn btn-primary" data-toggle="modal" data-target="#bulk_import">
                                    批量导入
                                </button>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                投放单价
                            </div>
                            <div className="col-sm-6">
                                <input type="number"  className="form-control" data-key="apple.price"/>
                            </div>
                            <div className="col-sm-3">
                                <button type="button" className="btn btn-primary" style={{position:"relative"}}>
                                    Import<input data-pt="apple" type="file" onClick={_this.pt} name="file" onChange={this.uploadFile} id="import2" style={{position:"absolute",top:0,left:0,right:0,bottom:0,display:'block',opacity:0,zIndex:1}}/>
                                </button>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3"> </div>
                            <div className="col-sm-9 table-responsive">
                                <table className="table table-bordered text-center apple_tfdj" id="country_detail">
                                    <tbody className="tfdq_price_calendar">
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
                                <select className="form-control" data-key="apple.daily_type">
                                    <option value="install">Install</option>
                                    <option value="cost">Cost($)</option>
                                </select>
                            </div>
                            <div className="col-sm-3">
                                <input type="number" className="form-control" data-key="apple.daily_budget"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                最高总预算
                            </div>
                            <div className="col-sm-3">
                                <select className="form-control" data-key="apple.total_type">
                                    <option value="install">Install</option>
                                    <option value="cost">Cost($)</option>
                                </select>
                            </div>
                            <div className="col-sm-3">
                                <input type="number" className="form-control" data-key="apple.total_budget"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                预算分配
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="apple.distribution"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                授权账户
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="apple.authorized"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                命名规则
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="apple.named_rule"/>
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
                                <input type="text" className="form-control" data-key="apple.KPI"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                结算标准
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="apple.settlement"/>
                            </div>
                        </div>
                        <div className="col-sm-10">
                            <div className="col-sm-3 text-right">
                                账期
                            </div>
                            <div className="col-sm-9">
                                <input type="text" className="form-control" data-key="apple.period"/>
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
                        <textarea className="form-control" data-key="apple.remark">

                        </textarea>
                            </div>
                        </div>
                        <div className="col-sm-12">
                            <hr/>
                        </div>
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
                        <div className="col-sm-9 email_tempalte">
                            {/*<select className="form-control" data-key="email_tempalte">
                                <option value="1">最全数据模板</option>
                            </select>*/}
                            <div className="col-sm-12" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={0} 　/> 全部维度
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={1}　/> Optimization
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={2}　/> Date
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox"　value={3} /> Impression
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={4}　/> GEO
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={5}　/> CVR
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={6}　/> Revenue
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={7}　/> Profit
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={8}　/> Clicks
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={9}　/> Conversions
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={10}　/> CPC
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={11}　/> CPA
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={12}　/> Cost
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={13}　/> CTR
                                    </label>
                                </div>
                            </div>
                            <div className="col-sm-3 col-xs-6" style={{marginTop:"5px"}}>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" value={14}　/> Source
                                    </label>
                                </div>
                            </div>
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
                </div>
            </form>
        )
    }
});
export default  CreateOffer;
