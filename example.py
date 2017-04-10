"""
Example chat bot that monitors incoming messages and sends "Hi!" every second.
"""

import os
from tornado.ioloop import PeriodicCallback, IOLoop
from chatty import create
import config

def format_msg(data):
    ''' formats the msg text string properly '''
    msg = ''
    list_count = len(data['message']['message'])
    for counter in range(0, list_count):
        msg += str(data['message']['message'][counter]['text'])
    return msg

def chat_commands(data):
    ''' function to process chat commands and display console output '''
    if 'message' in data:
        msg = data['user_name'] + ' : ' + format_msg(data)
        if 'whisper' in data['message']['meta']:
            # formats whisper msg's appending [W]
            print('[W] ' + msg)
        else:
            #formats standard chat msg's
            print(msg)
        # uncomment next line for raw data
        #print('RECIEVED : ' + str(data))

        # will respond to the command !ping
        if data['message']['message'][0]['text'] == '!ping':
            CHAT.message("It's ping pong time...")
    else:
        print('RECIEVED : ' + str(data))

if __name__ == "__main__":
    CHAT = create(config)

    # Tell chat to authenticate with the beam server. It'll throw
    # a chatty.errors.NotAuthenticatedError if it fails.
    CHAT.authenticate()

    # Listen for incoming messages. When they come in, just print them.
    CHAT.on("message", chat_commands)

    # Create a timer that sends the message "Hi!" every second.
    '''PeriodicCallback(
        lambda: chat.message('Hi!'),
        1000
    ).start()'''

    # Start the tornado event loop.
    IOLoop.instance().start()
