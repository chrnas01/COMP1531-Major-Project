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
    
    assert resp == {'time_finish': resp['time_finish']}

# Tests for htto_standup_active() function.
###################################################################################
def test_standup_active_invalid_token(url):
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
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 60
    }
    requests.post(url + 'standup/start', json=standup_payload).json()

    active_payload = {
        'token': 'Invalid token',
        'channel_id': channel1['channel_id']
    }

    resp = requests.get(url + 'standup/active', params=active_payload).json()
    assert 'code' in resp
    assert resp['code'] == 400

def test_standup_active_invalid_channel_id(url):
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
    requests.post(url + 'standup/start', json=standup_payload).json()

    active_payload = {
        'token': user1['token'],
        'channel_id': 321
    }

    resp = requests.get(url + 'standup/active', params=active_payload).json()
    assert 'code' in resp
    assert resp['code'] == 400

def test_standup_active_inactive(url):
    '''
    Calling standup_active function when there is no standup occuring
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

    active_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id']
    }
    resp = requests.get(url + 'standup/active', params=active_payload).json()
    assert resp == {'is_active': False, 'time_finish': None}


def test_standup_active_successful(url):
    '''
    Standup successfully detected and correct finishing time returned
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

    # Starting Standup
    standup_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 60
    }
    standup1 = requests.post(url + 'standup/start', json=standup_payload).json()
    
    active_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id']
    }
    resp = requests.get(url + 'standup/active', params=active_payload).json()
    assert resp == {'is_active': True, 'time_finish': standup1['time_finish']}

# Tests for standup_send() function.
###################################################################################
def test_standup_send_invalid_token(url):
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
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 60
    }
    requests.post(url + 'standup/start', json=standup_payload).json()

    send_payload = {
        'token': 'Invalid token',
        'channel_id': channel1['channel_id'],
        'message': 'Invalid Token'
    }

    resp = requests.post(url + 'standup/send', json=send_payload).json()
    assert 'code' in resp
    assert resp['code'] == 400

def test_standup_send_invalid_channel_id(url):
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
    requests.post(url + 'standup/start', json=standup_payload).json()

    send_payload = {
        'token': user1['token'],
        'channel_id': 123,
        'message': 'Invalid Channel ID'
    }

    resp = requests.post(url + 'standup/send', json=send_payload).json()
    assert 'code' in resp
    assert resp['code'] == 400

def test_standup_send_message_too_long(url):
    '''
    Message is more than 1000 characters long
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
    requests.post(url + 'standup/start', json=standup_payload).json()

    send_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 1001*'A'
    }

    resp = requests.post(url + 'standup/send', json=send_payload).json()
    assert 'code' in resp
    assert resp['code'] == 400

def test_standup_send_message_1000char(url):
    '''
    Boundary Test: Message is exactly 1000 characters long
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
    requests.post(url + 'standup/start', json=standup_payload).json()

    send_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 1000*'A'
    }

    resp = requests.post(url + 'standup/send', json=send_payload).json()
    assert resp == {}

def test_standup_send_no_active_standup(url):
    '''
    An active standup is not currently running in this channel
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

    send_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'No active standup'
    }

    resp = requests.post(url + 'standup/send', json=send_payload).json()
    assert 'code' in resp
    assert resp['code'] == 400

def test_standup_send_member_not_user(url):
    '''
    The authorised user is not a memeber of the channel that the messasge is within
    '''

    # Clearing Database
    requests.delete(url + 'clear')

    # Registering user
    user1_payload = {
        'email': 'chrisnassif@gmail.com',
        'password': 'password',
        'name_first': 'Chris',
        'name_last': 'Nassif'
    }
    user1 = requests.post(url + 'auth/register', json=user1_payload).json()

    user2_payload = {
        'email': 'johnsmith@gmail.com',
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

    standup_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 60
    }
    requests.post(url + 'standup/start', json=standup_payload).json()

    send_payload = {
        'token': user2['token'],
        'channel_id': channel1['channel_id'],
        'message': 'User 2 is not a memeber of this channel'
    }
    resp = requests.post(url + 'standup/send', json=send_payload).json()
    
    assert 'code' in resp
    assert resp['code'] == 400


def test_standup_send_multiple_users(url):
    '''
    Users can successfully send messages
    '''

    # Clearing Database
    requests.delete(url + 'clear')

    # Registering users
    user1_payload = {
        'email': 'chrisnassif@gmail.com',
        'password': 'password',
        'name_first': 'Chris',
        'name_last': 'Nassif'
    }
    user1 = requests.post(url + 'auth/register', json=user1_payload).json()

    user2_payload = {
        'email': 'johnsmith@gmail.com',
        'password': 'password',
        'name_first': 'John',
        'name_last': 'Smith'
    }
    user2 = requests.post(url + 'auth/register', json=user2_payload).json()

    user3_payload = {
        'email': 'brucelee@gmail.com',
        'password': 'password',
        'name_first': 'Bruce',
        'name_last': 'Lee'
    }
    user3 = requests.post(url + 'auth/register', json=user3_payload).json()

    # Creating a Public Channel
    channel_payload = {
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True
    }
    channel1 = requests.post(url + 'channels/create', json=channel_payload).json()

    # Users joining channel
    join_payload1 = {
        'token': user2['token'],
        'channel_id': channel1['channel_id']
    }
    requests.post(url + 'channel/join', json=join_payload1).json()

    join_payload2 = {
        'token': user3['token'],
        'channel_id': channel1['channel_id']
    }
    requests.post(url + 'channel/join', json=join_payload2).json()

    # Creating Standup 
    standup_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 60
    }
    requests.post(url + 'standup/start', json=standup_payload).json()

    # Sending multiple messages
    send1_payload = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'User 1 is speaking'
    }
    resp1 = requests.post(url + 'standup/send', json=send1_payload).json()
    assert resp1 == {}

    send2_payload = {
        'token': user2['token'],
        'channel_id': channel1['channel_id'],
        'message': 'User 2 is speaking'
    }
    resp2 = requests.post(url + 'standup/send', json=send2_payload).json()
    assert resp2 == {}

    send3_payload = {
        'token': user3['token'],
        'channel_id': channel1['channel_id'],
        'message': 'User 3 is speaking'
    }
    resp3 = requests.post(url + 'standup/send', json=send3_payload).json()
    assert resp3 == {}
