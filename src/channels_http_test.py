'''
tests for http_channels.py
'''

import json
import requests
import other 
from echo_http_test import url 

# Tests for channels_list() function.
###################################################################################
def test_channels_list_successful(url):
    '''
    Successfuly provides a list of all channels that the authorized user is part of:
    '''

    # Clearing Database 
    other.clear()

    # Registering user 
    user_payload = {
        'email': 'chrisnassif@gmail.com',
        'password': 'password',
        'name_first': 'Chris',
        'name_last': 'Nassif'
    }
    user1 = requests.post(url + 'auth/register', json = user_payload)

    # Creating Private Channel 
    channel_payload = {
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': False
    }
    channel1 = requests.post(url + 'channels/create', json = channel_payload)

    resp = request.get(url + 'channels/list', json = {'channel_id': channel1['channel_id']})

    assert json.loads(resp.txt) ==  {'channels': [
        {
            'channel_name': 'Channel1',
            'channel_id': channel1['channel_id'],
            'is_public': False,
            'owner_members': [user1['u_id'],],
            'all_members': [user1['u_id'],],
        },
    ]}

    




