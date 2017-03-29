import React from "react";
import {ajax} from "../lib/ajax";
import {valid,setForm,getForm} from "../lib/form";
import {Select,AjaxSelect} from "./select";

var CreateAgent = React.createClass({
    getInitialState() {
        return {
            tfpt:[{
                id:"Facebook",
                text:"Facebook"
            },{
                id:"Adwords",
                text:"Adwords"
            },{
                id:"Apple",
                text:"Apple"
            }]
        }
    },
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
                    _this.setState({
                        tfpt:data.platform
                    });
                    setTimeout(function () {
                        $(".tfpt").val(data.platform.toString().split(",")).trigger("change");
                    });

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
                        <label htmlFor="accountName" className="col-sm-2 control-label text-right">* 代理商名字</label>
                        <div className="col-sm-10">
                            <input type="text" id="accountName" disabled={this.props.params.id?true:false} data-required="true" data-key="accountName"  name="name" className="form-control"   placeholder="accountName" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="scale" className="col-sm-2 control-label text-right">* 返点比例(%)</label>
                        <div className="col-sm-10">
                            <input type="email"  data-required="true" data-key="scale" id="scale"   name="name" className="form-control"   placeholder="scale" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="col-sm-2 control-label text-right">平台</label>
                        <div className="col-sm-10">
                            <Select keyword="platform" value="" className="platform" placeholder="platform"　multiple="false" data={this.state.tfpt}/>
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_name" className="col-sm-2 control-label text-right">公司名称</label>
                        <div className="col-sm-10">
                            <input type="text"  data-key="companyName"  name="name" className="form-control" id="company_name"  placeholder="Name" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_address" className="col-sm-2 control-label text-right">公司地址</label>
                        <div className="col-sm-10">
                            <input  type="text"　data-key="company_address" name="address" className="form-control" id="company_address" placeholder="Address" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="bank_account" className="col-sm-2 control-label text-right">银行账户</label>
                        <div className="col-sm-10">
                            <input  type="text" 　data-key="bank_account" name="bank_account" className="form-control" id="bank_account" placeholder="Bank" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="concordat_code" className="col-sm-2 control-label text-right">合同编号</label>
                        <div className="col-sm-10">
                            <input  type="text"　data-key="concordat_code" name="concordat_code" className="form-control" id="concordat_code" placeholder="Num" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="keywords" className="col-sm-2 control-label text-right">关键词</label>
                        <div className="col-sm-10">
                            <input  type="text"　data-key="keywords" name="keywords" className="form-control" id="keywords" placeholder="keywords" />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_remark" className="col-sm-2 control-label text-right">备注</label>
                        <div className="col-sm-10">
                            <textarea className="form-control" data-key="remark" name="remark" id="company_remark">

                            </textarea>
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
