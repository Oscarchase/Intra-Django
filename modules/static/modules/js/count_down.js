var COUNTDOWN_SUFFIX = ' left to register'

function formatCountdown(data) {
    var timeUnits = []
    for (var key in data)
        if (data[key])
            timeUnits.push(data[key] + ' ' + key)
    return timeUnits.join(', ')
}

function invalidateRegistration() {
    $('#register-button').addClass('disabled')
    $('#register-button').html('Registration is closed')
    $('#countdown').html('')
}

$(function() {
    var countdown = $('#countdown')

    if (countdown.length) {
        var timerId = setInterval(updateCountdown, 1000)

        function updateCountdown() {
            var dateDiff = (registerEnd - new Date) / 1000
            var days, hours, minutes, seconds

            if (dateDiff < 0) {
                clearInterval(timerId)
                return invalidateRegistration()
            }

            days = dateDiff / 86400
            dateDiff %= 86400
            hours = dateDiff / 3600
            dateDiff %= 3600
            minutes = dateDiff / 60
            seconds = dateDiff % 60

            var countdownString = formatCountdown({
                'days' : Math.floor(days),
                'hours' : Math.floor(hours),
                'minutes' : Math.floor(minutes),
                'seconds' : Math.floor(seconds),
            })
            countdown.html(countdownString + COUNTDOWN_SUFFIX)
        }
    }
})
