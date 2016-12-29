import React from "react";
import {DateSingle,Daterange} from "./daterange"

var About = React.createClass({
    render() {
        return (
            <div>
                <h5>about</h5>
                <Daterange start="1" end="0" id="date_range" />
                <br/>
                <DateSingle id="start_date"/>
            </div>
        )
    }
});
export default  About;