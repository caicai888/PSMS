import React from "react";
import {Select,AjaxSelect} from "./select";

var List = React.createClass({
    render:function () {
        return <div>
            <h5>list</h5>
            <div className="col-lg-6">
                <Select />
            </div>
            <div className="col-lg-6">
                <AjaxSelect />
            </div>
        </div>
    }
});
export default  List;