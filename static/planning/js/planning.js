$(function() {
    var options = {
        tmpl_path : STATIC_URL + 'planning/tmpls/',
        events_source : EVENT_URL,
        onAfterViewLoad : postProcess,
        language: LANGUAGE_CODE
    };

    var calendar = $('#calendar').calendar(options);

    $('.btn-group button[data-calendar-nav]').each(function() {
        var $this = $(this);
        $this.click(function() {
            calendar.navigate($this.data('calendar-nav'));
        });
    });

    $('.btn-group button[data-calendar-view]').each(function() {
        var $this = $(this);
        $this.click(function() {
            calendar.view($this.data('calendar-view'));
        });
    });

    function postProcess(view) {
        $('#calendar-title').text(this.getTitle());
    }
})
