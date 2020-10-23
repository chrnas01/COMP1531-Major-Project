'''
Test file for auth http
'''
import json
import requests
import other
from echo_http_test import url

################################################################################
def test_auth_login_invalid_email(url):
    '''
    Test to check auth login invalid email
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmai.l.com',
        'password': 'password'
    }
    resp = requests.post(url + 'auth/login', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_login_not_registered(url):
    '''
    Test to check auth login invalid email
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password'
    }
    resp = requests.post(url + 'auth/login', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_login_incorrect_password(url):
    '''
    Password is not correct
    '''
    requests.delete(url + 'clear')

    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'tan'
    }
    requests.post(url + 'auth/register', json=payload)

    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'notthepassword'
    }
    resp = requests.post(url + 'auth/login', json=payload)

    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_valid_login(url):
    '''
    Check valid
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'tan'
    }
    requests.post(url + 'auth/register', json=payload)

    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password'
    }
    resp = requests.post(url + 'auth/login', json=payload)
    assert json.loads(resp.text) == {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}

################################################################################

def test_logout_success(url):
    '''
    Check valid
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'tan'
    }
    requests.post(url + 'auth/register', json=payload)

    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password'
    }
    resp = requests.post(url + 'auth/login', json=payload)
    
    payload = {
        'token': resp.json()['token']
    }
    resp = requests.post(url + 'auth/logout', json=payload)
    assert json.loads(resp.text) == {'is_success': True}

def test_auth_unsuccessful_logout(url):
    '''
    Check logout was unsuccessful
    '''
    payload = {
        'token': 'this_token_does_not_exist',
    }
    resp = requests.post(url + 'auth/logout', json=payload)
    assert json.loads(resp.text) == {'is_success': False}

################################################################################

def test_auth_register_invalid_email(url):
    '''
    Test to check auth register invalid email
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmai.l.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'tan'
    }
    resp = requests.post(url + 'auth/register', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_used(url):
    '''
    Test to check auth register already used email
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'tan'
    }
    requests.post(url + 'auth/register', json=payload)

    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'tan'
    }
    resp = requests.post(url + 'auth/register', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_password_too_long(url):
    '''
    Test to check auth register invalid password (length 5)
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'ABCDE',
        'name_first': 'nicholas',
        'name_last': 'tan'
    }
    resp = requests.post(url + 'auth/register', json=payload) # 5 characters password (too short)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_password_valid(url):
    '''
    Test to check auth register valid password (length 6)
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'ABCDEF',
        'name_first': 'nicholas',
        'name_last': 'tan'
    }
    resp = requests.post(url + 'auth/register', json=payload) # 6 characters password (valid)
    assert json.loads(resp.text) == {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}

################################################################################

# Tests on name_first
def test_auth_register_firstname_short(url):
    '''
    name_first is too short
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': '',
        'name_last': 'tan'
    }
    resp = requests.post(url + 'auth/register', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_firstname_long(url):
    '''
    name_first is too long
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'A'*51,
        'name_last': 'tan'
    }
    resp = requests.post(url + 'auth/register', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_firstname_valid1(url):
    '''
    name_first is of valid length
    '''
    requests.delete(url + 'clear')
    # name_first is length 1
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'A',
        'name_last': 'tan'
    }
    resp = requests.post(url + 'auth/register', json=payload)
    assert json.loads(resp.text) == {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}

def test_auth_register_firstname_valid2(url):
    '''
    name_first is exactly the character limit
    '''
    requests.delete(url + 'clear')
    # name_first is length 50
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'A'*50,
        'name_last': 'tan'
    }
    resp = requests.post(url + 'auth/register', json=payload)
    assert json.loads(resp.text) == {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}

################################################################################
# Tests on name_last
def test_auth_register_lastname_short(url):
    '''
    name_last is too short
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': ''
    }
    resp = requests.post(url + 'auth/register', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_lastname_long(url):
    '''
    name_last is too long
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'A'*51
    }
    resp = requests.post(url + 'auth/register', json=payload)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_lastname_valid1(url):
    '''
    name_last is of valid length
    '''
    requests.delete(url + 'clear')
    # name_last is length 1
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'A'
    }
    resp = requests.post(url + 'auth/register', json=payload)
    assert json.loads(resp.text) == {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}

def test_auth_register_lastname_valid2(url):
    '''
    name_last is of valid length
    '''
    requests.delete(url + 'clear')
    # name_last is length 50
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'A'*50
    }
    resp = requests.post(url + 'auth/register', json=payload)
    assert json.loads(resp.text) == {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}

################################################################################
# Tests for handle_str
def test_http_handle_str1(url):
    '''
    testing that the handle string randomisation is working
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'EMAIL@gmail.com',
        'password': 'WORDSS',
        'name_first': 'FIRSTNAME',
        'name_last': 'LASTNAME'
    }
    requests.post(url + 'auth/register', json=payload)

    payload = {
        'email': 'EMAIL2@gmail.com',
        'password': 'WORDSS',
        'name_first': 'FIRSTNAME',
        'name_last': 'LASTNAME'
    }
    requests.post(url + 'auth/register', json=payload)

    resp = requests.get(url + 'other/show/handle_str')
    assert json.loads(resp.text) == ['firstnamelastname', 'firstnamelastname2']

def test_http_handle_str20char(url):
    '''
    testing that the handle string randomisation is working for names longer
    than 20 characters
    '''
    requests.delete(url + 'clear')
    payload = {
        'email': 'EMAIL2@gmail.com',
        'password': 'WORDSS',
        'name_first': 'twentycharacters',
        'name_last': 'isthisname'
    }
    requests.post(url + 'auth/register', json=payload)

    payload = {
        'email': 'EMAIL@gmail.com',
        'password': 'WORDSS',
        'name_first': 'twentycharacters',
        'name_last': 'isthisname'
    }
    requests.post(url + 'auth/register', json=payload)

    resp = requests.get(url + 'other/show/handle_str')
    assert json.loads(resp.text) == ['twentycharactersisth', 'twentycharactersist2']
