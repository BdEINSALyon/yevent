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
        var $shop = $('#cart');

        $.get('/invitation/shop/config/'+$shop.data('auth'), function(response){
            shop.guest = response;
        });

        $.get('/ticketing/prices.json', function(response){
            shop.prices = response;
        });

        document.addEventListener('contextmenu', function(evt) {
          evt.preventDefault();
        }, false);

        function refreshSeats(){

            // Store all current value for tickets numbers
            $shop.find('select.seats').each(function () {
                shop.tickets[$(this).data('id')]=parseInt($(this).val());
            });

            // Compute amount of tickets left
            var left = (shop.guest.left_seats||0) - _.reduce(_.values(shop.tickets), function(memo, num){ return memo + num; });

            // Display allowed values only
            $shop.find('select.seats').each(function () {
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

            var value = _.reduce(
                _.map( // Compute each line by select value x price of product
                    shop.tickets,
                    function(value, key){
                        return shop.prices[key]['price']*value
                    }),
                function(memo, num){
                    return memo + num;
                });
            if(_.reduce(_.values(shop.tickets), function(memo, num){ return memo + num; })>0){
                $shop.find('#order_button').show();
            } else {
                $shop.find('#order_button').hide();
            }
            $shop.find("#total").html(value.toFixed(2).toString().replace('.',',')+' €')


        }

        if($shop.find('select.seats').length > 0)
            setInterval(refreshSeats, 250);

    });

})(shop);
