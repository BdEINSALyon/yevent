/**
 * Created by pvienne on 23/11/2016.
 */

var shop = {};

(function (shop) {
    const SHOP_NOT_READY = 'NOT_READY';
    const SHOP_READY = 'READY';

    shop.state = SHOP_NOT_READY;
    shop.tickets = {};
    shop.guest = {};

    $(function(){

        setInterval(function () {
            $.get('/shop/ping/'+shop.auth);
        }, 5000);

        $.get('/shop/config/'+shop.auth, function(response){
            shop.guest = response;
        });

    });

})(shop);
