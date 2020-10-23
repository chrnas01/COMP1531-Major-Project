'''
Tests functions in other.py
'''
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
        'permission_id': 2
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

###############################################################################