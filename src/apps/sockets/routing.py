# from channels.routing import route
#
# from . import consumers
#
#
# channel_routing = [
#     # This makes regular HTTP requests come through our channels!!!! AH!!
#     # route("http.request", "sockets.consumers.http_consumer"),
#
#     route("websocket.connect", consumers.ws_add),
#     route("websocket.receive", consumers.ws_message),
#     route("websocket.receive", consumers.ws_message),
# ]
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            # chat.routing.websocket_urlpatterns
        ])
    ),
})
