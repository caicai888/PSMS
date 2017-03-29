import React from "react";
import {ajax} from "../lib/ajax";
require("../js/FileSaver");
var tableExport = require("../js/tableExport");
var time = null;

var AgentList = React.createClass({
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
    componentDidMount(){
        let _this = this;
        ajax("get","/api/rebate/show").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    result:data.results,
                    result_search:data.results
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
            <div className="row animated slideInDown">
                <div className="col-md-8">&nbsp;</div>
                <div className="form-group col-md-4 text-right">
                    <div className="input-group">
                        <div style={{cursor:"pointer"}} onClick={_this.export_table} className="input-group-addon">Export</div>
                        <input onKeyUp={_this.search_table}  className="form-control" type="email" placeholder="Search..." />
                        <div style={{cursor:"pointer"}} onClick={_this.search_table} className="input-group-addon">Search</div>
                    </div>
                </div>
                <div className="col-sm-12">
                    <div className="table-responsive">
                        <table id="export_table" className="table table-bordered">
                            <thead>
                            <tr>
                                <th>ID</th>
                                <th>代理商名字</th>
                                <th>返点比例</th>
                                <th>关键词</th>
                                <th>平台</th>
                                <th>操作</th>
                            </tr>
                            </thead>
                            <tbody>
                            {
                                this.state.result.map(function (ele,index,array) {
                                    return <tr key={index}>
                                        <td>{ele.id}</td>
                                        <td>{ele.accountId}</td>
                                        <td>{ele.scale}</td>
                                        <td>{ele.keywords}</td>
                                        <td>{ele.platform}</td>
                                        <td><a className="btn btn-primary" href={"#/create_agent/"+ele.id}>Edit</a></td>
                                    </tr>
                                })
                            }
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        )
    }
});
export default  AgentList;
