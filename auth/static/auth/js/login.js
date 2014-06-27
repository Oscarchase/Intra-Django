var HIDDEN_TIMEOUT = 1200;
var TIMER_INTERVAL = 20;
var DY = 1;
var DOGE_SIZE_FACTOR = 2.0;
var DOGE_SHOW_BODY_FACTOR = 1.5;

function animate_doge() {
    var timerId;
    var y = 0;
    var dy = DY;
    var doge = $('<img id="secret-doge">');
    var widget = $('#id_username');

    doge.attr('src', STATIC_URL + '/django_doge/img/doge.png');
    doge.prependTo('#login-content');

    function update_doge(dtop) {
        var w = widget.width() / DOGE_SIZE_FACTOR;
        doge.css({
            'width'  : w,
            'height' : w,
            'left'   : widget.offset().left + w / 2,
            'top'    : widget.offset().top - dtop,
            'clip'   : 'rect(0px, ' + w + 'px, ' + dtop + 'px, 0px)'
        });
    }

    function doge_stay() {
        setTimeout(function() {
            timerId = setInterval(make_a_wild_doge_appear, TIMER_INTERVAL);
        }, HIDDEN_TIMEOUT);
    }

    function make_a_wild_doge_appear() {
        y += dy;
        update_doge(y);
        if (y <= 0 ||
            y >= widget.width() / DOGE_SIZE_FACTOR / DOGE_SHOW_BODY_FACTOR) {
            dy = -dy;
            clearInterval(timerId);
            doge_stay();
        }
    }

    update_doge(0);
    doge_stay();
}

$(function() {
    $('#id_username').focus();
    $('.login-field').popover('show');
    animate_doge();
});

window.onresize = function() {
    $('.login-field').popover('destroy');
}
