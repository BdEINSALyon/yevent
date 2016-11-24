/**
 * Created by pvienne on 23/11/2016.
 */

var shop = {};

(function (shop) {
    const SHOP_NOT_READY = 'NOT_READY';
    const SHOP_LOGGING = 'LOGGING';
    const SHOP_SELECTING_PRODUCTS = 'SELECTING_PRODUCTS';
    const SHOP_FILLING_FORM = 'FILLING_FORM';
    const SHOP_PAYMENT = 'PAYMENT';
    const SHOP_SUCCESS = 'SUCCESS';

    shop.state = SHOP_NOT_READY;

    $(function(){
        document.domain = 'bde-insa-lyon.fr';
        var $iframe = $("#yurplan-iframe");

        setInterval(function shopStateDetection(){
            var $shop = null;
            try {
                $shop = $iframe.contents();
            } catch(e){ // Can not access to the iFrame content
                if(shop.state != SHOP_NOT_READY){
                    $iframe.hide();
                }
                return;
            }

            if($shop.find('.password_event').length>0 && [SHOP_NOT_READY, SHOP_LOGGING].indexOf(shop.state)) {
                shop.state = SHOP_NOT_READY;
            }

            switch(shop.state){
                case SHOP_NOT_READY:
                    if($shop.find('.password_event').length>0){
                        shop.state = SHOP_LOGGING;
                        $iframe.one('load', function(){
                            $shop = $iframe.contents();
                            if($shop.find('.password_event').length>0){
                                shop.state = SHOP_NOT_READY;
                            } else {
                                shop.state = SHOP_SELECTING_PRODUCTS;
                            }
                        });
                        $shop.find('input[name=password]').val('bdeinsa');
                        $shop.find('input[type=submit]').click();
                    } else if($shop.find('.ticket-event').length>0) {
                        shop.state = SHOP_SELECTING_PRODUCTS;
                    }
            }
            if(shop.state != SHOP_NOT_READY && shop.state != SHOP_LOGGING) {
                if($iframe.css('display') == 'none'){
                    $iframe.show();
                }
                try {
                    var height = $shop.find('body')[0].scrollHeight+'px';
                    if($iframe.height() != height){
                        $iframe.height(height);
                    }
                } catch(ignored){}
            } else {
                if($iframe.css('display') != 'none'){
                    $iframe.hide();
                }
            }
        }, 100);
    });

})(shop);
