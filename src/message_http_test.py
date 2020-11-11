import pytest
import re
from subprocess import Popen, PIPE
from datetime import datetime, timezone
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

    resp = requests.get(url + 'other/get_messages', params=payload).json()

    expected_result = {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'test',
                'time_created': resp['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            }
        ]
    }

    assert resp == expected_result


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
    resp = requests.post(url + 'message/send', json=payload).json()

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
    resp = requests.post(url + 'message/send', json=payload).json()

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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id']
    }
    requests.delete(url + 'message/remove', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'start': 0
    }

    expected_result = {
        'messages': []
    }

    resp = requests.get(url + 'other/get_messages', params=payload)
    assert resp.json() == expected_result

########################################################

# http_message_edit

def test_message_edit_invalid_sender(url, setup):
    '''
    editing a message that was sent by a different user
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id'],
        'message': 'edit'
    }

    # AccessError
    resp = requests.put(url + 'message/edit', json=payload)
    resp.status_code == 400

def test_message_edit_invalid_perms(url, setup):
    '''
    editing a message without permissions
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_2['token'],
        'message_id': resp['message_id'],
        'message': 'edit'
    }

    # AccessError
    resp = requests.put(url + 'message/edit', json=payload)
    resp.status_code == 400

def test_message_edit_success(url, setup):
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id'],
        'message': 'edit'
    }
    requests.put(url + 'message/edit', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'start': 0
    }

    resp = requests.get(url + 'other/get_messages', params=payload).json()

    expected_result = {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'edit',
                'time_created': resp['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            }
        ]
    }

    assert resp == expected_result

########################################################

def test_send_later_invalid_channel(url, setup):
    '''
    sending a message later to an invalid channel
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
        'channel_id': 99,
        'message': 'test',
        'time_sent': int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 5
    }

    # InputError
    resp = requests.post(url + 'message/sendlater', json=payload)
    resp.status_code == 400

def test_send_later_invalid_message(url, setup):
    '''
    sending message later that is too long
    '''
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    msg = ''
    for i in range(1001):
        msg += str(i)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'message': msg,
        'time_sent': int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 5
    }

    # InputError
    resp = requests.post(url + 'message/sendlater', json=payload)
    resp.status_code == 400

def test_send_later_invalid_time(url, setup):
    '''
    sending message later at time in the past
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
        'message': 'test',
        'time_sent': int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) - 5
    }

    # InputError
    resp = requests.post(url + 'message/sendlater', json=payload)
    resp.status_code == 400

def test_send_later_invalid_access(url, setup):
    '''
    sending message later when user has not joined the channel
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
        'message': 'test',
        'time_sent': int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 5
    }

    # AccessError
    resp = requests.post(url + 'message/sendlater', json=payload)
    resp.status_code == 400

def test_send_later_valid(url, setup):
    '''
    sending message later
    '''
    user_1, user_1, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    time = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 5

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test',
        'time_sent': time
    }
    requests.post(url + 'message/sendlater', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'start': 0
    }

    resp = requests.get(url + 'other/get_messages', params=payload).json()

    expected_result = {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'test',
                'time_created': time,
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            }
        ]
    }

    assert resp == expected_result

########################################################

def test_react_invalid_message(url, setup):
    '''
    reacting to a message that is in a channel the user is not a part of
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id'],
        'react_id': 1
    }

    # InputError
    resp = requests.post(url + 'message/react', json=payload)
    resp.status_code == 400

def test_react_invalid_react(url, setup):
    '''
    reacting to a message with a react that doesn't exist
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id'],
        'react_id': 99
    }

    # InputError
    resp = requests.post(url + 'message/react', json=payload)
    resp.status_code == 400

def test_react_already_reacted(url, setup):
    '''
    reacting to a message that you have already reacted to
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id'],
        'react_id': 1
    }
    requests.post(url + 'message/react', json=payload)

    # InputError
    resp = requests.post(url + 'message/react', json=payload)
    resp.status_code == 400

def test_react_valid(url, setup):
    '''
    reacting to a message
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id'],
        'react_id': 1
    }
    requests.post(url + 'message/react', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'start': 0
    }

    resp = requests.get(url + 'other/get_messages', params=payload).json()

    expected_result = {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'test',
                'time_created': resp['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [user_1['u_id']],
                    'is_this_user_reacted': True
                }],
                'is_pinned': False
            }
        ]
    }

    assert resp == expected_result

########################################################

def test_unreact_invalid_message(url, setup):
    '''
    reacting to a message that is in a channel the user is not a part of
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id'],
        'react_id': 1
    }

    # InputError
    resp = requests.post(url + 'message/unreact', json=payload)
    resp.status_code == 400

def test_unreact_invalid_react(url, setup):
    '''
    reacting to a message with a react that doesn't exist
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id'],
        'react_id': 99
    }

    # InputError
    resp = requests.post(url + 'message/unreact', json=payload)
    resp.status_code == 400

def test_unreact_already_unreacted(url, setup):
    '''
    reacting to a message that you have already reacted to
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id'],
        'react_id': 1
    }

    # InputError
    resp = requests.post(url + 'message/unreact', json=payload)
    resp.status_code == 400

def test_unreact_valid(url, setup):
    '''
    reacting to a message
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id'],
        'react_id': 1
    }
    requests.post(url + 'message/react', json=payload)
    requests.post(url + 'message/unreact', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'start': 0
    }

    resp = requests.get(url + 'other/get_messages', params=payload).json()

    expected_result = {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'test',
                'time_created': resp['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            }
        ]
    }

    assert resp == expected_result

########################################################

def test_pin_invalid_message(url, setup):
    '''
    pinning a message that does not exist
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': 99
    }

    # InputError
    resp = requests.post(url + 'message/pin', json=payload)
    resp.status_code == 400

def test_pin_invalid_channel(url, setup):
    '''
    pinning a message that is in a channel the user is not a part of
    '''
    user_1, user_2, _ = setup

    payload = {
        'token': user_2['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test'
    }
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id']
    }

    # AccessError
    resp = requests.post(url + 'message/pin', json=payload)
    resp.status_code == 400

def test_pin_already_pinned(url, setup):
    '''
    pinning a message that is already pinned
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id']
    }
    requests.post(url + 'message/pin', json=payload)

    # InputError
    resp = requests.post(url + 'message/pin', json=payload)
    resp.status_code == 400

def test_pin_invalid_perms(url, setup):
    '''
    pinning a message when you are not an owner
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_2['token'],
        'message_id': resp['message_id']
    }

    # AccessError
    resp = requests.post(url + 'message/pin', json=payload)
    resp.status_code == 400

def test_pin_valid(url, setup):
    '''
    pinning to a message
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id']
    }

    requests.post(url + 'message/pin', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'start': 0
    }

    resp = requests.get(url + 'other/get_messages', params=payload).json()

    expected_result = {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'test',
                'time_created': resp['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': True
            }
        ]
    }

    assert resp == expected_result

########################################################

def test_unpin_invalid_message(url, setup):
    '''
    unpinning a message that does not exist
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': 99
    }

    # InputError
    resp = requests.post(url + 'message/unpin', json=payload)
    resp.status_code == 400

def test_unpin_invalid_channel(url, setup):
    '''
    unpinning a message that is in a channel the user is not a part of
    '''
    user_1, user_2, _ = setup

    payload = {
        'token': user_2['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test'
    }
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_2['token'],
        'message_id': resp['message_id']
    }
    requests.post(url + 'message/pin', json=payload)

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id']
    }

    # AccessError
    resp = requests.post(url + 'message/unpin', json=payload)
    resp.status_code == 400

def test_unpin_already_unpinned(url, setup):
    '''
    unpinning a message that is already pinned
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
    requests.post(url + 'message/send', json=payload)

    # InputError
    resp = requests.post(url + 'message/unpin', json=payload)
    resp.status_code == 400

def test_unpin_invalid_perms(url, setup):
    '''
    pinning a message when you are not an owner
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id']
    }
    requests.post(url + 'message/pin', json=payload)

    payload = {
        'token': user_2['token'],
        'message_id': resp['message_id']
    }

    # AccessError
    resp = requests.post(url + 'message/unpin', json=payload)
    resp.status_code == 400

def test_unpin_valid(url, setup):
    '''
    pinning to a message
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
    resp = requests.post(url + 'message/send', json=payload).json()

    payload = {
        'token': user_1['token'],
        'message_id': resp['message_id']
    }

    requests.post(url + 'message/pin', json=payload)
    requests.post(url + 'message/unpin', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'start': 0
    }

    resp = requests.get(url + 'other/get_messages', params=payload).json()

    expected_result = {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'test',
                'time_created': resp['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            }
        ]
    }

    assert resp == expected_result

########################################################