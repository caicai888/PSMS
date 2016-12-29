/**
 * Created by sa on 16-12-20.
 */
let location_hostname = location.hostname;
let url="";
if(location_hostname.includes("localhost")>-1){
    url = "/api";
}else{
    url = "";
}
const config = {
    url:url
};
module.exports = {
    config:config
};