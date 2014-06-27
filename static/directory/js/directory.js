function http_redirect(url){
    window.location.href = url;
}

$(function() {
    $('.doge-picture').attr('src', STATIC_URL + '/django_doge/img/doge.png');

    $('.spinner .btn:first-of-type').on('click', function() {
      $('.spinner input').val( parseInt($('.spinner input').val(), 10) + 1);
    });
    $('.spinner .btn:last-of-type').on('click', function() {
      $('.spinner input').val( parseInt($('.spinner input').val(), 10) - 1);
    });

    $('#ldap-filter').focus();
});
