'''Sockets handling for the Chat Bot'''
from json import loads, dumps
from random import randint
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from .evented import Evented


class Socket(Evented):
    '''Socket Class'''

    packet_id = 0

    def __init__(self, addresses):
        super(Socket, self).__init__()

        self.connected = False
        self.ws = None
        self.addresses = addresses

        # Connect to chat
        self._connect()

    def _get_address(self):
        rnd = randint(0, len(self.addresses) - 1)
        return self.addresses[rnd]

    def _connect(self):
        address = self._get_address()
        print('Connecting to {}...'.format(address))

        websocket_connect(
            address,
            callback=self._on_open,
            on_message_callback=self.parse_packet
        )

    def parse_packet(self, packet_str):
        '''Parses each packet from the chat server'''
        if packet_str is None:
            self._on_close()
        else:
            # converts packet to a python readable format
            packet = loads(packet_str)
            self.emit("message", packet)

    def _on_open(self, future):
        if future.exception() is None:
            self.ws = future.result()
            self.connected = True
            self.emit("opened")
            self.emit('message', self.system_msg(
                'Connetion to chat servers opened...'))
        else:
            self.emit('message', self.system_msg(
                'Cannot connection to server, retying alternative servers'))
            self.connected = False

            IOLoop.instance().call_later(1, self._connect)

    def _on_close(self):
        self.connected = False
        self.emit("closed")
        self.emit('message', self.system_msg(
            'Server connection lost, retying alternative servers'))
        IOLoop.instance().call_later(1, self._connect)

    def send(self, _type, *args, **kwargs):
        '''sends a packet to the chat server'''
        if not self.connected:
            return

        # create a packet to send to the server
        packet = {
            "type": _type,
            "arguments": args,
            "id": self.packet_id
        }

        packet.update(kwargs)

        self.emit('message', packet)
        self.ws.write_message(dumps(packet))
        self.packet_id += 1

    def system_msg(self, data):
        '''builds a responce for bot system messages'''
        responce = {'type': 'system',
                    'event': 'connection',
                    'data': data}
        return responce
