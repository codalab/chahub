# from channels import Group
#
#
# def ws_message(message):
#     # ASGI WebSocket packet-received and send-packet message types
#     # both have a "text" key for their textual data.
#     message.reply_channel.send({
#         "text": message.content['text'],
#     })
#
#
# def ws_add(message):
#     """On connection"""
#     # Accept the incoming connection
#     message.reply_channel.send({"accept": True})
#     # Add them to the chat group
#     Group("updates").add(message.reply_channel)
#
#
# def ws_disconnect(message):
#     Group("updates").discard(message.reply_channel)
