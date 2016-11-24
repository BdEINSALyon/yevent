/**
 * Created by pvienne on 23/11/2016.
 */

$(function(){
    var $shop = $("#yurplan-iframe").contents();

    var loop = function(){
        if($shop.find('.password_event')){
            $shop.find('input[name=password]').val('bdeinsa').parent().submit();
        }
    };

    setInterval(loop, 100);
});
