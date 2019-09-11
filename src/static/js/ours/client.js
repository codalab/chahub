var CHAHUB = {}

CHAHUB.api = {
    request: function (method, url, data) {
        if(method.toLowerCase() !== "get") {
            data = JSON.stringify(data)
        }

        return $.ajax({
            type: method,
            url: url,
            data: data,
            contentType: "application/json",
            dataType: 'json'
        })
    },
    search: function (filters) {
        // Add query params to URL
        // This causes bugs with repeating the query params over and over, so we just replaceState now
        //route('?' + $.param(params))
        var url_params = `/?${$.param(filters)}`
        window.history.replaceState("", "", url_params);
        return CHAHUB.api.request('GET', URLS.API + "query" + url_params)
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
    },
    // Producer Stats
    get_producer_stats: function() {
        return CHAHUB.api.request('GET', URLS.API + "producer_stats/")
    },
    // ------------------------------------------------------------------------
    // Users
    get_user: function(id) {
        return CHAHUB.api.request('GET', URLS.API + "users/" + id + "/")
    },
    delete_user: function(id) {
        return CHAHUB.api.request('DELETE', `${URLS.API}users/${id}/`)
    },
    // Merge requests
    create_merge: function(data) {
        return CHAHUB.api.request('POST', URLS.API + "create_merge_request/", data)
    },
}
