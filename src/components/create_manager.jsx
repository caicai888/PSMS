import React from "react";
import {ajax} from "../lib/ajax";
import {valid,setForm,getForm} from "../lib/form";

var CreateManager = React.createClass({
    getInitialState() {
        return {
            permissions:{},
            permission_ids:"",
            role:[],
            count:1,
            role_ids:""
        };
    },
    submit(){
        let newArr =[];
        for(let ele of $("#table_html input:checked")){
            newArr.push($(ele).val());
        }

        let roleId =[];
        for(let ele of $("#role_cb input:checked")){
            roleId.push($(ele).val());
        }

        if(valid("#create_customer","data-required")){
            var data = setForm("#create_customer","data-key");
            data.permission_ids=newArr.join(",");
            data.role_ids=roleId.join(",");
            if(data.role_ids.length==0){
                $(".ajax_error").html("必须选择一个组");
                $(".modal").modal("toggle");
                return;
            }
            var url = this.props.params.id?"/api/user/edit/"+this.props.params.id:"/api/user/create";
            ajax("post",url,JSON.stringify(data)).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    location.hash = "manager_list";
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
            ajax("post","/api/user/do_edit/"+_this.props.params.id).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.setState({
                        permission_ids:data.results.permission_ids,
                        role_ids:data.results.role_ids
                    });
                    getForm("#create_customer",data.results);
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                }
            });
        }
        ajax("get","/api/roles").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    role:data.results
                });
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        });
        ajax("get","/api/permissions").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    permissions:data.results
                });
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        });



    },
    render:function () {
        let count=1;
        let _this = this;
        let html_tr="";
        let permissions = this.state.permissions;
        for (let ele in permissions){
            let html_td="";
            for(let key in permissions[ele]){
                html_td += `<td>
                                <div className="checkbox">
                                    <label>
                                        <input type="checkbox" ${this.state.permission_ids&&this.state.permission_ids.toString().length>0&&_this.state.permission_ids.toString().includes(permissions[ele][key])?"checked":""} value="${permissions[ele][key]}" /> ${key}
                                    </label>
                                </div>
                            </td>`
            }
            html_tr +=`<tr>
                        <td>${ele}</td>
                        ${html_td}
                    </tr>`;
        }
        $("#table_html").html(html_tr);

        if(_this.state.count==1){
            console.log(this.state.role_ids)
            let role_cb = "<tr>";
            this.state.role.map(function (ele,index,array) {
                role_cb += `<td>
                            <div className="checkbox">
                                <label>
                                    <input  ${_this.state.role_ids.length>0&&_this.state.role_ids.includes(ele.id)?"checked":""} className="role_cb" type="checkbox"  value=${ele.id}  /> ${ele.name}
                                </label>
                            </div>
                        </td>${index!=0&&((index+1)%4==0)?'</tr>':''}`
            })
            $("#role_cb").html(role_cb);
        }
        $("#role_cb input").unbind("click").bind("click",function () {
            if(!$(this).prop("checked")){
                return;
            }
            ajax("get","/api/role_permissions/"+$(this).val()).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    _this.setState({
                        permission_ids:data.results.permission_ids,
                        count:++_this.state.count
                    });
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                }
            });
        })

        return (
            <div className="col-sm-8 col-sm-offset-2 animated slideInDown create_customer" style={{marginTop:0}}>
                <form id="create_customer" className="form-horizontal" role="form" noValidate="noValidate">
                    <div className="form-group">
                        <label htmlFor="company_name" className="col-sm-2 control-label text-right">* 名称</label>
                        <div className="col-sm-10">
                            <input type="text"  data-required="true" data-key="name"  name="name" className="form-control"   placeholder="Name" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_name" className="col-sm-2 control-label text-right">* Email</label>
                        <div className="col-sm-10">
                            <input type="email"  data-required="true" data-key="email"  name="name" className="form-control"   placeholder="Email" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_name" className="col-sm-2 control-label text-right">* 密码</label>
                        <div className="col-sm-10">
                            <input type="password"  data-required="true" data-key="passwd"  name="name" className="form-control"   placeholder="Password" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_name" className="col-sm-2 control-label text-right">* Phone</label>
                        <div className="col-sm-10">
                            <input type="number"  data-key="phone"  name="name" className="form-control"   placeholder="Phone" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_address" className="col-sm-2 control-label text-right">组</label>
                        <div className="col-sm-10 ">
                            <div className="table-responsive">
                                <table className="table group_table table-bordered">
                                    <tbody id="role_cb">

                                    </tbody>
                                </table>
                            </div>

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
export default  CreateManager;