import React from "react";
import moment from "moment";
require("daterangepicker");
require("daterangepicker/daterangepicker-bs3.css");


var Daterange = React.createClass({
    componentDidMount(){
        var _this=this;
        var start = moment().subtract(_this.props.start, 'days');
        var end = moment().subtract(_this.props.end, 'days');
        function cb(start, end) {
            $('#'+_this.props.id+' span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        }
        $('#'+_this.props.id).daterangepicker({
            startDate: start,
            endDate: end,
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
        }, cb);
        cb(start, end);
    },
    render() {
        return (
            <div id={this.props.id} className="pull-left" style={{background:"#fff",cursor:"pointer",padding:" 5px 10px", border:" 1px solid #ccc"}}>
                <i className="glyphicon glyphicon-calendar fa fa-calendar"> </i>&nbsp;<span> </span> <b className="caret"> </b>
            </div>
        )
    }
});

var DateSingle = React.createClass({
    componentDidMount(){
        var _this= this;
        $('#'+this.props.id).daterangepicker({
            singleDatePicker: true,
            locale: {
                format: "YYYY-MM-DD"
            },
            autoUpdateInput:false
        },function(start) {
           $('#'+_this.props.id).val(start.format("YYYY-MM-DD"))
        });
    },
    render() {
        return (
            <input id={this.props.id} data-key={this.props.keyword} type="text" className="form-control" readOnly="readOnly"/>
        )
    }
});

module.exports = {
    DateSingle:DateSingle,
    Daterange:Daterange
};
