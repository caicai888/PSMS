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
            $(".reportRange").val(start.format("YYYY-MM-DD")+":"+end.format("YYYY-MM-DD"));
            $(".report_weidu li:last").click();
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
        var timeKey = _this.props.class;
        var date = function (id,time) {
            /*var id = (id=="start_date"?".end_date":".start_date");*/
            var id = "." + id;
            $(id).daterangepicker({
                singleDatePicker: true,
                locale: {
                    format: "YYYY-MM-DD"
                },
                autoUpdateInput:false,
                minDate:id ==".end_date"?time:(id.includes("1")&&id ==".end_date1"?time:(id.includes("2")&&id ==".end_date2"?time:false)), //着急忙慌的,先写死了
                maxDate:id ==".start_date"?time:(id.includes("1")&&id ==".start_date1"?time:(id.includes("2")&&id ==".start_date2"?time:false)),
            },function(end) {
                $(id).val(end.format("YYYY-MM-DD"));
                var timeKey ="";
                if(!id.includes("1")&&!id.includes("2")&&id==".end_date"){
                    timeKey = "start_date"
                }
                if(!id.includes("1")&&!id.includes("2")&&id==".start_date"){
                    timeKey ="end_date";
                }
                if(id.includes("1")&&id==".start_date1"){
                    timeKey ="end_date1";
                }
                if(id.includes("1")&&id==".end_date1"){
                    timeKey ="start_date1";
                }
                if(id.includes("2")&&id==".start_date2"){
                    timeKey ="end_date2";
                }
                if(id.includes("2")&&id==".end_date2"){
                    timeKey ="start_date2";
                }
                date(timeKey,end.format("YYYY-MM-DD"))
            })
        }
        /*$('#'+this.props.id).daterangepicker({
            singleDatePicker: true,
            locale: {
                format: "YYYY-MM-DD"
            },
            autoUpdateInput:false
        },function(start) {
           $('#'+_this.props.id).val(start.format("YYYY-MM-DD"));
           date(_this.props.id,start.format("YYYY-MM-DD"))
        });*/
        date(timeKey,false);
        $('.'+timeKey).val(moment().subtract(_this.props.start, 'days').format("YYYY-MM-DD"));
    },
    render() {
        return (
            <input className={"form-control "+this.props.class} data-maxDate={this.props.maxDate} data-minDate={this.props.minDate} data-required={this.props.require} data-key={this.props.keyword} type="text"  readOnly="readOnly"/>
        )
    }
});

module.exports = {
    DateSingle:DateSingle,
    Daterange:Daterange
};
