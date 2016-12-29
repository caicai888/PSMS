/**
 * Created by sa on 16-12-17.
 */
var valid = function (form,custom_property) {
    var flag = true;
    var count=0;
    var custom_property = Array.from($(form).find("["+custom_property+"]"));
    for (var i=0;i<custom_property.length;i++){
        var radio_key =false;
        if($(custom_property[i]).attr("type")=="radio"){
            $(form +" input[type=radio]").each(function () {
                if($(this).prop("checked")&&$(this).val()){
                    radio_key = true;
                    return;
                }
            })
        }
        if(($(custom_property[i]).val()=="" && $(custom_property[i]).attr("type")!="radio") || (!radio_key&&$(custom_property[i]).attr("type")=="radio")){
            count++;
            $(custom_property[i]).parent().addClass("has-error");
            if($(custom_property[i]).next("p").html()){
                $(custom_property[i]).next("p").show();
            }
            (function (i) {
                setTimeout(function () {
                    $(custom_property[i]).parent().removeClass("has-error");
                    if($(custom_property[i]).next("p").html()){
                        $(custom_property[i]).next("p").hide();
                    }
                },2000)
            })(i);
        }
    }
    if(count!=0){
        flag=false;
    }
    console.log(count,flag)
    return flag;
};
var setForm = function (form,custom_prop) {
    var obj={};
    var custom_prop_arr = $(form).find("["+custom_prop+"]");
    for (var i=0;i<custom_prop_arr.length;i++){
        var key =  $(custom_prop_arr[i]).attr(custom_prop);
        //判断key 有没有点(.)
        var result="";
        if(key.indexOf(".")>-1){
            var key_arr = key.split(".");
            //var str ="";
            for (var j=0;j<key_arr.length;j++){
                result += '{"'+key_arr[j]+'":';
                //str+="}"
                if(j==key_arr.length-1){
                    result=result+'"'+ ($(custom_prop_arr[i]).val()) +'"'+"}".repeat(key_arr.length);
                }
            }
            $.extend(true,obj,JSON.parse(result));
        }else if($(custom_prop_arr[i]).attr("type")=="radio"){
            if($(custom_prop_arr[i]).prop("checked")){
                obj[key] = $(custom_prop_arr[i]).val();
            }
        }else{
            obj[key] = $(custom_prop_arr[i]).val();
        }

    }
    return obj;
};

var getForm = function (form,data) {
    var obj=data;
    var arr=[];
    for (var i in obj){
        if(typeof  obj[i] =="object"){
            console.log(JSON.stringify(obj[i]).toString().replace(/\{|\}|\"/gi,""));
            var str = JSON.stringify(obj[i]).toString().replace(/\{|\}|\"/gi,"");
            var str_arr = str.split(",");
            for(var j=0;j<str_arr.length;j++){
                var str_pos = str_arr[j].indexOf(":");
                console.log( form +" [data-key='"+i+"."+str_arr[j].substr(0,str_pos)+"']")
                $( form +" [data-key='"+i+"."+str_arr[j].substr(0,str_pos)+"']").val(str_arr[j].substr(str_pos+1))
            }
        }else if($( form +" [data-key="+i+"]").attr("type")=="radio"){
            $( form +" [data-key="+i+"]").each(function () {
                if($(this).val() == obj[i]){
                    $(this).prop("checked",true);
                }
            })
        }else {
            $( form +" [data-key="+i+"]").val(obj[i]);
        }
    }
    return obj;
};
module.exports ={
    valid:valid,
    setForm:setForm,
    getForm:getForm
}
