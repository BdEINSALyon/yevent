/**
 * Created by pvienne on 23/11/2016.
 */



(function () {
    var shop = {};
    const SHOP_NOT_READY = 'NOT_READY';
    const SHOP_LOGGING = 'LOGGING';
    const SHOP_SELECTING_PRODUCTS = 'SELECTING_PRODUCTS';
    const SHOP_FILLING_FORM = 'FILLING_FORM';
    const SHOP_PAYMENT = 'PAYMENT';
    const SHOP_SUCCESS = 'SUCCESS';
    const SHOP_FAILURE = 'FAILURE';

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
        var $iframe = $("#yurplan-iframe");

        document.addEventListener('contextmenu', function(evt) {
          evt.preventDefault();
        }, false);

        $iframe.on('load', function () {
            $iframe.contents()[0].addEventListener('contextmenu', function(evt) {
              evt.preventDefault();
            }, false);
        });

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

            var $header = $shop.find('.widget-header');
            if($header.length > 0) {
                // We are on the last
                if ($header.find('.active.last').length > 0 && shop.hasNotState([SHOP_SUCCESS, SHOP_FAILURE])) {
                    if ($shop.find('.alert.alert-success').length > 0) {
                        shop.state = SHOP_SUCCESS;
                        // Handle a shop success
                        var yurplan_id = $($shop.find('.alert.alert-success a')[0]).attr('href').split('?',2)[0];
                        var count = _.reduce(_.values(shop.tickets), function(memo, num){ return memo + num; });
                        $.get('/shop/complete/'+$iframe.data('auth')+
                            '?yurplan_id='+encodeURIComponent(yurplan_id)+'&seats_count='+count, function (result) {
                            console.log(result)
                        })
                    } else {
                        shop.state = SHOP_FAILURE;
                    }
                    if($shop.find('.share').parent().parent().css('display')!='none')
                        $shop.find('.share').parent().parent().hide();
                }
                if ($header.find('> div:nth-of-type(2)').hasClass('active')){
                    shop.state = SHOP_FILLING_FORM;
                }
                if ($header.find('> div:nth-of-type(4)').length > 0){
                    if ($header.find('> div:nth-of-type(3)').hasClass('active')){
                        shop.state = SHOP_PAYMENT;
                    }
                }
            }

            // Listening loops by states
            switch(shop.state){
                case SHOP_NOT_READY:
                    if(shop.guest.check == undefined) break;
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
                        $shop.find('input[name=password]').attr('autocomplete','off');
                        $shop.find('input[name=password]').attr('type','text');
                        $shop.find('input[name=password]').val(shop.guest.check);
                        $shop.find('input[type=submit]').closest("form").submit();
                    } else if($shop.find('.ticket-event').length>0) {
                        shop.state = SHOP_SELECTING_PRODUCTS;
                    }
                    break;
                case SHOP_SELECTING_PRODUCTS:
                    $shop.find('#lost-order').remove();
                    $shop.find('img[src*=logo]').remove();
                    if((shop.guest.left_seats||0)<2) {
                        // Hide 2 seats tickets
                        $shop.find('#1971.category-label').remove();
                        $shop.find('#1971.category-container').remove();
                    }

                    // Store all current value for tickets numbers
                    $shop.find('select.nbSeat').each(function () {
                        var factor = 1;
                        if($shop.find('#1971.category-container').has($(this)).length){
                            factor = 2;
                        }
                        shop.tickets[$(this).attr('name')]=parseInt($(this).val()) * factor;
                    });

                    // Compute amount of tickets left
                    var left = (shop.guest.left_seats||0) - _.reduce(_.values(shop.tickets), function(memo, num){ return memo + num; });

                    // Display allowed values only
                    $shop.find('select.nbSeat').each(function () {
                        var factor = 1;
                        if($shop.find('#1971.category-container').has($(this)).length){
                            factor = 2;
                        }
                        var selected = parseInt($(this).val());
                        var count = 0;
                        $(this).children().each(function(){ // Children of select are options
                            $(this).attr('value', count);
                            if(parseInt($(this).html()) != count)
                                $(this).html(count);
                            if(parseInt($(this).attr('value'))*factor > selected + left){
                                // Option is hidden if it will exceed amount of allowed tickets
                                $(this).hide();
                            } else {
                                // Else display it
                                $(this).show();
                            }
                            count++;
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

})();
