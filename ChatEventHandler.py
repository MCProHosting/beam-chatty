'''
Handles all the chat events and prints to the console in a readable format
'''
import config as configuration

CONFIG = configuration


def handler(data, chat):
    ''' parse chat server packets into a readable format '''

    # Parses Server reply msg's?
    if data['type'] == 'reply':
        typereply(data)

    # handles chat events
    elif data['type'] == 'event':
        typeevent(data, chat)

    # handles all the send messages to the server
    elif data['type'] == 'method':
        type_method(data)

    # Bot System messages
    elif data['type'] == 'system':
        if CONFIG.CHATDEBUG:
            print('SYSTEM MESSAGE: ' + str(data['data']))

    else:
        # If any event has not been handled then this
        # will print the responce
        print('CHAT EVENT HANDLER: ' + str(data))


def typereply(data):
    '''Handles the Reply type data'''

    if CONFIG.CHATDEBUG:
        print('Server Reply: ' + str(data['data']))


def typeevent(data, chat):
    '''handles Event type Data'''

    # Connection welcome responce
    if data['event'] == 'WelcomeEvent':
        print("Connected to the channel chat...")

    # User Join channel Message
    elif data['event'] == 'UserJoin':
        if data['data']['username'] is not None:
            print(data['data']['username'] + ' has joined the channel.')

    # User Leave channel message
    elif data['event'] == 'UserLeave':
        if data['data']['username'] is not None:
            print(data['data']['username'] + ' has left the channel.')

    # Format all chat messages by users
    elif data['event'] == 'ChatMessage':
        if 'whisper' in data['data']['message']['meta']:
            # format chat messages (whispers)
            print(data['data']['user_name'] + ' → ' + data['data']['target'],
                  ': ' + format_msg(data['data']))
        elif 'me' in data['data']['message']['meta']:
            # format chat messages (Actions)
            print(data['data']['user_name'],
                  format_msg(data['data']))

        elif 'me' in data['data']['message']['meta']:
            # format chat messages (whispers)
            print(data['data']['user_name'],
                  format_msg(data['data']))
        else:
            # format chat messages (Regular)
            print(data['data']['user_name'] + ' : ' + format_msg(data['data']))
            # CHAT COMMAND - This will reply to a chat
            # message only containing '!ping
            if format_msg(data['data']) == '!ping':
                chat.message('Somone wants some ping pong action?')

    # A poll has started
    # has anti log spam
    elif data['event'] == 'PollStart':
        if CONFIG.POLL_SPAM:
            print('{} has started a poll'.format(
                data['data']['author']['user_name']))
            CONFIG.POLL_SPAM = False

    # A poll has ended
    elif data['event'] == 'PollEnd':
        print('The poll started by {} has ended'.format(
            data['data']['author']['user_name']))
        CONFIG.POLL_SPAM = False


def type_method(data):
    '''handles Event type Data'''

    if data['method'] == 'auth':
        print('Sending Authentication...')

    # Messages the bot sends
    elif data['method'] == 'msg':
        if CONFIG.CHATDEBUG:
            print('METHOD MESSAGE: ' + str(data))
    else:
        # catches unhandled messages
        print('METHOD MESSAGE: ' + str(data))


def format_msg(data):
    '''formats the msg text string properly'''
    msg = ''.join(item["text"] for item in data["message"]["message"])

    # returns the message
    return msg
