'''
tests for http_standup.py
'''

import json
import requests
import other
from echo_http_test import url

# Tests for http_standup_start() function.
###################################################################################
def test_standup_start_invalid_token(url):
    '''
    Token is invalid
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
    user1 = requests.post(url + 'auth/register', json=user_payload).json()

    # Creating Private Channel
    channel_payload = {
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': False
    }
    channel1 = requests.post(url + 'channels/create', json=channel_payload).json()

    standup_payload = {
        'token': 'Invalid Token',
        'channel_id': channel1['channel_id'],
        'length': 60
    }

    resp = requests.post(url + 'standup/start', json=standup_payload).json()
    assert 'code' in resp
    assert resp['code'] == 400

def test_standup_start_invalid_channel_id(url):
    '''
    Channel ID is invalid.
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
    user1 = requests.post(url + 'auth/register', json=user_payload).json()

    standup_payload = {
        'token': user1['token'],
        'channel_id': 321,
        'length': 60
    }

    resp = requests.post(url + 'standup/start', json=standup_payload).json()
    assert 'code' in resp
    assert resp['code'] == 400

def test_standup_start_already_active1(url):
    '''
    Standup already running on this channel.
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
    user1 = requests.post(url + 'auth/register', json=user_payload).json()

    # Creating Private Channel
    channel_payload = {
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': False
    }
    channel1 = requests.post(url + 'channels/create', json=channel_payload).json()

    standup_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 60
    }
    # Standup 1 
    requests.post(url + 'standup/start', json=standup_payload).json()

    resp = requests.post(url + 'standup/start', json=standup_payload).json()
    assert 'code' in resp
    assert resp['code'] == 400

def test_standup_start_already_acive2(url):
    '''
    Standup already running on this channel. Another user attempts to create a standup
    within the same channel.
    '''

    # Clearing Database
    requests.delete(url + 'clear')

    # Registering user1
    user1_payload = {
        'email': 'chrisnassif@gmail.com',
        'password': 'password',
        'name_first': 'Chris',
        'name_last': 'Nassif'
    }
    user1 = requests.post(url + 'auth/register', json=user1_payload).json()

    # Registering user1
    user2_payload = {
        'email': 'john@gmail.com',
        'password': 'password',
        'name_first': 'John',
        'name_last': 'Smith'
    }
    user2 = requests.post(url + 'auth/register', json=user2_payload).json()

    # Creating Private Channel
    channel_payload = {
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': False
    }
    channel1 = requests.post(url + 'channels/create', json=channel_payload).json()

    standup1_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 60
    }
    # Standup 1 
    requests.post(url + 'standup/start', json=standup1_payload).json()

    standup2_payload = {
        'token': user2['token'],
        'channel_id': channel1['channel_id'],
        'length': 60
    }

    resp = requests.post(url + 'standup/start', json=standup2_payload).json()
    assert 'code' in resp
    assert resp['code'] == 400

def test_standup_start_successful(url):
    '''
    Standup successfully started.
    '''

    # Clearing Database
    requests.delete(url + 'clear')

    # Registering user1
    user1_payload = {
        'email': 'chrisnassif@gmail.com',
        'password': 'password',
        'name_first': 'Chris',
        'name_last': 'Nassif'
    }
    user1 = requests.post(url + 'auth/register', json=user1_payload).json()

    # Creating Public Channel
    channel_payload = {
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True
    }
    channel1 = requests.post(url + 'channels/create', json=channel_payload).json()

    standup1_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 600
    }
    resp = requests.post(url + 'standup/start', json=standup1_payload).json()
    
    standup = {}
    for standup in other.data['standup']:
        if standup['channel_id'] == channel1['channel_id']:
            break

    assert resp == {'time_finish': standup['time_finish']}

# Tests for htto_standup_active() function.
###################################################################################
