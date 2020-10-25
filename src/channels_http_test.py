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
    user1 = requests.post(url + 'auth/register', json=user_payload)

    # Creating Private Channel 
    channel_payload = {
        'token': user1.json()['token'],
        'name': 'Channel1',
        'is_public': False
    }
    channel1 = requests.post(url + 'channels/create', json=channel_payload)

    # Generating a list of channels the user is apart of 
    resp = requests.get(url + 'channels/list', params={'token': user1.json()['token']})

    assert json.loads(resp.text) ==  {'channels': [
        {
            'channel_name': 'Channel1',
            'channel_id': channel1.json()['channel_id'],
            'is_public': False,
            'owner_members': [user1.json()['u_id'],],
            'all_members': [user1.json()['u_id'],]
        }
    ]}


def test_channels_list_successful_two_channels(url):
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
    user1 = requests.post(url + 'auth/register', json=user_payload)

    # Creating Private and Public Channel 
    channel_payload1 = {
        'token': user1.json()['token'],
        'name': 'Channel1',
        'is_public': False
    }
    channel1 = requests.post(url + 'channels/create', json=channel_payload1)

    channel_payload2 = {
        'token': user1.json()['token'],
        'name': 'Channel2',
        'is_public': True
    }
    channel2 = requests.post(url + 'channels/create', json=channel_payload2)

    # Generating a list of channels the user is apart of 
    resp = requests.get(url + 'channels/list', params={'token': user1.json()['token']})

    assert json.loads(resp.text) ==  {'channels': [
        {
            'channel_name': 'Channel1',
            'channel_id': channel1.json()['channel_id'],
            'is_public': False,
            'owner_members': [user1.json()['u_id']],
            'all_members': [user1.json()['u_id']]
        },
        {
            'channel_name': 'Channel2',
            'channel_id': channel2.json()['channel_id'],
            'is_public': True,
            'owner_members': [user1.json()['u_id'],],
            'all_members': [user1.json()['u_id'],],
        }
    ]}

def test_channels_list_no_channels(url):
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
    user1 = requests.post(url + 'auth/register', json=user_payload1)

    user_payload2 = {
        'email': 'johnsmith@gmail.com',
        'password': 'password',
        'name_first': 'John',
        'name_last': 'Smith'
    }
    user2 = requests.post(url + 'auth/register', json=user_payload2)

    # User 1 creates private channel 
    channel_payload = {
        'token': user1.json()['token'],
        'name': 'Channel1',
        'is_public': False
    }
    requests.post(url + 'channels/create', json=channel_payload)

    # Generating a list of channels user 2 is apart of 
    resp = requests.get(url + 'channels/list', params={'token': user2.json()['token']})
    assert json.loads(resp.text) == {'channels': []}

    # Tests for channels_listall() function.
###################################################################################

def test_channels_listall_successful(url):
    '''
    Successfully provides a list of all channels and their associated details
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
    user1 = requests.post(url + 'auth/register', json=user_payload)

    # Creating Private and Public Channel 
    channel_payload1 = {
        'token': user1.json()['token'],
        'name': 'Channel1',
        'is_public': False
    }
    channel1 = requests.post(url + 'channels/create', json=channel_payload1)

    channel_payload2 = {
        'token': user1.json()['token'],
        'name': 'Channel2',
        'is_public': True
    }
    channel2 = requests.post(url + 'channels/create', json=channel_payload2)

    # Generating a list of channels the user is apart of 
    resp = requests.get(url + 'channels/listall', params={'token': user1.json()['token']})

    assert json.loads(resp.text) ==  {'channels': [
        {
            'channel_name': 'Channel1',
            'channel_id': channel1.json()['channel_id'],
            'is_public': False,
            'owner_members': [user1.json()['u_id']],
            'all_members': [user1.json()['u_id']]
        },
        {
            'channel_name': 'Channel2',
            'channel_id': channel2.json()['channel_id'],
            'is_public': True,
            'owner_members': [user1.json()['u_id']],
            'all_members': [user1.json()['u_id']]
        }
    ]}

def test_channels_listall_no_existing_channels(url):
    '''
    If there are no existing channels channels_listall() should return an empty list
    '''
     # Clearing Database 
    requests.delete(url + 'clear')

    # Registering user 
    user_payload1 = {
        'email': 'chrisnassif@gmail.com',
        'password': 'password',
        'name_first': 'Chris',
        'name_last': 'Nassif'
    }
    user1 = requests.post(url + 'auth/register', json=user_payload1)

     # Generating a list of channels that exist 
    resp = requests.get(url + 'channels/listall', params={'token': user1.json()['token']})
    assert json.loads(resp.text) == {'channels': []}

# Tests for channels_create() function.
###################################################################################

def test_channels_create_invalid_channel_name1(url):
    '''
    Public channel name is greater than 20 characters long
    '''

    # Clearing Database 
    requests.delete(url + 'clear')

    # Registering user
    user_payload1 = {
        'email': 'chrisnassif@gmail.com',
        'password': 'password',
        'name_first': 'Chris',
        'name_last': 'Nassif'
    }
    user1 = requests.post(url + 'auth/register', json=user_payload1)

    # Creatinng Channel
    channel_payload = {
        'token': user1.json()['token'],
        'name': 'ChannelNameGreaterthan20characters',
        'is_public': True
    }
    resp = requests.post(url + 'channels/create', json=channel_payload)
    assert 'code' in resp.json()
    assert resp.json()['code'] == 400


def test_channels_create_invalid_channel_name2(url):
    '''
    Private channel name is greater than 20 characters long
    '''
    
    # Clearing Database 
    requests.delete(url + 'clear')

    # Registering user
    user_payload1 = {
        'email': 'chrisnassif@gmail.com',
        'password': 'password',
        'name_first': 'Chris',
        'name_last': 'Nassif'
    }
    user1 = requests.post(url + 'auth/register', json=user_payload1)

    # Creatinng Channel
    channel_payload = {
        'token': user1.json()['token'],
        'name': 'ChannelNameGreaterthan20characters',
        'is_public': False
    }
    resp = requests.post(url + 'channels/create', json=channel_payload)
    assert 'code' in resp.json()
    assert resp.json()['code'] == 400 

def test_channels_create_20char_channel_name(url):
    '''
    Boundary Test: Channel name is exactly 20 characters long
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
    user1 = requests.post(url + 'auth/register', json=user_payload)

    # Creatinng Channel
    channel_payload = {
        'token': user1.json()['token'],
        'name': 20*'a',
        'is_public': False
    }
    resp = requests.post(url + 'channels/create', json=channel_payload)
    assert json.loads(resp.text) == {'channel_id': 1}

def test_channels_create_successful_public(url):
    '''
    Public channel is successfully created
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
    user1 = requests.post(url + 'auth/register', json=user_payload)

    # Creatinng Channel
    channel_payload = {
        'token': user1.json()['token'],
        'name': 'Channel1',
        'is_public': True
    }
    resp = requests.post(url + 'channels/create', json=channel_payload)
    assert json.loads(resp.text) == {'channel_id': 1}

def test_channels_create_successful_private(url):
    '''
    Private channel is successfully created
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
    user1 = requests.post(url + 'auth/register', json=user_payload)

    # Creatinng Channel
    channel_payload = {
        'token': user1.json()['token'],
        'name': 'Channel1',
        'is_public': False
    }
    resp = requests.post(url + 'channels/create', json = channel_payload)
    assert json.loads(resp.text) == {'channel_id': 1}

def test_channels_create_name_exists(url):
    '''
    Channel name already exists
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
    user1 = requests.post(url + 'auth/register', json=user_payload1)

    user_payload2 = {
        'email': 'johnsmith@gmail.com',
        'password': 'password',
        'name_first': 'John',
        'name_last': 'Smith'
    }
    user2 = requests.post(url + 'auth/register', json=user_payload2)
    
    # Creating Channel 
    channel_payload1 = {
        'token': user1.json()['token'],
        'name': 'Channel1',
        'is_public': True
    }
    requests.post(url + 'channels/create', json=channel_payload1)
    
    channel_payload2 = {
        'token': user2.json()['token'],
        'name': 'Channel1',
        'is_public': True
    }
    resp = requests.post(url + 'channels/create', json = channel_payload2)
    assert 'code' in resp.json()
    assert resp.json()['code'] == 400 

def test_channels_create_nameless_channel(url):
    '''
    Channel name is not input i.e. trying to make a channel without a name
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
    user1 = requests.post(url + 'auth/register', json=user_payload)

    # Creatinng Channel
    channel_payload = {
        'token': user1.json()['token'],
        'name': '',
        'is_public': False
    }
    resp = requests.post(url + 'channels/create', json=channel_payload)
    assert 'code' in resp.json()
    assert resp.json()['code'] == 400 

def test_channels_create_successful_private_multi(url):
    '''
    Creating multiple channels (Testing the channel_id progression system)
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
    user1 = requests.post(url + 'auth/register', json=user_payload)

    # Creatinng Channels
    channel_payload1 = {
        'token': user1.json()['token'],
        'name': 'Channel1',
        'is_public': True
    }
    resp = requests.post(url + 'channels/create', json=channel_payload1)
    assert json.loads(resp.text) == {'channel_id': 1}

    channel_payload2 = {
        'token': user1.json()['token'],
        'name': 'Channel2',
        'is_public': False
    }
    resp = requests.post(url + 'channels/create', json=channel_payload2)
    assert json.loads(resp.text) == {'channel_id': 2}

    channel_payload3 = {
        'token': user1.json()['token'],
        'name': 'Channel3',
        'is_public': True
    }
    resp = requests.post(url + 'channels/create', json=channel_payload3)
    assert json.loads(resp.text) == {'channel_id': 3}
