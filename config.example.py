''' Config File '''

# DO NOT CHANGE THESE VALUES OR THE BOT WILL BREAK
BEAM_URI = 'https://beam.pro/api/v1/'
USERSCURRENT_URI = 'users/current'
CHATSCID_URI = 'chats/{cid}'

# THE SETTINGS BELOW CAN BE CHANGED
# This need to be the ID for the channel you wish to join
# https://beam.pro/api/v1/channels/channelname?fields=id
CHANNELID = '123456'

# This is up to you to obtain. This can be done though
# Rest API. for more info https://dev.beam.pro/reference/oauth/index.html
ACCESS_TOKEN = 'EnterYourAccessToken'

# Client ID, obtained from https://beam.pro/lab
# select OAUTH CLIENTS and copy ID
CLIENTID = 'EnterYourClientID'


# enables/disables raw chat details as recieved from the server
# without the chat formatting
CHATDEBUG = False
