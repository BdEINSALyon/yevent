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
            console.log(shop.guest);
            var $select = $("#id_max_seats");
            var left = (shop.guest.left_seats || 0);
            var count = 0;
            $select.children().each(function () { // Children of select are options
                if (parseInt($(this).attr('value')) > left) {
                    // Option is hidden if it will exceed amount of allowed tickets
                    $(this).remove();
                }
                count++;
            });
            while (count <= left) {
                $select.append("<option value=\"" + count + "\">" + count + "</option>");
                count++;
            }
        });

    });

})(shop);
