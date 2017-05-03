''' Handles and formats chat events '''


class Handler():
    '''handles chat events'''

    def __init__(self, config, chat):
        self.config = config
        self.event_types = {
            'reply': self.type_reply, 'event': self.type_event,
            'method': self.type_method, 'system': self.type_system}
        self.poll_switch = True
        self.chat = chat

    def formatting(self, data):
        '''
        checks the event type and calls the function
        relating to that event type
        '''
        func = self.event_types[data['type']]
        func(data)
        if self.config.CHATDEBUG:
            print(data)

    def type_reply(self, data):
        '''Handles the Reply type data'''
        if 'data' in data:
            if 'authenticated' in data['data']:
                if data['data']['authenticated']:
                    print('Authenticated with the server')
                else:
                    print('Authenticated Failed, Chat log restricted')
            else:
                print('Server Reply: {}'.format(str(data)))
        else:
            print('Server Reply: {}'.format(str(data['error'])))

    def type_event(self, data):
        '''handles the reply chat event types'''
        event_string = {
            'WelcomeEvent': 'Connected to the channel chat...',
            'UserJoin': '{} has joined the channel.',
            'UserLeave': '{} has left the channel.',
            'ChatMessage': '{user} : {msg}',
            'whisper': '{user} → {target} : {msg}',
            'me': '{user} {msg}',
            'PollStart': '{} has started a poll',
            'PollEnd': 'The poll started by {} has ended'}

        if data['event'] == 'WelcomeEvent':
            print(event_string[data['event']])

        elif data['event'] == 'UserJoin' or data['event'] == 'UserLeave':
            if data['data']['username'] is not None:
                print(event_string[data['event']].format(
                    data['data']['username']))

        elif data['event'] == 'PollStart':
            if self.poll_switch:
                print(event_string[data['event']].format(
                    data['data']['author']['user_name']))
                self.poll_switch = False

        elif data['event'] == 'PollEnd':
            print(event_string[data['event']].format(
                data['data']['author']['user_name']))
            self.poll_switch = True

        elif data['event'] == 'ChatMessage':
            msg = ''.join(
                item["text"] for item in data['data']["message"]["message"])
            if 'whisper' in data['data']['message']['meta']:
                print(event_string['whisper'].format(
                    user=data['data']['user_name'],
                    target=data['data']['target'],
                    msg=msg))

            elif 'me' in data['data']['message']['meta']:
                print(event_string['me'].format(
                    user=data['data']['user_name'],
                    msg=msg))
            else:
                print(event_string[data['event']].format(
                    user=data['data']['user_name'],
                    msg=msg))
                if msg == '!ping':
                    self.chat.message('Its ping pong time')

    def type_method(self, data):
        '''handles the reply chat event types'''
        if self.config.CHATDEBUG:
            if data['method'] == 'auth':
                print('Authenticating with the server...')

            elif data['method'] == 'msg':
                if self.config.CHATDEBUG:
                    print('METHOD MSG: {}'.format(str(data)))
            else:
                print('METHOD MSG: {}'.format(str(data)))

    def type_system(self, data):
        '''handles the reply chat event types'''
        if self.config.CHATDEBUG:
            print('SYSTEM MSG: {}'.format(str(data['data'])))
