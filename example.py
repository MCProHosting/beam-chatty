"""
Example chat bot that monitors incoming messages. responds to !ping command
"""

from tornado.ioloop import IOLoop
from chatty import create
import config
import ChatEventHandler


def _handle_chat(data):
    chatevents.formatting(data)


if __name__ == "__main__":
    chat = create(config)
    chatevents = ChatEventHandler.Handler(config, chat)
    # Tell chat to authenticate with the beam server. It'll throw
    # a chatty.errors.NotAuthenticatedError if it fails.
    chat.authenticate()

    # Listen for incoming messages. When they come in, just print them.
    chat.on("message", _handle_chat)

    # Start the tornado event loop.
    IOLoop.instance().start()
