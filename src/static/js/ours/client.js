var CHAHUB = {}

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
    search: function (filters) {
        // get existing params and update them with the filters
        var params = route.query()
        Object.assign(params, filters)

        // Add query params to URL
        // This causes bugs with repeating the query params over and over, so we just replaceState now
        //route('?' + $.param(params))
        var url_params = `/?${$.param(params)}`
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
    }
}
