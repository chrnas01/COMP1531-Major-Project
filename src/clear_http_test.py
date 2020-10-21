'''
tests for the http clear function
'''
import other
import auth
import channels

def test_http_user_clear_1():
    '''
    test clearing a user
    '''
    other.clear()
    requests.post(url + 'auth/register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'tan'})
    assert other.is_empty()

def test_http_user_clear_0():
    '''
    test clearing zero users
    '''
    other.clear()
    assert other.is_empty()

def test_http_channel_clear_1():
    '''
    test clearing a channel
    '''
    other.clear()
    resp = requests.post(url + 'auth/register', params={'email': 'nicholas@gmail.com', 'password': 'password', 'name_first': 'nicholas', 'name_last': 'tan'})
    requests.post(url + 'channels/create', params={'token': json.loads(resp.text)['token'], 'name': 'my_channel', 'is_public': True)    
    assert other.is_empty()
    