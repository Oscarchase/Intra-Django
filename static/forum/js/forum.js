var LEFT_NAV_COL = 2;

function destroy_popovers() {
    $('.create-field').popover('destroy');
    $('.create-field').removeClass('has-error');
}

function validate(fields) {
    var ret = true;

    for (var i = 0; i < fields.length; ++i) {
        var field = $(fields[i]);
        if (!field.val()) {
            field.parent().addClass('has-error');
            field.parent().popover('show');
            ret = false;
        }
    }
    return ret;
}

var TRHEAD_FIELDS = ['#id_title', '#id_content'];

function validate_new_thread() {
    return validate(THREAD_FIELDS);
}

var COMMENT_FIELDS = ['#id-content-comment'];

function validate_comment() {
    return validate(COMMENT_FIELDS);
}

var POST_FIELDS = ['#id-content-post'];

function validate_post() {
    return validate(POST_FIELDS);
}

$(function() {
    // Left nav
    var left_nav = $('#forum-left-nav');
    var left_nav_col = left_nav.parent();
    var main_container = $('#forum-main-container');

    left_nav.affix({
        offset: {
            top: $('#accordion').offset().top - $('header').offset().top
        }
    });

    function resize_left_nav() {
        var width = main_container.outerWidth() * LEFT_NAV_COL / 12;
        width -= (left_nav_col.innerWidth() - left_nav_col.width());
        left_nav.css('width', width + 'px');
    }

    function reset_left_nav() {
        left_nav.css('width', '');
    }

    left_nav.on('affix.bs.affix', resize_left_nav);
    left_nav.on('affix-top.bs.affix', reset_left_nav);
    resize_left_nav();
    window.onresize = resize_left_nav;

    // Modal form
    $('#new-thread-modal').on('hide.bs.modal', destroy_popovers);
    $('#comment-post-modal').on('hide.bs.modal', destroy_popovers);
    $('#reply-post-modal').on('hide.bs.modal', destroy_popovers);
});
