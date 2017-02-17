import React from "react";
import {ajax} from "../lib/ajax";
import {Page} from "./page";
require("../js/FileSaver");
var tableExport = require("../js/tableExport");
var time = null;

var OfferList = React.createClass({
    getInitialState() {
        return {
            result:[],
            result_search:[],
            permissions:sessionStorage.getItem("permissions")
        };
    },
    export_table(){
        tableExport("export_table",'ReportTable', 'csv');
    },
    status(e){
        let offer_id = e.target.dataset.offer_id;
        let confirmMessage = e.target.dataset.isDelete?"确认删除吗？":"确认修改状态吗？";
        let method =e.target.dataset.isDelete?"post":"get";
        let _this = this;
        if(confirm(confirmMessage)){
            ajax(method,"/api/update_offer_status/"+offer_id).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.offerList();
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                }
            });
        }
    },
    search_table(e){
        clearTimeout(time);
        var _this = this;
        var val = $(e.target).val();
        time = setTimeout(function () {
            ajax("post","/api/offer_search",JSON.stringify({key:val})).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.setState({
                        result:data.result,
                        totalPages:data.totalPages || 1,
                        page:1
                    })
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                }
            });
            /* 前端搜索
            if(val){
                var newResult = [];
                for (let elem of _this.state.result_search){
                    if(Object.values(elem).join('').includes(val)){
                        newResult.push(elem)
                    }
                }
                console.log(newResult)
                _this.setState({result:newResult});
            }else{
                _this.setState({result:_this.state.result_search});
            }
            */
        },500);
    },
    copy(e){
        let offer_id = e.target.dataset.offer_id;
        let _this = this;
        if(confirm("确认复制id为"+offer_id+"的Offer吗？")){
            ajax("post","/api/create_offer",JSON.stringify({offer_id:offer_id})).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.offerList();
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                }
            });
        }
    },
    allPrice(e){
        let eleObj = $(e.target);
        let offer_id = e.target.dataset.offer_id;
        if(eleObj.hasClass("allPrice_active")){
            eleObj.removeClass("allPrice_active");
            eleObj.parents("tr").nextAll(".country_price").remove();
            return false;
        }else {
            eleObj.addClass("allPrice_active");
            ajax("get","/api/country_price/"+offer_id).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    var html ="";
                    for(let obj of data.result){
                        html+=`<tr class='country_price'><td colspan='6'></td><td>${obj.country}</td><td>${obj.price}</td><td colspan='5'></td></tr>`;
                    }
                    eleObj.parents("tr").after(html)
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                }
            });
        }
    },
    offerList(page,limit){
        let _this = this ;
        ajax("post","/api/offer_show",JSON.stringify({
            page:page||1,
            limit:limit||15
        })).then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    result:data.result,
                    result_search:data.result,
                    totalPages:data.totalPages,
                    page:page||1
                })
            }else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
        });
    },
    componentDidMount(){
        this.offerList();
    },
    componentWillUpdate(){
        $(".allPrice").removeClass("allPrice_active");
        $(".country_price").remove();
    },
    render:function () {
        let _this = this;
        return (
            <div id="offer_list">
                <div className="row">
                    <div className="col-md-8">&nbsp;</div>
                    <div className="form-group col-md-4 text-right">
                        <div className="input-group">
                            <div onClick={_this.export_table} className="input-group-addon">Export</div>
                            <input onKeyUp={_this.search_table} className="form-control" type="text" placeholder="Search..." />
                            <div onClick={_this.search_table} className="input-group-addon">Search</div>
                        </div>
                    </div>
                </div>
                <div className="table-responsive">
                    <table id="export_table" className="table table-bordered text-center">
                        <thead>
                            <tr>
                                <th>Status</th>
                                <th>Offer ID</th>
                                <th>应用名称</th>
                                <th>系统</th>
                                <th>客户名称</th>
                                <th>合作模式</th>
                                <th>投放地区</th>
                                <th>单价</th>
                                <th>投放起始</th>
                                <th>投放截止</th>
                                <th>销售名称</th>
                                <th>操作</th>
                                <th>最后修改</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                _this.state.result.map(function (ele,index,array) {
                                    return <tr key={index}>
                                                <td >
                                                    <div data-offer_id={ele.offer_id}  onClick={_this.status} className={ele.status=='active'?'isTrue':''}></div>
                                                    <span style={{display:'none'}}>{ele.status=='active'?'Active':'Inactive'}</span>
                                                </td>
                                                <td><a href={"#/offer_detail/"+ele.offer_id}>{ele.offer_id}</a></td>
                                                <td title={ele.app_name}>{ele.app_name}</td>
                                                <td>{ele.os}</td>
                                                <td>{ele.customer_id}</td>
                                                <td>{ele.contract_type}</td>
                                                <td>{ele.country}</td>
                                                <td><span className="onePrice">{ele.price}</span> <span data-offer_id={ele.offer_id} onClick={_this.allPrice} className="allPrice">&lt;</span></td>
                                                <td>{ele.startTime}</td>
                                                <td>{ele.endTime}</td>
                                                <td>{ele.sale_name}</td>
                                                <td>
                                                    <a href={"#/offer_detail/"+ele.offer_id+"/report"} className={_this.state.permissions.includes("report_query")?"":"none"}><img src="./src/img/zx.jpg"/></a>
                                                    <a href={"#/create_offer/"+ele.offer_id} className={_this.state.permissions.includes("offer_edit")?"btn btn-primary":"none"}>Edit</a>
                                                    <a data-offer_id={ele.offer_id} onClick={_this.copy}  style={{marginLeft:"15px"}} className={_this.state.permissions.includes("offer_edit")?"btn btn-warning":"none"}>Copy</a>
                                                    <a data-is-delete="true" data-offer_id={ele.offer_id} onClick={_this.status} style={{marginLeft:"15px"}} className={_this.state.permissions.includes("offer_edit")?"btn btn-danger":"none"}>Delete</a>
                                                </td>
                                                <td>{ele.updateTime}</td>
                                            </tr>
                                })
                            }
                        </tbody>
                    </table>
                </div>
                <Page id="offerListPage" limit="15" totalPages={_this.state.totalPages} onClick={_this.offerList} page={_this.state.page}/>
            </div>
        )
    }
});
export default  OfferList;
