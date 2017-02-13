import React from "react";
import {ajax} from "../lib/ajax";
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
        let _this = this;
        if(confirm("确认修改状态吗？")){
            ajax("get","/api/update_offer_status/"+offer_id).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.componentDidMount();
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
        var val = $(e.target).val() || $(e.target).prev().val();
        time = setTimeout(function () {
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
        },500);
    },
    copy(e){
        let offer_id = e.target.dataset.offer_id;
        let _this = this;
        if(confirm("确认复制id为"+offer_id+"的Offer吗？")){
            ajax("post","/api/create_offer",JSON.stringify({offer_id:offer_id})).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.componentDidMount();
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                }
            });
        }
    },
    componentDidMount(){
        var _this = this ;
        ajax("get","/api/offer_show").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    result:data.result,
                    result_search:data.result
                })
            }else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
        });
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
                                <th>销售名称</th>
                                <th>合作模式</th>
                                <th>投放地区</th>
                                <th>单价</th>
                                <th>投放起始</th>
                                <th>投放截止</th>
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
                                                <td>{ele.app_name}</td>
                                                <td>{ele.os}</td>
                                                <td>{ele.customer_id}</td>
                                                <td>{ele.sale_name}</td>
                                                <td>{ele.contract_type}</td>
                                                <td>{ele.country}</td>
                                                <td>{ele.price}</td>
                                                <td>{ele.startTime}</td>
                                                <td>{ele.endTime}</td>
                                                <td>
                                                    <a href={"#/offer_detail/"+ele.offer_id+"/report"} className={_this.state.permissions.includes("report_query")?"":"none"}><img src="./src/img/zx.jpg"/></a>
                                                    <a href={"#/create_offer/"+ele.offer_id} className={_this.state.permissions.includes("offer_edit")?"btn btn-primary":"none"}>Edit</a>
                                                    <a data-offer_id={ele.offer_id} onClick={_this.copy}  style={{marginLeft:"15px"}} className={_this.state.permissions.includes("offer_edit")?"btn btn-warning":"none"}>Copy</a>
                                                </td>
                                                <td>{ele.updateTime}</td>
                                            </tr>
                                })
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
});
export default  OfferList;
