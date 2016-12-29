import React from "react";
import {ajax} from "../lib/ajax";
import {valid,setForm,getForm} from "../lib/form";

var GroupList = React.createClass({
    getInitialState() {
        return {
            result:[]
        };
    },
    componentDidMount(){
        let _this = this;
        ajax("get","/api/roles").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    result:data.results
                })
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        });
    },
    render:function () {
        return (
            <div className="col-sm-12 animated slideInDown">
                <div className="table-responsive">
                    <table className="table table-bordered">
                        <thead>
                            <tr>
                                <th>Role_id</th>
                                <th>Role_name</th>
                                <th>最后修改</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                this.state.result.map(function (ele,index,array) {
                                    return <tr key={index}>
                                                <td>{ele.id}</td>
                                                <td>{ele.name}</td>
                                                <td>{ele.last_datetime}</td>
                                                <td><a href={"#/create_group_manager/"+ele.id} className="btn btn-primary">Edit</a></td>
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
export default  GroupList;
