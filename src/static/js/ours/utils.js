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

function num_formatter(num, digits) {
    var si = [
        {value: 1, symbol: ""},
        {value: 1E3, symbol: "K"},
        {value: 1E6, symbol: "M"},
        {value: 1E9, symbol: "G"},
        {value: 1E12, symbol: "T"},
        {value: 1E15, symbol: "P"},
        {value: 1E18, symbol: "E"}
    ]
    var rx = /\.0+$|(\.[0-9]*[1-9])0+$/
    var i
    for (i = si.length - 1; i > 0; i--) {
        if (num >= si[i].value) {
            break
        }
    }
    return (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol
}

/* ----------------------------------------------------------------------------
 Dict helpers
 ----------------------------------------------------------------------------*/
function dict_remove_empty_values(obj) {
    Object.keys(obj).forEach((key) => (obj[key] == null || obj[key] === '') && delete obj[key])
}
