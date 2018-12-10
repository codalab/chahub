/* ----------------------------------------------------------------------------
 CSRF wrapper for ajax
 ----------------------------------------------------------------------------*/

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


/* ----------------------------------------------------------------------------
 Delay timer
 ----------------------------------------------------------------------------*/
// This helper function buffers a task to only execute after a delay has been met.
//
// Like, if you're typing in an autocomplete field it should wait until you're
// finished typing before it sends the request
window.delay = (function (timer) {
    var timer = timer || 0;
    return function (callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();


/* ----------------------------------------------------------------------------
 Dates
 ----------------------------------------------------------------------------*/
var pretty_date = function (date_string) {
    if (!!date_string) {
        return luxon.DateTime.fromISO(date_string).toLocaleString(luxon.DateTime.DATE_FULL)
    } else {
        return ''
    }
}

var deadline_date = function (date_string) {
    if (!!date_string) {
        var deadline_count = luxon.DateTime.fromISO(date_string).diffNow(["months", "days", "hours", "minutes", "seconds", "milliseconds"]).toObject()
        var days_normalized = luxon.Duration.fromObject(deadline_count).shiftTo('days').toObject()

        if (deadline_count.milliseconds < 0) {
            return 'Phase ended ' + Math.abs(Math.round(days_normalized.days)) + ' days ago'
        }

        if (deadline_count.months >= 2) {
            return deadline_count.months + ' months, ' + deadline_count.days + ' days left'
        } else if (deadline_count.months >= 1) {
            return deadline_count.days + ' days left'
        } else if (deadline_count.days >= 7) {
            return deadline_count.days + ' days, ' + deadline_count.hours + ' hours left'
        } else if (deadline_count.days >= 1) {
            return deadline_count.hours + ' hours, ' + deadline_count.minutes + ' minutes left'
        } else if (deadline_count.hours >= 1) {
            return deadline_count.minutes + ' minutes left'
        }
    } else {
        return 'No Phase Deadline'
    }
};

/* ----------------------------------------------------------------------------
 Dict helpers
 ----------------------------------------------------------------------------*/
function dict_remove_empty_values(obj) {
    Object.keys(obj).forEach((key) => (obj[key] == null || obj[key] === '') && delete obj[key])
}
