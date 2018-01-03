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
    $(".ui.dropdown").dropdown()


    /*-----------------------------------------------------------------------------
     Sockets
     */
    var ws_protocol = window.location.protocol == 'https:' ? 'wss' : 'ws'
    var socket = new ReconnectingWebSocket(ws_protocol + '://' + window.location.host + '/')
    socket.onmessage = function(e) {
        toastr.success("Received msg: " + e.data)
    }
    window.socket = socket


    /*-----------------------------------------------------------------------------
     Riotjs
     */
    riot.mount('*')
})
