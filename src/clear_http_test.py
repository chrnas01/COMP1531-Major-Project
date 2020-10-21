'''
tests for the http clear function
'''
import other
import auth
import channels
import requests
import json
from echo_http_test import url

def test_http_user_clear_1(url):
    '''
    test clearing a user
    '''
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'tan'
    }
    requests.post(url + 'auth/register', params=payload)
    requests.delete(url + 'clear')
    assert other.is_empty()

def test_http_user_clear_0(url):
    '''
    test clearing zero users
    '''
    requests.delete(url + 'clear')
    assert other.is_empty()

def test_http_channel_clear_1(url):
    '''
    test clearing a channel
    '''
    payload = {
        'email': 'nicholas@gmail.com',
        'password': 'password',
        'name_first': 'nicholas',
        'name_last': 'tan'
    }
    resp = requests.post(url + 'auth/register', params=payload)

    payload = {
        'token': resp.json()['token'],
        'name': 'my_channel',
        'is_public': True
    }
    requests.post(url + 'channels/create', params=payload) 
    
    requests.delete(url + 'clear')
    assert other.is_empty()