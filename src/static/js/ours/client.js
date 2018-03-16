var CHAHUB = {
    URLS: []  // Set in base.html
}

CHAHUB.api = {
    request: function (method, url, data) {
        return $.ajax({
            type: method,
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: 'json'
        })
    },
    search: function (query) {
        route('/?' + $.param(query))
        return CHAHUB.api.request('GET', URLS.API + "query/?" + $.param(query))
    },
    // ------------------------------------------------------------------------
    // Producers
    get_producers: function() {
        return CHAHUB.api.request('GET', URLS.API + "producers/")
    },
    create_producer: function(data) {
        return CHAHUB.api.request('POST', URLS.API + "producers/", data)
    },
    update_producer: function(pk, data) {
        return CHAHUB.api.request('PUT', URLS.API + "producers/" + pk + "/", data)
    },
    delete_producer: function(pk) {
        return CHAHUB.api.request('DELETE', URLS.API + "producers/" + pk + "/")
    }
}
