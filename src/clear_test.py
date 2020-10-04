import pytest
import error
import other
import auth
import channels

def test_user_clear_1():
    auth.auth_register('test0@email.com', 'password', 'name_first0', 'name_last0')
    other.clear()
    assert bool(other.data['users']) == False

def test_user_clear_0():
    other.clear()
    assert bool(other.data['users']) == False

def test_user_clear_10():
    for counter in range(10):
        email = 'test' + str(counter) + '@email.com'
        firstname = 'name_first' + str(counter)
        lastname = 'name_last' + str(counter)
        auth.auth_register(email, 'password', firstname, lastname)
    other.clear()
    assert bool(other.data['users']) == False

def test_channel_clear_1():
    auth.auth_register('test0@email.com', 'password', 'name_first0', 'name_last0')
    channels.channels_create(other.data['users'][0]['token'], 'test_channel', True)
    other.clear()
    assert bool(other.data['users']) == False
    assert bool(other.data['channels']) == False