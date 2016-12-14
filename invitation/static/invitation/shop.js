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
    shop.listen = false;
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

    shop.timeoutToRefresh = function(){
        setInterval(function(){
            $.get('/shop/orders/'+shop.order_id+'.json', function(order){
                if(order.status == 1){
                    clearTimeout(refreshTimeout);
                    // Thanks for your order
                    $("#yurplan-iframe").addClass('hidden');
                    $("#timeout").hide();
                    $("#success").show();
                    $("#success-image").show();
                } else if(order.status >= 2) {
                    clearTimeout(refreshTimeout);
                    // Error to process
                    $("#yurplan-iframe").addClass('hidden');
                    $("#timeout").hide();
                    $("#error").show();
                }
            })
        }, 5*1000);
        var timeLeft = 3.5*60;
        function timecounter(){
            timeLeft--;
            if(timeLeft <= 0){
                window.location.reload(true);
                return;
            }
            var minutes = Math.floor(timeLeft/60);
            $('#timeout-minutes').html((minutes<10?'0':'')+minutes.toString());
            var seconds = Math.floor(timeLeft%60);
            $('#timeout-seconds').html((seconds<10?'0':'')+seconds.toString());
            refreshTimeout = setTimeout(timecounter, 1000);
        }
        var refreshTimeout = setTimeout(timecounter, 1000);
        $("#timeout").show();
    };

    $(function(){
        var $iframe = $("#yurplan-iframe");

        document.addEventListener('contextmenu', function(evt) {
          evt.preventDefault();
        }, false);

        $iframe.on('load', function () {
            console.log('Frame Loaded');

            // Retrieve iFrame content
            try {
                if($iframe.attr('scrolling') != 'no')
                    $iframe.attr('scrolling', 'no');
                shop.listen = true;
                $shop = $iframe.contents();
            } catch(e){ // Can not access to the iFrame content
                if($iframe.attr('scrolling') != 'auto')
                    $iframe.attr('scrolling', 'auto');
                if($iframe.height() != '650px')
                    $iframe.height('650px');
                shop.listen = false;
                return;
            }

            var location = $iframe[0].contentWindow.location.href;
            console.log(location);

            if(location.match(/\/form\/advanced/g)){
                shop.state = SHOP_FILLING_FORM;
            } else if(location.match(/\/shop\//g)) {
                shop.state = SHOP_WORKSHOP;
            } else if(location.match(/\/confirm\/([A-Z0-9]+)\/validation/g)){
                shop.order_id = /\/confirm\/([A-Z0-9]+)\/validation/g.exec(location)[1];
                shop.state = SHOP_PAYMENT;
                var count = _.reduce(_.values(shop.tickets), function(memo, num){ return memo + num; });
                $shop.find('form').submit(function(){
                    $.get('/shop/complete/'+$iframe.data('auth')+
                        '?yurplan_id='+encodeURIComponent(shop.order_id)+'&seats_count='+count, function (result) {
                        console.log(result)
                    });
                    shop.timeoutToRefresh();
                });
            } else if($shop.find('.password_event').length>0){
                shop.state = SHOP_NOT_READY;
            } else {
                if($shop.find('.widget-header .active.last').length>0){
                    var $header = $shop.find('.widget-header');
                    var $lastTitle = $header.find('.last');
                     if($lastTitle.hasClass('hide')) {
                        $header.children().addClass('hide');
                        $lastTitle.removeClass('hide');
                        $lastTitle.removeClass('col-sm-3');
                        $lastTitle.removeClass('col-sm-4');
                    }
                    if ($shop.find('.alert.alert-success').length > 0) {
                        shop.state = SHOP_SUCCESS;
                    } else {
                        shop.state = SHOP_FAILURE;
                    }
                } else {
                    shop.state = SHOP_SELECTING_PRODUCTS;
                }
            }

            $iframe.contents()[0].addEventListener('contextmenu', function(evt) {
              evt.preventDefault();
            }, false);

            $shop.find('#lost-order').remove();
            $shop.find('img[src*=logo]').remove();
            $shop.find('img[src*=us]').remove();
            $shop.find('img[src*=fr]').remove();
            $shop.find('#alert-already-ordered').remove();
            $shop.find('.display-workshop-button').remove();
            $shop.find('.display-workshop').show();
            $shop.find('.widget-connect-me').remove();
            $shop.find('.no-account').remove();
        });

        $.get('/shop/config/'+$iframe.data('auth'), function(response){
            shop.guest = response;
        });
        var $shop = null;

        setInterval(function shopStateDetection(){

            if(!shop.listen) return;

            // If user come back to the start state, go to not ready mode
            if($shop.find('.password_event').length>0 && shop.hasNotState([SHOP_NOT_READY, SHOP_LOGGING])) {
                shop.state = SHOP_NOT_READY;
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

                            if(left<0){
                                // Bug!
                                $shop.find('select.nbSeat').val(0);
                                shop.tickets = {};
                                left = shop.guest.left_seats||0;
                            }

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
        }, 300);
    });

})();
