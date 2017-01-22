import React from "react";
import {ajax} from "../lib/ajax";
require("../js/bootstrap.min");
var Header = React.createClass({
    getInitialState() {
        return {
            permissions:String(sessionStorage.getItem("permissions"))
        }
    },
    loginOut(){
        ajax("get","/api/user/logout").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                $(".userEmail").html("");
                $(".userId").html("");
                location.hash="/login";
                $(".isShow").hide();
            }else {
                $(".ajax_error").html(data.message);
                $("#modal").modal("toggle");
            }
        });
    },
    componentDidMount(){
        if(location.hash!=""&&location.hash!="#/login"){
            ajax("post","/api/user/verify_session").then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    $(".userEmail").html(data.results.email);
                    $(".userId").html(data.results.id);
                    $(".isShow").show();
                }else {
                    $(".ajax_error").html(data.message);
                    $("#modal").modal("toggle");
                    $("#modal").on("hidden.bs.modal",function () {
                        location.hash="/login";
                        $(".isShow").hide();
                    })
                }
            });
        }
        $("#nav_nav>ul.ul_active>li").on("click",function () {
            $(this).addClass("active").siblings().removeClass("active");
        });
        var hash = location.hash;
        $("#nav_nav>ul.ul_active>li").each(function () {
            if(hash.indexOf($(this).attr("data-hash"))>-1){
                $("#nav_nav>ul>li").removeClass("active");
                $(this).addClass("active");
                return;
            }
        });

    },
    render:function () {
        let _this = this;
        console.log(_this.state.permissions)
        return <nav className="navbar navbar-default" role="navigation">
            <div className="container-fluid">
                <div className="navbar-header">
                    <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#nav_nav">
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"> </span>
                        <span className="icon-bar"> </span>
                        <span className="icon-bar"> </span>
                    </button>
                    <a className="navbar-brand" href="#/welcome">PSMS</a>
                </div>

                <div className="collapse nav_right navbar-collapse" id="nav_nav">
                    <ul className="nav ul_active navbar-nav isShow">
                        <li data-hash="dashboard" className={_this.state.permissions.includes("dashboard_query")?"":"none"}><a href="#/dashboard">Dashboard</a></li>
                        <li data-hash="manager" className={_this.state.permissions.includes("manager_query")?"dropdown":"none"}>
                            <a href="javascript:void(0)" className="dropdown-toggle" data-toggle="dropdown">Manager <span className="caret"></span></a>
                            <ul className="dropdown-menu" role="menu">
                                <li className={_this.state.permissions.includes("manager_create")?"":"none"}><a href="#/create_manager">Create Manager</a></li>
                                <li className={_this.state.permissions.includes("manager_create")?"divider":"none"}> </li>
                                <li className={_this.state.permissions.includes("manager_query")?"":"none"}><a href="#/manager_list">Manager List</a></li>
                                <li className={_this.state.permissions.includes("manager_query")?"divider":"none"}> </li>
                                <li className={_this.state.permissions.includes("manager_create")?"":"none"}><a href="#/create_group_manager">Create Group</a></li>
                                <li className={_this.state.permissions.includes("manager_create")?"divider":"none"}> </li>
                                <li className={_this.state.permissions.includes("manager_query")?"":"none"}><a href="#/group_list_manager">Group List</a></li>
                            </ul>
                        </li>
                        <li data-hash="customer" className={_this.state.permissions.includes("advertiser_query")?"dropdown":"none"}>
                            <a href="javascript:void(0)" className="dropdown-toggle" data-toggle="dropdown">Advertiser <span className="caret"></span></a>
                            <ul className="dropdown-menu" role="menu">
                                <li className={_this.state.permissions.includes("advertiser_create")?"":"none"}><a href="#/create_customer">Create Advertiser</a></li>
                                <li className={_this.state.permissions.includes("advertiser_create")?"divider":"none"}> </li>
                                <li className={_this.state.permissions.includes("advertiser_query")?"":"none"}><a href="#/customer_list">Advertiser List</a></li>
                            </ul>
                        </li>
                        <li data-hash="offer"  className={_this.state.permissions.includes("offer_query")?"dropdown":"none"}>
                            <a href="javascript:void(0)" className="dropdown-toggle" data-toggle="dropdown">Offer <span className="caret"></span></a>
                            <ul className="dropdown-menu" role="menu">
                                <li className={_this.state.permissions.includes("offer_create")?"":"none"}><a href="#/create_offer">Create Offer</a></li>
                                <li className={_this.state.permissions.includes("offer_create")?"divider":"none"}> </li>
                                <li className={_this.state.permissions.includes("offer_query")?"":"none"}><a href="#/offer_list">Offer List</a></li>
                            </ul>
                        </li>
                        {/*<li><a href="#/about">About</a></li>
                        <li><a href="#/list">List</a></li>*/}
                    </ul>
                    <ul className="nav navbar-nav navbar-right isShow">
                        <li><a onClick={this.loginOut} href="javascript:void(0)">Email：<span className="userEmail"></span>&nbsp;|&nbsp;UserId：<span className="userId"></span>&nbsp;|&nbsp;已登录！</a> </li>
                    </ul>
                </div>
            </div>
        </nav>

    }
});
module.exports = Header;
