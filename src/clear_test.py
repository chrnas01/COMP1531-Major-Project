import pytest
import error
import other
import auth
import channels

def test_user_clear_1():
    auth.auth_register('test0@email.com', 'password', 'name_first0', 'name_last0')
    other.clear()
    assert bool(auth.all_users) == False

def test_user_clear_0():
    other.clear()
    assert bool(auth.all_users) == False

def test_user_clear_10():
    for counter in range(10):
        auth.auth_register('test' + str(counter) + '@email.com', 'password', 'name_first' + str(counter), 'name_last' + str(counter))
    other.clear()
    assert bool(auth.all_users) == False

def test_channel_clear_1():
    auth.auth_register('test0@email.com', 'password', 'name_first0', 'name_last0')
    channels.channels_create(auth.all_users[0]['token'], 'test_channel', True)
    other.clear()
    assert bool(auth.all_users) == False
    assert bool(channels.data) == False