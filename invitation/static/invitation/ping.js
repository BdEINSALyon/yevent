/**
 * Created by pvienne on 23/11/2016.
 */
var AUTH_TOKEN = AUTH_TOKEN || '';
$(function(){
    document.domain = 'bde-insa-lyon.fr';

    setInterval(function () {
        $.get('/ping');
    }, 1000);

    $('.nav a').click(function () {
        var link = $(this);
        $.get('/halt', function() {
           window.location = link.attr('href');
        });
        return false;
    })

});
