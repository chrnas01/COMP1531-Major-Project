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
    requests.delete(url + 'clear')

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

    # Generating a list of channels the user is apart of 
    resp = request.get(url + 'channels/list', json = {'token': user1['token']})

    assert json.loads(resp.txt) ==  {'channels': [
        {
            'channel_name': 'Channel1',
            'channel_id': channel1['channel_id'],
            'is_public': False,
            'owner_members': [user1['u_id'],],
            'all_members': [user1['u_id'],],
        },
    ]}

def test_channels_list_successful_two_channels():
    '''
    Successfuly provides a list of all channels that the authorized user is part of:
    '''

    # Clearing Database 
    requests.delete(url + 'clear')

    # Registering user 
    user_payload = {
        'email': 'chrisnassif@gmail.com',
        'password': 'password',
        'name_first': 'Chris',
        'name_last': 'Nassif'
    }
    user1 = requests.post(url + 'auth/register', json = user_payload)

    # Creating Private and Public Channel 
    channel_payload1 = {
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': False
    }
    channel1 = requests.post(url + 'channels/create', json = channel_payloa1)

    channel_payload2 = {
        'token': user1['token'],
        'name': 'Channel2',
        'is_public': True
    }
    channel2 = requests.post(url + 'channels/create', json = channel_payload2)

    # Generating a list of channels the user is apart of 
    resp = request.get(url + 'channels/list', json = {'token': user1['token']})

    assert json.loads(resp.txt) ==  {'channels': [
        {
            'channel_name': 'Channel1',
            'channel_id': channel1['channel_id'],
            'is_public': False,
            'owner_members': [user1['u_id'],],
            'all_members': [user1['u_id'],],
        },
        {
            'channel_name': 'Channel_2',
            'channel_id': channel2['channel_id'],
            'is_public': True,
            'owner_members': [user1['u_id'],],
            'all_members': [user1['u_id'],],
        },
    ]}

def test_channels_list_no_channels():
    '''
    User doesnt belong to any channels
    '''
    
    # Clearing Database 
    requests.delete(url + 'clear')

    # Registering users 
    user_payload1 = {
        'email': 'chrisnassif@gmail.com',
        'password': 'password',
        'name_first': 'Chris',
        'name_last': 'Nassif'
    }
    user1 = requests.post(url + 'auth/register', json = user_payload1)

    user_payload2 = {
        'email': 'johnsmith@gmail.com',
        'password': 'password',
        'name_first': 'John',
        'name_last': 'Smith'
    }
    user2 = requests.post(url + 'auth/register', json = user_payload2)

    # User 1 creates private channel 
    channel_payload = {
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': False
    }
    channel1 = requests.post(url + 'channels/create', json = channel_payload)

    # Generating a list of channels user 2 is apart of 
    resp = request.get(url + 'channels/list', json = {'token': user2['token']})
    assert json.loads(resp.txt) == {'channels': []}

    # Tests for channels_listall() function.
###################################################################################

def test_channels_listall_successful():
    '''
    Successfully provides a list of all channels and their associated details
    '''