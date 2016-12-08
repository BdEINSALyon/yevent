/**
 * Created by pvienne on 23/11/2016.
 */

var shop = {};

(function () {
    const SHOP_NOT_READY = 'NOT_READY';
    const SHOP_LOGGING = 'LOGGING';
    const SHOP_SELECTING_PRODUCTS = 'SELECTING_PRODUCTS';
    const SHOP_FILLING_FORM = 'FILLING_FORM';
    const SHOP_WORKSHOP = 'WORKSHOP';
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
                var $lastTitle = $header.find('.last');
                if ($header.find('.active.last').length > 0 && shop.hasNotState([SHOP_SUCCESS, SHOP_FAILURE])) {
                    if($lastTitle.hasClass('hide')) {
                        $header.children().addClass('hide');
                        $lastTitle.removeClass('hide');
                        $lastTitle.removeClass('col-sm-3');
                        $lastTitle.removeClass('col-sm-4');
                    }
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
                }else {
                    if ($header.find('> div:nth-of-type(1)').hasClass('active')) {
                        shop.state = SHOP_SELECTING_PRODUCTS;
                    }
                    if ($header.find('> div:nth-of-type(2)').hasClass('active')) {
                        shop.state = SHOP_FILLING_FORM;
                    }
                    if ($header.find('> div:nth-of-type(3)').hasClass('active')) {
                        shop.state = SHOP_WORKSHOP;
                    }
                    if ($header.find('> div:nth-of-type(5)').length > 0) {
                        if ($header.find('> div:nth-of-type(4)').hasClass('active')) {
                            shop.state = SHOP_PAYMENT;
                        }
                    }
                    if (!$lastTitle.hasClass('hide')) {
                        $lastTitle.addClass('hide');
                    }
                }
            }

            $shop.find('#lost-order').remove();
            $shop.find('img[src*=logo]').remove();
            $shop.find('img[src*=us]').remove();
            $shop.find('img[src*=fr]').remove();
            $shop.find('#alert-already-ordered').remove();
            $shop.find('.display-workshop-button').remove();
            $shop.find('.display-workshop').show();
            $shop.find('.widget-connect-me').remove();
            $shop.find('.no-account').remove();

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
                    if((shop.guest.left_seats||0)<2) {
                        // Hide 2 seats tickets
                        $shop.find('#1971.category-label').remove();
                        $shop.find('#1971.category-container').remove();
                    }

                    $shop.find('select.nbSeat').each(function(){
                        var $elem = $(this);
                        var $elemEvents = $._data(this, "events");
                        $elem.children().each(function(count) { // Children of select are options
                            if (parseInt($(this).attr('value')) != count || parseInt($(this).html()) != count) {
                                $(this).attr('value', count);
                                $(this).html(count);
                            }
                        });
                        if($elemEvents != undefined && $elemEvents['change'] != undefined){
                            return; // We are already bind
                        }

                        $elem.change(function(){ // When a select is changed
                            // Factor by two seats if it's a 2 people pack
                            var factor = 1;
                            if($shop.find('#1971.category-container').has($(this)).length){
                                factor = 2;
                            }

                            // Update the count array of tickets
                            shop.tickets[$(this).attr('name')]=parseInt($(this).val()) * factor;

                            // Sum left seats
                            var left = (shop.guest.left_seats||0) - _.reduce(_.values(shop.tickets), function(memo, num){ return memo + num; });

                            // Update each select
                            $shop.find('select.nbSeat').each(function () {
                                var factor = 1;
                                if($shop.find('#1971.category-container').has($(this)).length){
                                    factor = 2;
                                }
                                var selected = parseInt($(this).val()) * factor;
                                var count = 0;
                                $(this).children().each(function(){ // Children of select are options
                                    if(parseInt($(this).attr('value'))*factor > selected + left){
                                        // Option is hidden if it will exceed amount of allowed tickets
                                        $(this).remove();
                                    }
                                    count++;
                                });
                                while(count*factor <= selected + left){
                                    $(this).append("<option value=\""+count+"\">"+count+"</option>");
                                    count++;
                                }
                            });
                        });
                        { // Handle on the first load
                            var left = (shop.guest.left_seats || 0) - (_.reduce(_.values(shop.tickets), function (memo, num) {
                                    return memo + num;
                                })||0);
                            // Factor by two seats if it's a 2 people pack
                            var factor = 1;
                            if ($shop.find('#1971.category-container').has($(this)).length) {
                                factor = 2;
                            }
                            var selected = parseInt($(this).val()) * factor;
                            var count = 0;
                            $elem.children().each(function () { // Children of select are options
                                if (parseInt($(this).attr('value')) * factor > selected + left) {
                                    // Option is hidden if it will exceed amount of allowed tickets
                                    $(this).remove();
                                }
                                count++;
                            });
                            while (count * factor <= selected + left) {
                                $elem.append("<option value=\"" + count + "\">" + count + "</option>");
                                count++;
                            }
                        }
                    });
                    break;
                case SHOP_FILLING_FORM:
                    break;
                case SHOP_WORKSHOP:
                    var $cart = $shop.find('.cart');
                    if($shop.find('.form-actions button').length < 1) {
                        $cart.find('.toggle-cart').hide();
                        $cart.find('.cart-list').show().find('hr').remove();
                        $shop.find('.form-actions').html('<button class="btn btn-default btn-large" type="submit">Suivant</button>');
                    }
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
