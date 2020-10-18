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


# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


@pytest.fixture
def setup():
    '''
    Pytest fixture used to setup users
    '''
    other.clear()

    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user1 = requests.post(url + 'register', params=payload)

    payload = {
        'email': 'steven@gmail.com',
        'password': 'password',
        'name_first': 'Steven',
        'name_last': 'Luong'
    }
    user2 = requests.post(url + 'register', params=payload)

    payload = {
        'email': 'sam@gmail.com',
        'password': 'password',
        'name_first': 'Sam',
        'name_last': 'He'
    }
    user3 = requests.post(url + 'register', params=payload)

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

    with pytest.raises(InputError):
        requests.post(url + 'channel/invite', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': 99
    }

    with pytest.raises(InputError):
        requests.post(url + 'channel/invite', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    with pytest.raises(AccessError):
        requests.post(url + 'channel/invite', params=payload)


def test_channel_invite_success(url, setup):
    '''
    channel invite success
    '''

    user_1, user_2, user_3 = setup

    payload = {
        'token': user_1['token'],
        'name': 'test channel',
        'is_public': False
    }
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/invite', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    channel_details = request.get(url + 'channel/details', params=payload)

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

    assert channel_details == expected_result

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

    with pytest.raises(InputError):
        request.get(url + 'channel/details', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }

    with pytest.raises(AccessError):
        request.get(url + 'channel/details', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/invite', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    result = request.get(url + 'channel/details', params=payload)

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

    assert result == expected_result


########################################################

# channel messages

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

    with pytest.raises(InputError):
        requests.post(url + 'channel/leave', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }

    with pytest.raises(AccessError):
        requests.post(url + 'channel/leave', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/invite', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/leave', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    result = request.get(url + 'channel/details', params=payload)

    assert not user_2['u_id'] in result['owner_members']
    assert not user_2['u_id'] in result['all_members']

# def test_channel_leave_empty_channel(url, setup):
#     '''
#     successful call for both users to leave the channel
#     '''
#     user_1, user_2, _ = setup

#     payload = {
#         'token': user_1['token'],
#         'name': 'test channel',
#         'is_public': False
#     }
#     channel_data = requests.post(url + 'channels/create', params=payload)

#     payload = {
#         'token': user_1['token'],
#         'channel_id': channel_data['channel_id'],
#         'u_id': user_2['u_id']
#     }
#     requests.post(url + 'channel/invite', params=payload)


#     payload = {
#         'token': user_2['token'],
#         'channel_id': channel_data['channel_id']
#     }
#     requests.post(url + 'channel/leave', params=payload)


#     payload = {
#         'token': user_1['token'],
#         'channel_id': channel_data['channel_id']
#     }
#     requests.post(url + 'channel/leave', params=payload)


#     assert not user_1['u_id'] in other.data['channels'][channel_data['channel_id'] - 1][
#         'all_members']
#     assert not user_2['u_id'] in other.data['channels'][channel_data['channel_id'] - 1][
#         'all_members']

########################################################

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

    with pytest.raises(InputError):
        requests.post(url + 'channel/join', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }

    with pytest.raises(AccessError):
        requests.post(url + 'channel/join', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    result = request.get(url + 'channel/details', params=payload)

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

    assert result == expected_result


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    result = request.get(url + 'channel/details', params=payload)

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

    assert result == expected_result

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
    requests.post(url + 'channel/addowner', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': 99
    }

    with pytest.raises(InputError):
        requests.post(url + 'channel/addowner', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id']
    }

    with pytest.raises(InputError):
        requests.post(url + 'channel/addowner', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }

    with pytest.raises(AccessError):
        requests.post(url + 'channel/addowner', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }

    with pytest.raises(AccessError):
        requests.post(url + 'channel/addowner', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/addowner', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    requests.post(url + 'channel/addowner', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    result = request.get(url + 'channel/details', params=payload)

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

    assert result == expected_result

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

    with pytest.raises(InputError):
        requests.post(url + 'channel/removeowner', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': 99
    }

    with pytest.raises(InputError):
        requests.post(url + 'channel/removeowner', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }

    with pytest.raises(InputError):
        requests.post(url + 'channel/removeowner', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id']
    }

    with pytest.raises(AccessError):
        requests.post(url + 'channel/removeowner', params=payload)


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/addowner', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    requests.post(url + 'channel/addowner', params=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/removeowner', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    requests.post(url + 'channel/removeowner', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id']
    }
    requests.post(url + 'channel/removeowner', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id']
    }
    result = request.get(url + 'channel/details', params=payload)

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

    assert result == expected_result


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
    channel_data = requests.post(url + 'channels/create', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_3['token'],
        'channel_id': channel_data['channel_id']
    }
    requests.post(url + 'channel/join', params=payload)

    payload = {
        'token': user_2['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    requests.post(url + 'channel/addowner', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id']
    }
    requests.post(url + 'channel/removeowner', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user_3['u_id']
    }
    requests.post(url + 'channel/removeowner', params=payload)

    payload = {
        'token': user_1['token'],
        'channel_id': channel_data['channel_id']
    }
    result = request.get(url + 'channel/details', params=payload)

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

    assert result == expected_result

########################################################
