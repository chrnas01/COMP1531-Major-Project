'''
Tests functions in other.py
'''
import pytest
import other
import auth
import message
import channels
import channel
from datetime import datetime, timezone
from error import InputError, AccessError

@pytest.fixture
def setup():
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


def test_admin_userpermission_change_invalid_uid(setup):
    '''
    Changing user permission of u_id that does not exist
    '''
    requests.delete(url + 'clear')

    # Setup pytest
    user_1, _, _ = setup

    payload = {
        'token': user_1['token'],
        'u_id': 99,
        'permission_id': 1
    }
    resp = requests.post(url + 'admin/userpermission/change', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400


def test_admin_userpermission_change_invalid_permission_id(setup):
    '''
    Changing user permission with wrong permission_id
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'u_id': user_2['u_id'],
        'permission_id': 2
    }
    resp = requests.post(url + 'admin/userpermission/change', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400


def test_admin_userpermission_change_unauthorised_user(setup):
    '''
    Changing user permission with wrong unauthorised user
    '''
    # Setup pytest
    _, user_2, user_3 = setup

    payload = {
        'token': user_2['token'],
        'u_id': user_3['u_id'],
        'permission_id': 1
    }
    resp = requests.post(url + 'admin/userpermission/change', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400


def test_admin_userpermission_change_success(setup):
    '''
    Successful admin user permission change
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    payload = {
        'token': user_1['token'],
        'u_id': user_2['u_id'],
        'permission_id': 1
    }
    resp = requests.post(url + 'admin/userpermission/change', json=payload)

    assert is_successful_in_change_permissions(user_1, user_2)
    assert json.loads(resp.text) == {}

################################################################################