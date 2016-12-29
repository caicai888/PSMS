import React from "react";
import OfferDetailDetail from "./offer_detail_detail";

var OfferDetail = React.createClass({
    componentDidMount(){

    },
    render:function () {
        return (
            <div>
                <ul id="myTab" className="nav nav-tabs">
                    <li className="active"><a href="#offer_detail" data-toggle="tab">Offer Detail</a>
                    </li>
                    <li><a href="#bind_list" data-toggle="tab">Bind List</a></li>
                    <li><a href="#report"  data-toggle="tab">Report</a>
                    </li>
                </ul>
                <div id="myTabContent" className="tab-content" style={{marginTop:"10px"}}>
                    <div className="tab-pane fade in active" id="offer_detail">
                        <div className="row" style={{marginBottom:"10px"}}>
                            <div className="col-sm-10 ">
                                <div className="col-sm-3 text-right">ID</div>
                                <div className="col-sm-9">
                                    1000
                                </div>
                            </div>
                        </div>
                        <OfferDetailDetail id={this.props.params.id} />
                    </div>
                    <div className="tab-pane fade" id="bind_list">
                        <div className="row">
                            <div className="col-sm-10">
                                <div className="col-sm-3 text-right">
                                    Facebook
                                </div>
                                <div className="col-sm-9">
                                    <textarea className="form-control">

                                    </textarea>
                                </div>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-sm-10">
                                <div className="col-sm-3 text-right">
                                    Adwords
                                </div>
                                <div className="col-sm-9">
                                    <textarea className="form-control">

                                    </textarea>
                                </div>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-sm-10">
                                <div className="col-sm-3 text-right"></div>
                                <div className="col-sm-9">
                                    <a className="btn btn-primary" style={{marginRight:"20px"}}>Save</a>
                                    <a className="btn btn-warning">Cancel</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="tab-pane fade" id="report">
                        <div className="row">
                            <div className="col-md-3">
                                <div id="reportRange">
                                    <span>December 13, 2016 - December 19, 2016</span>
                                </div>
                            </div>
                            <div className="col-md-4">
                                <ul className="box-center report_weidu">
                                    <li data-key="" className="active">Day</li>
                                    <li data-key="country">Country</li>
                                    <li data-key="slot">Slot</li>
                                    <li data-key="campaign">Campaign</li>
                                </ul>
                            </div>
                            <div className="col-md-2 pull-right allSlot">
                                <select className="form-control">
                                    <option value="all_slot">All Slot</option>
                                </select>
                            </div>
                        </div>
                        <div className="row dashboard_data">
                            <div className="col-md-12">
                                <div className="box_20">
                                    <p>Revenue($)</p>
                                    <p>739.42</p>
                                </div>
                                <div className="box_20">
                                    <p>Profit($)</p>
                                    <p>739.42</p>
                                </div>
                                <div className="box_20">
                                    <p>Cost($)</p>
                                    <p>739.42</p>
                                </div>
                                <div className="box_20">
                                    <p>Impressions($)</p>
                                    <p>739.42</p>
                                </div>
                                <div className="box_20">
                                    <p>Clicks($)</p>
                                    <p>739.42</p>
                                </div>
                                <div className="box_20">
                                    <p>Conversions($)</p>
                                    <p>739.42</p>
                                </div>
                                <div className="box_20">
                                    <p>CTR($)</p>
                                    <p>739.42</p>
                                </div>
                                <div className="box_20">
                                    <p>CVR($)</p>
                                    <p>739.42</p>
                                </div>
                                <div className="box_20">
                                    <p>CPC($)</p>
                                    <p>739.42</p>
                                </div>
                                <div className="box_20">
                                    <p>CPA($)</p>
                                    <p>739.42</p>
                                </div>
                            </div>
                        </div>
                        <div className="row report_report">
                            <div className="col-md-12">
                                <div className="report_zhexian">
                                    <ul>
                                        <li className="active">Revenue</li>
                                        <li>Profit</li>
                                        <li>Cost</li>
                                        <li>Impressions</li>
                                        <li>Clicks</li>
                                        <li>Conversions</li>
                                        <li>CTR</li>
                                        <li>CVR</li>
                                        <li>CPC</li>
                                        <li>CPA</li>
                                        <div className="clear"></div>
                                    </ul>
                                </div>
                            </div>
                            <div className="col-md-12 report_overflow">
                                <div id="report_zhexian">

                                </div>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-xs-12 date_detail">
                                <div className="col-xs-6">Details</div>
                                <div className="col-xs-6 text-right">
                                    <button className="btn btn-primary">Export</button>
                                </div>
                            </div>
                        </div>
                        <div className="table-responsive" style={{marginTop:"10px"}}>
                            <table className="table table-bordered">
                                <thead>
                                <tr>
                                    <th>Revenue</th>
                                    <th>Profit</th>
                                    <th>Cost</th>
                                    <th>Impressions</th>
                                    <th>Clicks</th>
                                    <th>Conversions</th>
                                    <th>CTR</th>
                                    <th>CVR</th>
                                    <th>CPC</th>
                                    <th>CPA</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <td>Revenue</td>
                                    <td>Profit</td>
                                    <td>Cost</td>
                                    <td>Impressions</td>
                                    <td>Clicks</td>
                                    <td>Conversions</td>
                                    <td>CTR</td>
                                    <td>CVR</td>
                                    <td>CPC</td>
                                    <td>CPA</td>
                                </tr>
                                </tbody>
                            </table>
                        </div>

                    </div>
                </div>
            </div>
        )
    }
});
module.exports = OfferDetail;
