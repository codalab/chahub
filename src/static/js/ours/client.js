var CHAHUB = {}

CHAHUB.api = {
    request: function (method, url, data) {
        if(method.toLowerCase() !== "get") {
            data = JSON.stringify(data)
        }
        url = `${URLS.API}${url}`

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
        return CHAHUB.api.request('GET', "query" + url_params)
    },
    // ------------------------------------------------------------------------
    // Producers
    get_producers: function() {
        return CHAHUB.api.request('GET', "producers/")
    },
    create_producer: function(data) {
        return CHAHUB.api.request('POST', "producers/", data)
    },
    update_producer: function(pk, data) {
        return CHAHUB.api.request('PUT', "producers/" + pk + "/", data)
    },
    delete_producer: function(pk) {
        return CHAHUB.api.request('DELETE', "producers/" + pk + "/")
    },
    // Producer Stats
    get_producer_stats: function() {
        return CHAHUB.api.request('GET', "producer_stats/")
    },
    // ------------------------------------------------------------------------
    // Users
    get_user: function(id) {
        return CHAHUB.api.request('GET', "users/" + id + "/")
    },
    delete_user: function(id) {
        return CHAHUB.api.request('DELETE', `users/${id}/`)
    },
    delete_profile: function (user_pk, profile_pk) {
        return CHAHUB.api.request('DELETE', `users/${user_pk}/scrub_profile/`, {profile_pk: profile_pk})
    },
    // ------------------------------------------------------------------------
    // Email
    add_email: function(user_pk, email_address) {
        return CHAHUB.api.request('POST', `users/${user_pk}/add_email_address/`, {email_address: email_address})
    },
    resend_verification_email(user_pk, email_pk) {
        return CHAHUB.api.request('POST', `users/${user_pk}/resend_verification_email/`, {email_pk: email_pk})
    },
    delete_email: function (user_pk, email_pk) {
        return CHAHUB.api.request('DELETE', `users/${user_pk}/remove_email_address/`, {email_pk: email_pk})
    },
    make_primary_email: function (user_pk, email_pk) {
        return CHAHUB.api.request('POST', `users/${user_pk}/change_primary_email/`, {email_pk: email_pk})
    },
    // Merge requests
    create_merge: function(data) {
        return CHAHUB.api.request('POST', URLS.API + "create_merge_request/", data)
    },
}
