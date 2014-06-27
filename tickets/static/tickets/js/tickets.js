function validate_reply(nb) {
    if (!$('#form-reply-' + nb).find('#id_response').val()) {
        $('#response-input-' + nb).addClass('has-error');
        $('#response-input-' + nb).popover('show');
        return false;
    }
    return true;
}

var NEW_TICKET_FIELDS = ['#id_title', '#id_problem'];

function validate_new_ticket() {
    var ret = true;

    for (var i = 0; i < NEW_TICKET_FIELDS.length; ++i) {
        var field = $(NEW_TICKET_FIELDS[i]);
        if (!field.val()) {
            field.parent().addClass('has-error');
            field.parent().popover('show');
            ret = false;
        }
    }
    return ret;
}

$(function() {
    $('#new-ticket-modal').on('hide.bs.modal', function () {
        $('.create-field').popover('destroy');
        $('.create-field').removeClass('has-error');
    });
    $('.collapse').on('hide.bs.collapse', function () {
        $('.popover-collapse').popover('destroy');
        $('.response-widget').removeClass('has-error');
    });
    $('.fa-cog').hover(
        function() { $(this).addClass('fa-spin'); },
        function() { $(this).removeClass('fa-spin'); }
    );
    if (window.location.hash) {
        var panel = $('#collapse-' + window.location.hash.substr(1));

        panel.addClass('in');
        $('html,body').animate({
            scrollTop: panel.offset().top
        }, 'slow');
    }
});

window.onresize = function() {
    $('div').popover('destroy');
}

