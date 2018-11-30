$(document).ready(function () {
    /*-----------------------------------------------------------------------------
     Template niceties
     */
    // fix menu when passed
    $('.masthead')
        .visibility({
            once: false,
            onBottomPassed: function () {
                $('.fixed.menu').transition('fade in')
            },
            onBottomPassedReverse: function () {
                $('.fixed.menu').transition('fade out')
            }
        })


    // create sidebar and attach to menu open
    $('.ui.sidebar').sidebar('attach events', '.toc.item')

    // dropdowns (nice non-select ones!)
    //$(".ui.dropdown").dropdown()


    /*-----------------------------------------------------------------------------
     Sockets
     */
    var ws_protocol = window.location.protocol == 'https:' ? 'wss' : 'ws'










    // @@@@@@@@ Disabling sockets for now! @@@@@@@@
    /*
    var socket = new ReconnectingWebSocket(ws_protocol + '://' + window.location.host + '/')





    // TODO: Have a whitelist for allowed event types so someone can't maliciously call events like "delete_competition"
    // var allowed_message_types = [
    //     "competition_add",
    //     "competition_update"
    // ]










    socket.onmessage = function(e) {
        var update_message = JSON.parse(e.data)

        toastr.success("Received msg: " + e.data)
        //console.log(e)

        // console.log(update_message.type + ": " + update_message.data)
        CHAHUB.events.trigger(update_message.type, update_message.data)
    }
    window.socket = socket
    */


    /*-----------------------------------------------------------------------------
     Riotjs
     */
    CHAHUB.events = riot.observable()

    //riot.mount('*')

    // Make the URLs in riotjs router start from / instead of the default #
    // route.base('/')
})
