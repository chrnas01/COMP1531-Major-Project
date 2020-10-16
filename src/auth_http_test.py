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

################################################################################

def test_auth_login_invalid_email(url):
    '''
    Test to check auth login invalid email
    '''
    other.clear()
    with pytest.raises(InputError):
        resp = requests.post(url + 'login', params={'email': 'nicholas@gmai.l.com', 'password': 'password'})
    
def test_auth_login_not_registered(url):
    '''
    Test to check auth login invalid email
    '''
    other.clear()
    with pytest.raises(InputError):
        resp = requests.post(url + 'login', params={'email': 'nicholas@gmail.com', 'password': 'password'})

def test_auth_login_incorrect_password(url):
    '''
    Password is not correct
    '''
    other.clear()
    resp = requests.post(url + 'register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'tan'})
    with pytest.raises(InputError):
        resp = requests.post(url + 'login', params={'email': 'nicholas@gmail.com', 'password': 'notthepassword'})

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
    with pytest.raises(InputError):
        resp = requests.post(url + 'register', params={'email': 'nicholas@gmai.l.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'tan'})
    
def test_auth_register_used(url):
    '''
    Test to check auth register already used email
    '''
    other.clear()
    requests.post(url + 'register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'tan'})
    with pytest.raises(InputError):
        resp = requests.post(url + 'register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'tan'})

def test_auth_register_password_too_long(url):
    '''
    Test to check auth register invalid password (length 5)
    '''
    other.clear()
    with pytest.raises(InputError):
        resp = requests.post(url + 'register', params={'email': 'nicholas@gmail.com', 'password': 'ABCDE', 'name_first': 'nicholas', 'name_last': 'tan'}) # 5 characters password (too short)

def test_auth_register_password_valid(url):
    '''
    Test to check auth register valid password (length 6)
    '''
    pass

