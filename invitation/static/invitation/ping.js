/**
 * Created by pvienne on 23/11/2016.
 */
var AUTH_TOKEN = AUTH_TOKEN || '';
$(function(){
    document.domain = 'bde-insa-lyon.fr';

    setInterval(function () {
        $.get('/ping');
    }, 1000);

    $('a').click(function () {
        var link = $(this);
        $.get('/halt', function() {
           window.location = link.attr('href');
        });
        return false;
    });
    $(window).on('unload', function () {
        console.log('Unload!');
        $.ajax({
            type: 'GET',
            async: false,
            url: '/halt'
        }, function () {
            console.log('Halted')
        });
    });

});
