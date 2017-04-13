'''Handles the connection to Beam Chat servers'''

import requests
from .evented import Evented
from .socket import Socket
from .errors import NotAuthenticatedError


class Connection(Evented):
    '''Connection Class'''

    def __init__(self, config):
        super(Connection, self).__init__()
        self.config = config
        self.chat_details = None
        self.userid = None

    def _buildurl(self, path):
        """Creates an address to Beam with the given path."""
        return self.config.BEAM_URI + path

    def _get_chat_details(self):
        """gets chat connection details from Beam"""

        # Creates the header for the request
        header = {'Media-Type': 'application/json',
                  'Authorization': 'Bearer ' + self.config.ACCESS_TOKEN}
        # Get the request and return the responce
        url = self._buildurl(self.config.CHATSCID_URI.format(
            cid=self.config.CHANNELID))
        self.chat_details = requests.get(url=url, headers=header).json()
        url = self._buildurl(self.config.USERSCURRENT_URI)
        self.userid = requests.get(url=url, headers=header).json()['id']

    def _connect_to_chat(self):
        """Connects to the chat websocket."""

        if self.chat_details is None:
            raise NotAuthenticatedError("You must first log in to Beam!")

        self.websocket = Socket(self.chat_details["endpoints"])
        self.websocket.on("opened", self._send_auth_packet)
        self.websocket.on("message", lambda msg: self.emit("message", msg))

    def _send_auth_packet(self):
        """Sends an authentication packet to the chat server"""
        self.websocket.send(
            "method",
            self.config.CHANNELID, self.userid, self.chat_details["authkey"],
            method="auth")

    def authenticate(self):
        """Gets beam connection info and connects to the chat server."""
        self._get_chat_details()
        self._connect_to_chat()

    def message(self, msg):
        """Sends a chat message."""
        self.websocket.send("method", msg, method="msg")
