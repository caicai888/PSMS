import React from "react";

var Welcome = React.createClass({
    /*componentDidMount(){
        if(!sessionStorage.getItem("into")){
            sessionStorage.setItem("into",1);
            location.reload();
        }
    },*/
    render:function () {
        return <div className="welcome box-center">
                    欢迎来到PSMS财务系统
               </div>
    }
});
export default  Welcome;