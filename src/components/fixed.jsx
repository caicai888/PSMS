import React from "react";

var Fixed = React.createClass({
    render:function () {
        return (
            <div>
                <div className="mask ">
                    <div className="mask_mask box-center">
                        <img src="./src/img/loading-2.gif"/>
                    </div>
                </div>
                <div className="modal fade" style={{marginTop:"20px"}}>
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <button type="button" className="close" data-dismiss="modal">
                                    <span >&times;</span>
                                    <span className="sr-only">Close</span>
                                </button>
                                <h4 className="modal-title">Tip</h4>
                            </div>
                            <div className="modal-body">
                                <p className="ajax_error"> </p>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});
export default  Fixed;
