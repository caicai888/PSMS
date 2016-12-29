import React from "react";
import {ajax} from "../lib/ajax";
require("../js/FileSaver");
var tableExport = require("../js/tableExport");
var time = null;
var CustomerList = React.createClass({
    getInitialState() {
        return {
            result:[],
            result_search:[]
        };
    },
    export_table(){
      tableExport("export_table",'ReportTable', 'csv');
    },
    search_table(e){
        clearTimeout(time);
        var _this = this;
        var val = $(e.target).val()  || $(e.target).prev().val();
        time = setTimeout(function () {
            if(val){
                var newResult = [];
                for (let elem of _this.state.result_search){
                    if(Object.values(elem).join('').includes(val)){
                        newResult.push(elem)
                    }
                }
                _this.setState({result:newResult});
            }else{
                _this.setState({result:_this.state.result_search});
            }
        },500);
    },
    delete_customer(e){
        var id = e.target.dataset.key;
        var index = e.target.dataset.index;
        var _this = this;
        if(confirm("确认删除ｉｄ为"+id+"的客户吗？")){
            ajax("post","/api/customers/delete/"+id).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                    _this.state.result.splice(index,1);
                    _this.setState({
                        result:_this.state.result,
                        result_search:_this.state.result
                    });
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                }
            });
        }
    },
    componentDidMount(){
        var _this = this ;
        ajax("get","/api/customers").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    result:data.results,
                    result_search:data.results
                })
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        });
    },
    render:function () {
        var _this = this;
        return (
            <div>
                <div className="row">
                    <div className="col-md-8">&nbsp;</div>
                    <div className="form-group col-md-4 text-right">
                        <div className="input-group">
                            <div style={{cursor:"pointer"}} onClick={_this.export_table} className="input-group-addon">Export</div>
                            <input onKeyUp={_this.search_table}  className="form-control" type="email" placeholder="Search..." />
                            <div style={{cursor:"pointer"}} onClick={_this.search_table} className="input-group-addon">Search</div>
                        </div>
                    </div>
                </div>
                <div className="table-responsive">
                    <table id="export_table" className="table table-bordered">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>客户编码</th>
                                <th>客户名称</th>
                                <th>公司名称</th>
                                <th>公司地址</th>
                                <th>备注</th>
                                <th>最后修改</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                this.state.result.map(function (item,index,array) {
                                    return  <tr key={index}>
                                                <td>{item.customers_id}</td>
                                                <td>{item.customer_code}</td>
                                                <td>{item.company_name}</td>
                                                <td>{item.company_name}</td>
                                                <td>{item.company_address}</td>
                                                <td>{item.comment}</td>
                                                <td>{item.last_datetime}</td>
                                                <td>
                                                    <a href={"#/create_customer/"+item.customers_id} className="btn btn-primary">Edit</a>&nbsp;&nbsp;&nbsp;
                                                    <a data-index={index} data-key={item.customers_id}  onClick={_this.delete_customer} className="btn btn-danger">Delete</a>
                                                </td>
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
export default  CustomerList;
