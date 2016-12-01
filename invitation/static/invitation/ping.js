/**
 * Created by pvienne on 23/11/2016.
 */
var AUTH_TOKEN = AUTH_TOKEN || '';
$(function(){
    document.domain = 'bde-insa-lyon.fr';
    var ping = true;

    setInterval(function () {
        if(ping)
            $.get('/ping');
    }, 1000);

    $('a').click(function () {
        var link = $(this);
        $.get('/halt', function() {
           window.location = link.attr('href');
        });
        return false;
    });
    $(window).bind('beforeunload', function(){
        ping = false;
        $.ajax({
            type: 'GET',
            async: false,
            url: '/halt'
        }, function () {
            setTimeout(function () {
                ping = true;
            },1500);
        });
    });

});
