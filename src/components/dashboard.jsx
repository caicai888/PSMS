import React from "react";
import {ajax} from "../lib/ajax";

var Dashboard = React.createClass({
    getInitialState() {
        return {
            result:[],
            adwordsResult:[]
        };
    },
    componentDidMount(){
        let _this = this;
        ajax("get","/api/dashboard").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    result: [data.result]
                })
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        });
        ajax("get","/api/adwords/dashboard").then(function (data) {
            var data = JSON.parse(data);
            if(data.code=="200"){
                _this.setState({
                    adwordsResult: [data.result]
                })
            }else {
                $(".ajax_error").html(data.message);
                $(".modal").modal("toggle");
            }
        });
    },
    render:function () {
        console.log(this.state.result)
        return (
            <div>
                <div className="row">
                    <div className="col-md-12" style={{padding:"15px"}}>
                        Facebook Dashboard
                    </div>
                </div>
                <div className="row dashboard_data">
                    {
                        this.state.result.map(function (ele,index,array) {
                            return <div className="col-md-12" key={index}>
                                <div className="box_20">
                                    <p>Revenue($)</p>
                                    <p>{ele.revenue}</p>
                                </div>
                                <div className="box_20">
                                    <p>Profit($)</p>
                                    <p>{ele.profit}</p>
                                </div>
                                <div className="box_20">
                                    <p>Cost($)</p>
                                    <p>{ele.spend}</p>
                                </div>
                                <div className="box_20">
                                    <p>Impressions</p>
                                    <p>{ele.impressions}</p>
                                </div>
                                <div className="box_20">
                                    <p>Clicks</p>
                                    <p>{ele.clicks}</p>
                                </div>
                                <div className="box_20">
                                    <p>Conversions</p>
                                    <p>{ele.conversions}</p>
                                </div>
                                <div className="box_20">
                                    <p>CTR(%)</p>
                                    <p>{ele.ctr}</p>
                                </div>
                                <div className="box_20">
                                    <p>CVR(%)</p>
                                    <p>{ele.cvr}</p>
                                </div>
                                <div className="box_20">
                                    <p>CPC</p>
                                    <p>{ele.cpc}</p>
                                </div>
                                <div className="box_20">
                                    <p>CPI</p>
                                    <p>{ele.cpi}</p>
                                </div>
                            </div>
                        })
                    }
                </div>
                <div className="row">
                    <div className="col-md-12" style={{padding:"15px"}}>
                        Adwords Dashboard
                    </div>
                </div>
                <div className="row dashboard_data">
                    {
                        this.state.adwordsResult.map(function (ele,index,array) {
                            return <div className="col-md-12" key={index}>
                                <div className="box_20">
                                    <p>Revenue($)</p>
                                    <p>{ele.revenue}</p>
                                </div>
                                <div className="box_20">
                                    <p>Profit($)</p>
                                    <p>{ele.profit}</p>
                                </div>
                                <div className="box_20">
                                    <p>Cost($)</p>
                                    <p>{ele.spend}</p>
                                </div>
                                <div className="box_20">
                                    <p>Impressions</p>
                                    <p>{ele.impressions}</p>
                                </div>
                                <div className="box_20">
                                    <p>Clicks</p>
                                    <p>{ele.clicks}</p>
                                </div>
                                <div className="box_20">
                                    <p>Conversions</p>
                                    <p>{ele.conversions}</p>
                                </div>
                                <div className="box_20">
                                    <p>CTR(%)</p>
                                    <p>{ele.ctr}</p>
                                </div>
                                <div className="box_20">
                                    <p>CVR(%)</p>
                                    <p>{ele.cvr}</p>
                                </div>
                                <div className="box_20">
                                    <p>CPC</p>
                                    <p>{ele.cpc}</p>
                                </div>
                                <div className="box_20">
                                    <p>CPI</p>
                                    <p>{ele.cpi}</p>
                                </div>
                            </div>
                        })
                    }
                </div>
            </div>

        )
    }
});
export default  Dashboard;
