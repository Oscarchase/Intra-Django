$(function() {
    new ZeroClipboard(document.getElementById("copy-button"));

    if (window.location.hash)
        $('#autologin-modal').modal('show');

    $('.doge-picture').attr('src', STATIC_URL + '/django_doge/img/doge.png');
});
