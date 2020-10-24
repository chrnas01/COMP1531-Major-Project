import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
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

def test_channel_invite_invalid_channel_id(url, setup):
    '''
    inviting to a channel which does not exist
    '''

    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'channel_id': 99,
        'u_id': user_2['u_id']
    }

    # InputError
    resp = requests.post(url + 'channel/invite', json=payload)
    resp.status_code == 400


def test_channel_invite_invalid_uid(url, setup):
    '''
    inviting a user who does not exist
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
        'u_id': 99
    }

    # InputError
    resp = requests.post(url + 'channel/invite', json=payload)
    resp.status_code == 400


def test_channel_invite_invalid_access(url, setup):
    '''
    channel is private and user is not a member
    '''
    user_1, user_2, user_3 = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }

    # AccessError
    resp = requests.post(url + 'channel/invite', json=payload)
    resp.status_code == 400


def test_channel_invite_success(url, setup):
    '''
    channel invite success
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
    requests.post(url + 'channel/invite', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    resp = requests.get(url + 'channel/details', params=payload)

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            }
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
    }

    assert resp.json() == expected_result

########################################################


def test_channel_details_invalid_channel_id(url, setup):
    '''
    channel does not exist
    '''
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'channel_id': 99
    }

    # InputError
    resp = requests.get(url + 'channel/details', params=payload)
    resp.status_code == 400


def test_channel_details_invalid_access(url, setup):
    '''
    user is not a member of that channel
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
        'channel_id': channel_data['channel_id']
    }

    # AccessError
    resp = requests.get(url + 'channel/details', params=payload)
    resp.status_code == 400


def test_channel_details_success(url, setup):
    '''
    successful call
    '''
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
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
        'channel_id': channel_data['channel_id']
    }
    resp = requests.get(url + 'channel/details', params=payload)

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            }
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
    }

    assert resp.json() == expected_result


########################################################

def test_channel_messages_invalid_channel_id(url, setup):
    '''
    channel does not exist
    '''
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'channel_id': 99,
        'start': 0
    }

    # InputError
    resp = requests.get(url + 'channel/messages', params=payload)
    resp.status_code == 400

def test_channel_messages_invalid_start(url, setup):
    '''
    start does not exist
    '''
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'start': 100
    }

    # InputError
    resp = requests.get(url + 'channel/messages', params=payload)
    resp.status_code == 400

def test_channel_messages_invalid_user(url, setup):
    '''
    user does not have perms
    '''
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'start': 0
    }

    # AccessError
    resp = requests.get(url + 'channel/messages', params=payload)
    resp.status_code == 400

def test_channel_messages_success(url, setup):
    '''
    successful call
    '''
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'start': 0
    }

    expected_result = {
        'messages': [],
        'start': 0,
        'end': -1
    }

    resp = requests.get(url + 'channel/messages', params=payload)
    assert resp.json() == expected_result

########################################################


def test_channel_leave_invalid_channel_id(url, setup):
    '''
    channel does not exist
    '''
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'channel_id': 99
    }

    # InputError
    resp = requests.post(url + 'channel/leave', json=payload)
    resp.status_code == 400


def test_channel_leave_not_already_in_channel(url, setup):
    '''
    user is not in the channel
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
        'channel_id': channel_data['channel_id']
    }

    # AccessError
    resp = requests.post(url + 'channel/leave', json=payload)
    resp.status_code == 400


def test_channel_leave_success_all_members(url, setup):
    '''
    successful call for one user to leave the channel
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
    requests.post(url + 'channel/invite', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/leave', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    resp = requests.get(url + 'channel/details', params=payload)

    assert not user_2['u_id'] in resp.json()['owner_members']
    assert not user_2['u_id'] in resp.json()['all_members']

def test_channel_join_invalid_channel_id(url, setup):
    '''
    channel does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'channel_id': 99
    }

    # InputError
    resp = requests.post(url + 'channel/join', json=payload)
    resp.status_code == 400


def test_channel_join_invalid_access(url, setup):
    '''
    user does not have permissions to join the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }

    # AccessError
    resp = requests.post(url + 'channel/join', json=payload)
    resp.status_code == 400


def test_channel_join_as_flockr_owner(url, setup):
    '''
    successful call with user as flockr owner
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    payload = {
        'token': user_2['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    resp = requests.get(url + 'channel/details', params=payload)

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
    }

    assert resp.json() == expected_result


def test_channel_join_success(url, setup):
    '''
    successful call
    '''
    user_1, user_2, user_3 = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    resp = requests.get(url + 'channel/details', params=payload)

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert resp.json() == expected_result

########################################################


def test_channel_addowner_invalid_channel_id(url, setup):
    '''
    channel does not exist
    '''
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'channel_id': 99,
        'u_id': user_2['u_id']
    }

    # InputError
    resp = requests.post(url + 'channel/addowner', json=payload)
    resp.status_code == 400


def test_channel_addowner_invalid_uid(url, setup):
    '''
    uid does not exist
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
        'u_id': 99
    }

    # InputError
    resp = requests.post(url + 'channel/addowner', json=payload)
    resp.status_code == 400


def test_channel_addowner_already_existing_owner(url, setup):
    '''
    the user is already an owner
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
        'u_id': user_1['u_id']
    }

    # InputError
    resp = requests.post(url + 'channel/addowner', json=payload)
    resp.status_code == 400


def test_channel_addowner_self_escalation(url, setup):
    '''
    user attempts to set themselves as owner
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }

    # AccessError
    resp = requests.post(url + 'channel/addowner', json=payload)
    resp.status_code == 400


def test_channel_addowner_not_owner_of_channel(url, setup):
    '''
    user does not have permissions to set other user as owner
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }

    # AccessError
    resp = requests.post(url + 'channel/addowner', json=payload)
    resp.status_code == 400


def test_channel_addowner_success(url, setup):
    '''
    successful call
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/addowner', json=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    requests.post(url + 'channel/addowner', json=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    resp = requests.get(url + 'channel/details', params=payload)

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert resp.json() == expected_result

########################################################


def test_channel_removeowner_invalid_channel_id(url, setup):
    '''
    channel does not exist
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'channel_id': 99,
        'u_id': user_2['u_id']
    }

    # InputError
    resp = requests.post(url + 'channel/removeowner', json=payload)
    resp.status_code == 400


def test_channel_removeowner_not_valid_uid(url, setup):
    '''
    uid is invalid
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': 99
    }

    # InputError
    resp = requests.post(url + 'channel/removeowner', json=payload)
    resp.status_code == 400


def test_channel_removeowner_not_owner_of_channel(url, setup):
    '''
    the user, perms being removed, is not an owner of the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }

    # InputError
    resp = requests.post(url + 'channel/removeowner', json=payload)
    resp.status_code == 400


def test_channel_removeowner_invalid_perm(url, setup):
    '''
    the user, removing perms, is not an owner of the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id']
    }

    # AccessError
    resp = requests.post(url + 'channel/removeowner', json=payload)
    resp.status_code == 400


def test_channel_removeowner_success(url, setup):
    '''
    successful call
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/addowner', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    requests.post(url + 'channel/addowner', json=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/removeowner', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    requests.post(url + 'channel/removeowner', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id']
    }
    requests.post(url + 'channel/removeowner', json=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    resp = requests.get(url + 'channel/details', params=payload)

    expected_result = {
        'name': 'test channel',
        'owner_members': [

        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert resp.json() == expected_result


def test_channel_removeowner_as_flockr_owner(url, setup):
    '''
    successful call with user, removing perms, as flock owner
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    payload = {
        'token': user_2['token'],
        'name': 'test channel',
        'is_public': True
    }
    channel_data = requests.post(url + 'channels/create', json=payload).json()

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', json=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    requests.post(url + 'channel/addowner', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/removeowner', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    requests.post(url + 'channel/removeowner', json=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    resp = requests.get(url + 'channel/details', params=payload)

    expected_result = {
        'name': 'test channel',
        'owner_members': [

        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert resp.json() == expected_result

########################################################
