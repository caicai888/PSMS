import React from "react";
import {ajax} from "../lib/ajax";
import {valid,setForm,getForm} from "../lib/form";

var Login = React.createClass({
    submit(){
        if(valid("#login_form","data-required")){
            var data = setForm("#login_form","data-key");
            ajax("post","/api/user/login",JSON.stringify(data)).then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    location.hash = "welcome";
                    $(".userEmail").html(data.results.email);
                    $(".userId").html(data.results.id);
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("show");
                }
            });
        }else {
            $(".has-error input:first").focus();
        }
    },
    componentWillMount(){
      if($(".userId").html()!=""){
          location.hash="welcome"
      }
    },
    componentDidMount(){
        var _this = this;
        $(document).keydown(function (e) {
            var event = e || event;
            if(event.keyCode==13){
                _this.submit();
            }
        });
    },
    render:function () {
        return <div className="row box-center" id="login">
                    <div className="col-md-4 col-lg-3">
                        <div className="login animated slideInDown">
                            <div className="login_title">Sign in</div>
                            <form role="form" id="login_form" noValidate="noValidate" autoComplete="on">
                                <div className="form-group">
                                    <input type="email" name="email" data-key="email" data-required="true"  className="form-control" placeholder="Email" />
                                </div>
                                <div className="form-group">
                                    <input type="password" data-key="passwd" data-required="true" name="password" className="form-control" placeholder="Password" />
                                </div>
                                {/*<div className="form-group padding_clear">
                                    <div className="col-xs-8">
                                        <input type="text"  placeholder="Captcha" className="form-control"/>
                                    </div>
                                    <div className="col-xs-4">
                                        <img />
                                    </div>
                                </div>*/}
                                <div className="form-group loginIn">
                                    <button onClick={this.submit} style={{width:"100%"}} id="submit_login" type="button" className="btn btn-primary">Go</button>
                                </div>
                            </form>
                        </div>

                    </div>
                </div>
    }
});
export default  Login;
