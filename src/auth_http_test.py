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

def test_auth_login_incorrect_password():
    '''
    Password is not correct
    '''
    other.clear()
    resp = requests.post(url + 'register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 't'})
    with pytest.raises(InputError):
        resp = requests.post(url + 'login', params={'email': 'nicholas@gmail.com', 'password': 'notthepassword'})

################################################################################
