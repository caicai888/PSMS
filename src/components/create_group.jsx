import React from "react";
import {ajax} from "../lib/ajax";
import {valid,setForm,getForm} from "../lib/form";

var CreateGroup = React.createClass({
    getInitialState() {
        return {
            permissions:{},
            permission_ids:""
        };
    },
    submit(){
        let newArr =[];
        for(let ele of $("#table_html input:checked")){
            newArr.push($(ele).val());
        }
        if(valid("#create_customer","data-required")){
            var data = setForm("#create_customer","data-key");
            data.permission_ids=newArr.join(",");
            var url = this.props.params.id?"/api/role/edit/"+this.props.params.id:"/api/role/create";
            ajax("post",url,JSON.stringify(data)).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    location.hash = "group_list_manager";
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                }
            });
        }else {
            $(".has-error input:first").focus();
        }
    },
    componentDidMount(){
        let _this = this;
        if(_this.props.params.id){
            sessionStorage.setItem("count","1");
            ajax("post","/api/role/do_edit/"+_this.props.params.id).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.setState({
                        permission_ids:data.results
                    });
                    getForm("#create_customer",data.results);
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                }
            });
        }
        ajax("get","/api/permissions").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    permissions:data.results
                })
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        });
    },
    render:function () {
        let _this = this;
        let html_tr="";
        let permissions = this.state.permissions;
        for (let ele in permissions){
            let html_td="";
            for(let key in permissions[ele]){
                html_td += `<td>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" ${this.state.permission_ids&&this.state.permission_ids.permission_ids.length>0&&_this.state.permission_ids.permission_ids.includes(permissions[ele][key])?"checked":""} value="${permissions[ele][key]}" /> ${key}
                                    </label>
                                </div>
                            </td>`
            }
            html_tr +=`<tr>
                        <td>${ele}</td>
                        ${html_td}
                    </tr>`;
        }
        $("#table_html").html(html_tr)
        return (
            <div className="col-sm-8 col-sm-offset-2 animated slideInDown create_customer">
                <form id="create_customer" className="form-horizontal" role="form" noValidate="noValidate">
                    <div className="form-group">
                        <label htmlFor="company_name" className="col-sm-2 control-label text-right">* 名称</label>
                        <div className="col-sm-10">
                            <input type="text"  data-required="true" data-key="name"  name="name" className="form-control"   placeholder="Group Name" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_address" className="col-sm-2 control-label text-right">权限</label>
                        <div className="col-sm-10 ">
                            <div className="table-responsive">
                                <table className="table group_table table-bordered">
                                   <tbody id="table_html">

                                   </tbody>
                                </table>
                            </div>

                        </div>
                    </div>
                    <div className="form-group">
                        <div className="col-sm-offset-2 col-sm-10">
                            <button onClick={this.submit} type="button" className="btn btn-primary">Create/Update</button>
                            <a href={this.props.params.id?"javascript:history.go(-1)":"javascript:void(0)"} type="button" className="btn btn-warning" style={{marginLeft:"20px"}}>Cancel</a>
                        </div>
                    </div>
                </form>
            </div>
        )
    }
});
export default  CreateGroup;
