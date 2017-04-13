"""
Example chat bot that monitors incoming messages. responds to !ping command
"""

from tornado.ioloop import IOLoop
from chatty import create
import config
import ChatEventHandler


def _handle_chat(data):
    ChatEventHandler.handler(data, CHAT)


if __name__ == "__main__":
    CHAT = create(config)

    # Tell chat to authenticate with the beam server. It'll throw
    # a chatty.errors.NotAuthenticatedError if it fails.
    CHAT.authenticate()

    # Listen for incoming messages. When they come in, just print them.
    CHAT.on("message", _handle_chat)

    # Start the tornado event loop.
    IOLoop.instance().start()
