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
from error import InputError, AccessError

################################################################################

def test_auth_login_invalid_email(url):
    '''
    Test to check auth login invalid email
    '''
    other.clear()
    resp = requests.post(url + 'auth/login', params={'email': 'nicholas@gmai.l.com', 'password': 'password'})
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_login_not_registered(url):
    '''
    Test to check auth login invalid email
    '''
    other.clear()
    resp = requests.post(url + 'auth/login', params={'email': 'nicholas@gmail.com', 'password': 'password'})
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_login_incorrect_password(url):
    '''
    Password is not correct
    '''
    other.clear()
    requests.post(url + 'auth/register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'tan'})
    resp = requests.post(url + 'auth/login', params={'email': 'nicholas@gmail.com', 'password': 'notthepassword'})
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

################################################################################

def test_logout_success(url):
    '''
    Check valid
    '''
    pass

################################################################################

def test_auth_register_invalid_email(url):
    '''
    Test to check auth register invalid email
    '''
    other.clear()
    resp = requests.post(url + 'auth/register', params={'email': 'nicholas@gmai.l.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'tan'})
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_used(url):
    '''
    Test to check auth register already used email
    '''
    other.clear()
    requests.post(url + 'auth/register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'tan'})
    resp = requests.post(url + 'auth/register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'tan'})
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_password_too_long(url):
    '''
    Test to check auth register invalid password (length 5)
    '''
    other.clear()
    resp = requests.post(url + 'auth/register', params={'email': 'nicholas@gmail.com', 'password': 'ABCDE', 'name_first': 'nicholas', 'name_last': 'tan'}) # 5 characters password (too short)
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_password_valid(url):
    '''
    Test to check auth register valid password (length 6)
    '''
    pass

################################################################################

# Tests on name_first
def test_auth_register_firstname_short(url):
    '''
    name_first is too short
    '''
    other.clear()
    resp = requests.post(url + 'auth/register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': '', 'name_last': 'tan'})
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_firstname_long(url):
    '''
    name_first is too long
    '''
    other.clear()
    resp = requests.post(url + 'auth/register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'A'*51, 'name_last': 'tan'})
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

################################################################################
# Tests on name_last
def test_auth_register_lastname_short(url):
    '''
    name_last is too short
    '''
    other.clear()
    resp = requests.post(url + 'auth/register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': ''})
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

def test_auth_register_lastname_long(url):
    '''
    name_last is too long
    '''
    other.clear()
    resp = requests.post(url + 'auth/register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'A'*51})
    assert "code" in resp.json()
    assert resp.json()['code'] == 400

