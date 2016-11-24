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
    shop.tickets = {};
    shop.guest = {};
    shop.registerState = function (state) {
        if(shop.state != state){
            shop.state = state;
        }
    };
    shop.hasState = function(states){
        if(!(states instanceof Array))
            states = [states];
        return states.indexOf(shop.state) >= 0;
    };
    shop.hasNotState = function(states){
        return !shop.hasState(states);
    };

    $(function(){
        document.domain = 'bde-insa-lyon.fr';
        var $iframe = $("#yurplan-iframe");

        $.get('/shop/config/'+$iframe.data('auth'), function(response){
            shop.guest = response;
        });

        setInterval(function shopStateDetection(){
            var $shop = null;

            // Retrieve iFrame content
            try {
                $shop = $iframe.contents();
            } catch(e){ // Can not access to the iFrame content
                if(shop.state != SHOP_NOT_READY){
                    $iframe.hide();
                }
                return;
            }

            // If user come back to the start state, go to not ready mode
            if($shop.find('.password_event').length>0 && shop.hasNotState([SHOP_NOT_READY, SHOP_LOGGING])) {
                shop.state = SHOP_NOT_READY;
            }

            // Listening loops by states
            switch(shop.state){
                case SHOP_NOT_READY:
                    if($shop.find('.password_event').length>0){
                        shop.state = SHOP_LOGGING;
                        $iframe.one('load', function(){ // When form has been loaded
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
                    break;
                case SHOP_SELECTING_PRODUCTS:
                    // Store all current value for tickets numbers
                    $shop.find('select.nbSeat').each(function () {
                        shop.tickets[$(this).attr('name')]=parseInt($(this).val());
                    });

                    // Compute amount of tickets left
                    var left = (shop.guest.left_seats||0) - _.reduce(_.values(shop.tickets), function(memo, num){ return memo + num; });

                    // Display allowed values only
                    $shop.find('select.nbSeat').each(function () {
                        var selected = parseInt($(this).val());
                        $(this).children().each(function(){ // Children of select are options
                            if(parseInt($(this).attr('value')) > selected + left){
                                // Option is hidden if it will exceed amount of allowed tickets
                                $(this).hide();
                            } else {
                                // Else display it
                                $(this).show();
                            }
                        })
                    });
                    break;

            }

            // Update display
            if(shop.hasNotState([SHOP_NOT_READY, SHOP_LOGGING])) {
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
