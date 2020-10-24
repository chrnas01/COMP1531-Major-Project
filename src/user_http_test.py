import requests
import json
from echo_http_test import url

def test_user_profile_success(url):
    '''
    Tests that user_profile returns the correct data
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }    
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()
    
    profile_payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=profile_payload).json()
    assert resp == {
        'user': {
            'email': 'jayden@gmail.com',
            'u_id': user_1['u_id'],
            'name_first': 'Jayden',
            'name_last': 'Leung',
            'handle_str': 'jaydenleung',
            }
        }

def test_user_profile_invalid_uid(url):
    '''
    Tests that user_profile throws an InputError with invalid uid
    '''
    requests.delete(url + 'clear')

    #Setup users
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    } 
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()
    
    profile_payload = {
        'token': user_1['token'],
        'u_id': 99,
    }
    resp = requests.get(url + 'user/profile', params=profile_payload).json()    
    
    assert 'code' in resp
    assert resp['code'] == 400

########################################################

def test_user_profile_setname_success(url):
    '''
    Tests that user_profile_setname sets the correct first and last name
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    setname_payload = {
        'token': user_1['token'],
        'name_first': 'changed_first',
        'name_last': 'changed_last',
    }
    requests.put(url + 'user/profile/setname', json=setname_payload).json()

    profile_payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=profile_payload).json()

    assert resp == {
        'user': {
            'email': 'jayden@gmail.com',
            'handle_str': 'jaydenleung',
            'name_first': 'changed_first',
            'name_last': 'changed_last',
            'u_id': user_1['u_id'],
            }
        }

def test_user_profile_firstname_short(url):
    '''
    Tests that user_profile_setname throws InputError when first name is too short
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    setname_payload = {
        'token': user_1['token'],
        'name_first': '',
        'name_last': 'LASTNAME',
    }
    # name_first is now length 0

    resp = requests.put(url + 'user/profile/setname', json=setname_payload).json()
    
    assert 'code' in resp
    assert resp['code'] == 400
    

def test_user_profile_firstname_long(url):
    '''
    Tests that user_profile_setname throws InputError when first name is too long
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    setname_payload = {
        'token': user_1['token'],
        'name_first': 'A'*51,
        'name_last': 'LASTNAME',
    }
    # name_first is now length 51

    resp = requests.put(url + 'user/profile/setname', json=setname_payload).json()
    
    assert 'code' in resp
    assert resp['code'] == 400


def test_user_profile_lastname_short(url):
    '''
    Tests that user_profile_setname throws InputError when last name is too short
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    setname_payload = {
        'token': user_1['token'],
        'name_first': 'FIRSTNAME',
        'name_last': '',
    }
    # name_last is now length 0

    resp = requests.put(url + 'user/profile/setname', json=setname_payload).json()
    
    assert 'code' in resp
    assert resp['code'] == 400


def test_user_profile_lastname_long(url):
    '''
    Tests that user_profile_setname throws InputError when last name is too long
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    setname_payload = {
        'token': user_1['token'],
        'name_first': 'FIRSTNAME',
        'name_last': 'A'*51,
    }
    # name_last is now length 51

    resp = requests.put(url + 'user/profile/setname', json=setname_payload).json()
    
    assert 'code' in resp
    assert resp['code'] == 400


########################################################

def test_user_profile_setemail_success(url):
    '''
    Tests that user_profile_setemail sets the correct email
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    setemail_payload = {
        'token': user_1['token'],
        'email': 'test@gmail.com',
    }
    requests.put(url + 'user/profile/setemail', json=setemail_payload).json()
    
    profile_payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=profile_payload).json()

    assert resp == {
        'user': {
            'email': 'test@gmail.com',
            'u_id': user_1['u_id'],
            'name_first': 'Jayden',
            'name_last': 'Leung',
            'handle_str': 'jaydenleung',
            }
        }

def test_user_profile_setemail_invalid_email(url):
    '''
    Tests that user_profile_setemail throws InputError when email is invalid
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    setemail_payload = {
        'token': user_1['token'],
        'email': 'EMAIL',
    }
    resp = requests.put(url + 'user/profile/setemail', json=setemail_payload).json()
 
    assert 'code' in resp
    assert resp['code'] == 400

def test_user_profile_setemail_used_email(url):
    '''
    Tests that user_profile_setemail throws InputError when email is already used
    '''
    requests.delete(url + 'clear')

    # Setup users   
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung',
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    user_payload = {
        'email': 'Steven@gmail.com',
        'password': 'password',
        'name_first': 'Steven',
        'name_last': 'Luong',
    }
    requests.post(url + 'auth/register', json=user_payload).json()

    setemail_payload = {
        'token': user_1['token'],
        'email': 'Steven@gmail.com',
    }

    resp = requests.put(url + 'user/profile/setemail', json=setemail_payload).json()
 
    assert 'code' in resp
    assert resp['code'] == 400


########################################################

def test_user_profile_sethandle_success(url):
    '''
    Tests that user_profile_sethandle sets the correct handle_str
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    sethandle_payload = {
        'token': user_1['token'],
        'handle_str': 'newhandle',
    }
    requests.put(url + 'user/profile/sethandle', json=sethandle_payload).json()
    
    profile_payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=profile_payload).json()

    assert resp == {
        'user': {
            'email': 'jayden@gmail.com',
            'u_id': user_1['u_id'],
            'name_first': 'Jayden',
            'name_last': 'Leung',
            'handle_str': 'newhandle',
            }
        }

def test_user_profile_sethandle_already_exists(url):
    '''
    Tests that user_profile_sethandle sets the correct handle_str when there are duplicates
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'Steven@gmail.com',
        'password': 'password',
        'name_first': 'Steven',
        'name_last': 'Luong'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    sethandle_payload = {
        'token': user_1['token'],
        'handle_str': 'stevenluong',
    }
    resp = requests.put(url + 'user/profile/sethandle', json=sethandle_payload).json()

    assert 'code' in resp
    assert resp['code'] == 400
    

def test_user_profile_sethandle_short(url):
    '''
    Tests that user_profile_sethandle throws InputError when handle is too short
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'Jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    sethandle_payload = {
        'token': user_1['token'],
        'handle_str': '',
    }
    resp = requests.put(url + 'user/profile/sethandle', json=sethandle_payload).json()

    assert 'code' in resp
    assert resp['code'] == 400


def test_user_profile_sethandle_long(url):
    '''
    Tests that user_profile_sethandle throws InputError when handle is too long
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'Jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()

    sethandle_payload = {
        'token': user_1['token'],
        'handle_str': 'A'*20,
    }
    resp = requests.put(url + 'user/profile/sethandle', json=sethandle_payload).json()

    assert 'code' in resp
    assert resp['code'] == 400

def test_all_users(url):
    '''
    Test to show all users
    '''
    requests.delete(url + 'clear')

    # Setup users
    user_payload = {
        'email': 'Jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=user_payload).json()
    
    resp = requests.get(url + 'users/all', json={'token': user_1['token']}).json()
    
    assert resp == {'users': [{
        'u_id': user_1['u_id'],
        'token': user_1['token'],
        'email': 'Jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung',
        'handle_str': 'jaydenleung',
        'permission_id': 1}]       
    }
