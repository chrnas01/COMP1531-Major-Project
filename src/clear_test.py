'''
tests for the clear function
'''
import other
import auth
import channels

def test_user_clear_1():
    '''
    test clearing a user
    '''
    auth.auth_register('test0@email.com', 'password', 'name_first0', 'name_last0')
    other.clear()
    assert not bool(other.data['users'])

def test_user_clear_0():
    '''
    test clearing zero users
    '''
    other.clear()
    assert not bool(other.data['users'])

def test_channel_clear_1():
    '''
    test clearing a channel
    '''
    auth.auth_register('test0@email.com', 'password', 'name_first0', 'name_last0')
    channels.channels_create(other.data['users'][0]['token'], 'test_channel', True)
    other.clear()
    assert not bool(other.data['users'])
    assert not bool(other.data['channels'])
