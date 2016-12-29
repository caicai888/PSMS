import React from "react";
require("select2");
require("select2/dist/css/select2");

var Select = React.createClass({
    componentWillUpdate(){
        $("."+this.props.className).select2({
            data: this.props.data,
            multiple: this.props.multiple=="false"?false:true,
            placeholder:this.props.placeholder
        });
    },
    render(){
        return (
           <select  data-key={this.props.keyword}  className={this.props.className+" form-control"}> </select>
        )
    }
});

var AjaxSelect = React.createClass({
    componentDidMount(){
        $("."+this.props.className).select2({
            ajax: {
                method:"post",
                url: this.props.url, //"https://api.github.com/search/repositories",
                dataType: 'json',
                delay: 500,
                data: function (params) {
                    return JSON.stringify({
                        name: params.term
                    });
                },
                processResults: function (data, params) {
                    //var data = [{ id: 10, text: 'enhancement' }, { id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }];
                    return {
                        results: data.result
                    };
                },
                cache: true
            },
            minimumInputLength: 1,
            multiple: this.props.multiple=="false"?false:true,
            placeholder:this.props.placeholder
        });
    },
    render(){
        return (
            <select  data-key={this.props.keyword}  className={this.props.className+" form-control"} > </select>
        )
    }
});

module.exports ={
    Select:Select,
    AjaxSelect:AjaxSelect
}
