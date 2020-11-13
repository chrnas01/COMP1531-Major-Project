'''
Tests functions in other.py
'''
from datetime import datetime, timezone
import json
import requests
import other
import pytest
from echo_http_test import url

@pytest.fixture
def setup(url):
    '''
    Resets user data for each test
    '''
    # Clear database
    other.clear()

    # Setup users
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload) # Owner

    payload = {
        'email': 'Steven@gmail.com',
        'password': 'password',
        'name_first': 'Steven',
        'name_last': 'Luong'
    }
    user_2 = requests.post(url + 'auth/register', json=payload)

    payload = {
        'email': 'sam@gmail.com',
        'password': 'password',
        'name_first': 'Sam',
        'name_last': 'He'
    }
    user_3 = requests.post(url + 'auth/register', json=payload)

    return (user_1, user_2, user_3)


################################################################################


def test_admin_userpermission_change_invalid_uid(url, setup):
    '''
    Changing user permission of u_id that does not exist
    '''
    requests.delete(url + 'clear')

    # Setup pytest
    user_1, _, _ = setup

    payload = {
        'token': user_1.json()['token'],
        'u_id': 99,
        'permission_id': 1
    }
    resp = requests.post(url + 'admin/userpermission/change', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400


def test_admin_userpermission_change_invalid_permission_id(url, setup):
    '''
    Changing user permission with wrong permission_id
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    payload = {
        'token': user_1.json()['token'],
        'u_id': user_2.json()['u_id'],
        'permission_id': 0
    }
    resp = requests.post(url + 'admin/userpermission/change', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400


def test_admin_userpermission_change_unauthorised_user(url, setup):
    '''
    Changing user permission with wrong unauthorised user
    '''
    # Setup pytest
    _, user_2, user_3 = setup

    payload = {
        'token': user_2.json()['token'],
        'u_id': user_3.json()['u_id'],
        'permission_id': 1
    }
    resp = requests.post(url + 'admin/userpermission/change', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400


def test_admin_userpermission_change_success(url, setup):
    '''
    Successful admin user permission change
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Test that {} was returned (Not an error)
    payload = {
        'token': user_1.json()['token'],
        'u_id': user_2.json()['u_id'],
        'permission_id': 1
    }
    resp = requests.post(url + 'admin/userpermission/change', json=payload)
    assert json.loads(resp.text) == {}

    # Test that user permission was changed
    payload = {
        'user_1': user_1.json(),
        'user_2': user_2.json()
    }
    resp = requests.post(url + 'other/successful/permissions', json=payload)
    assert json.loads(resp.text) == {'successful': True}

################################################################################

def test_search(url, setup):
    '''
    searching in a channel
    '''
    user_1, user_2, _ = setup

    payload = {
        'token': user_1.json()['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1.json()['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2.json()['u_id']
    }
    requests.post(url + 'channel/invite', json=payload).json()

    payload = {
        'token': user_1.json()['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'msg'
    }
    requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_1.json()['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test'
    }
    requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_1.json()['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'Hello'
    }
    requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_2.json()['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test2'
    }
    requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_1.json()['token'],
        'query_str': 'est',
    }

    resp = requests.get(url + '/search', params=payload).json()

    expected_result = {
        'messages': [
            {
                'message_id': 2,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1.json()['u_id'],
                'message': 'test',
                'time_created': resp['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            },
            {
                'message_id': 4,
                'channel_id': channel_data['channel_id'],
                'u_id': user_2.json()['u_id'],
                'message': 'test2',
                'time_created': resp['messages'][1]['time_created'],
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

def test_search_other_channel(url, setup):
    '''
    searching in a separate channel
    '''
    user_1, user_2, _ = setup

    payload = {
        'token': user_1.json()['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2.json()['token'],
        'name': 'test channel2',
        'is_public': False
    }
    channel_data2 = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1.json()['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2.json()['u_id']
    }
    requests.post(url + 'channel/invite', json=payload).json()

    payload = {
        'token': user_1.json()['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'msg'
    }
    requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_1.json()['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'test'
    }
    requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_1.json()['token'],
        'channel_id': channel_data['channel_id'],
        'message': 'Hello'
    }
    requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_2.json()['token'],
        'channel_id': channel_data2['channel_id'],
        'message': 'test2'
    }
    requests.post(url + 'message/send', json=payload)

    payload = {
        'token': user_1.json()['token'],
        'query_str': 'e',
    }

    resp = requests.get(url + '/search', params=payload).json()

    expected_result = {
        'messages': [
            {
                'message_id': 2,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1.json()['u_id'],
                'message': 'test',
                'time_created': resp['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            },
            {
                'message_id': 3,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1.json()['u_id'],
                'message': 'Hello',
                'time_created': resp['messages'][1]['time_created'],
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
    