/**
 * Created by sa on 16-12-25.
 */
require("../js/AjaxFileUpload");
var uploadFile = function (url,method,id) {
    var promise = new Promise(function (resolve,reject) {
        $.ajaxFileUpload({
            url:url, //path problem
            type: method,
            secureuri: false, //一般设置为false
            fileElementId: id, // 上传文件的id、name属性名
            dataType: 'application/json', //返回值类型，一般设置为json、application/json
            //elementIds: elementIds, //传递参数到服务器
            success: function(data, status) {
                resolve(data);//请求成功
            },
            error: function(data, status, e) {
                reject(data)
            }
        });
    });
    return promise;
};
module.exports = {
    uploadFile:uploadFile
}
