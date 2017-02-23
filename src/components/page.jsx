//http://jqpaginator.keenwon.com/#a3
import React from "react";
require("jqPaginator/src/js/jqPaginator");

var Page = React.createClass({
    componentDidUpdate(){
        var _this = this;
        $("#"+this.props.id).jqPaginator({
            totalPages: this.props.totalPages,
            visiblePages: 10,//总共分多少页
            currentPage: this.props.page,
            onPageChange: function (num, type) {
                if(type!="init"){
                    _this.props.onClick(num,_this.props.limit);
                }
            }
        });
    },
    render(){
        return (
            <div id="page">
                <ul className="pagination" id={this.props.id}>

                </ul>
            </div>
        )
    }
});

module.exports ={
    Page:Page
}
