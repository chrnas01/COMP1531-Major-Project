import pytest
import re
from subprocess import Popen, PIPE
import signal
import requests
import json
from echo_http_test import url
import auth
import other


@pytest.fixture
def setup(url):
    '''
    Pytest fixture used to setup users
    '''
    # Clearing Database 
    requests.delete(url + 'clear')

    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'email': 'steven@gmail.com',
        'password': 'password',
        'name_first': 'Steven',
        'name_last': 'Luong'
    }
    user_2 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'email': 'sam@gmail.com',
        'password': 'password',
        'name_first': 'Sam',
        'name_last': 'He'
    }
    user_3 = requests.post(url + 'auth/register', json=payload).json()

    return user_1, user_2, user_3


########################################################

# http_message_send

def test_message_send_invalid_user(url, setup):
    '''
    sending from user who is not a member of the channel
    '''
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test'
    }

    # AccessError
    resp = requests.post(url + 'message/send', json=payload)
    resp.status_code == 400

def test_message_send_invalid_message(url, setup):
    '''
    sending a message longer than 1000 characters
    '''
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'A' * 1001
    }

    # InputError
    resp = requests.post(url + 'message/send', json=payload)
    resp.status_code == 400

def test_message_send_success(url, setup):
    '''
    successful call
    '''
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test'
    }
    resp = requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'start': 0
    }

    expected_result = {
        'messages': ['test'],
        'start': 0,
        'end': -1
    }

    resp = requests.get(url + 'channel/messages', params=payload)
    assert resp.json() == expected_result


########################################################

# http_message_remove

def test_message_remove_invalid_message(url, setup):
    '''
    removing a message that doesn't exist
    '''
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': 99
    }

    # InputError
    resp = requests.delete(url + 'message/remove', json=payload)
    resp.status_code == 400

def test_message_remove_invalid_sender(url, setup):
    '''
    removing a message that was sent by a different user
    '''
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/invite', json=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test'
    }
    resp = requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id']
    }

    # AccessError
    resp = requests.delete(url + 'message/remove', json=payload)
    resp.status_code == 400

def test_message_remove_invalid_perms(url, setup):
    '''
    removing a message without permissions
    '''
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/invite', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test'
    }
    resp = requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_2['token'],
        'message_id': resp['message_id']
    }

    # AccessError
    resp = requests.delete(url + 'message/remove', json=payload)
    resp.status_code == 400

def test_message_remove_success(url, setup):
    '''
    successful call
    '''
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test'
    }
    resp = requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id']
    }

    expected_result = {
        'messages': [],
        'start': 0,
        'end': -1
    }

    resp = requests.get(url + 'channel/messages', params=payload)
    assert resp.json() == expected_result

########################################################

# http_message_edit

########################################################