import React from "react";
import {ajax} from "../lib/ajax";
import {valid,setForm,getForm} from "../lib/form";

var CreateAgent = React.createClass({
    submit(){
        if(valid("#create_customer","data-required")){
            var data = setForm("#create_customer","data-key");
            var url = "/api/rebate/create";
            ajax("post",url,JSON.stringify(data)).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    location.hash = "agent_list";
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
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
            ajax("post","/api/rebate/show/"+_this.props.params.id).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    getForm("#create_customer",data);
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                }
            });
        }


    },
    render:function () {
        return (
            <div className="col-sm-8 col-sm-offset-2 animated slideInDown create_customer" style={{marginTop:0}}>
                <form id="create_customer" className="form-horizontal" role="form" noValidate="noValidate">
                    <div className="form-group">
                        <label htmlFor="company_name" className="col-sm-2 control-label text-right">* 代理商名字</label>
                        <div className="col-sm-10">
                            <input type="text" disabled={this.props.params.id?true:false} data-required="true" data-key="accountId"  name="name" className="form-control"   placeholder="accountId" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_name" className="col-sm-2 control-label text-right">* 返点比例(%)</label>
                        <div className="col-sm-10">
                            <input type="email"  data-required="true" data-key="scale"  name="name" className="form-control"   placeholder="" />
                        </div>
                    </div>
                    <div className="form-group">
                        <div className="col-sm-offset-2 col-sm-10">
                            <input type="hidden" data-key="rebateId" value={this.props.params.id}/>
                            <button  className="btn btn-primary" onClick={this.submit} type="button">Create/Update</button>
                            <a href="javascript:history.go(-1)" type="button" className="btn btn-warning" style={{marginLeft:"20px"}}>Cancel</a>
                        </div>
                    </div>
                </form>
            </div>
        )
    }
});
export default  CreateAgent;
