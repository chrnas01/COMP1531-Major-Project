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
        'is_public': Talse
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

