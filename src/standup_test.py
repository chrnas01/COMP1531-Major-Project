'''
tests for standup.py
'''

import pytest
import time
import auth
import channel
import channels
import standup
import other
from error import InputError, AccessError

# Tests for standup_start() function.
###################################################################################
def test_standup_start_invalid_token():
    '''
    Token is invalid
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    with pytest.raises(AccessError):
        assert standup.standup_start(123, channel1['channel_id'], 60)

def test_standup_start_invalid_channel_id():
    '''
    Channel ID is invalid.
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    with pytest.raises(InputError):
        assert standup.standup_start(user1['token'], 321, 60)

def test_standup_start_already_active1():
    '''
    Standup already running on this channel.
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Creating standup
    standup.standup_start(user1['token'], channel1['channel_id'], 60)

    with pytest.raises(InputError):
        assert standup.standup_start(user1['token'], channel1['channel_id'], 60)

def test_standup_start_already_acive2():
    '''
    Standup already running on this channel. Another user attempts to create a standup
    within the same channel.
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    user2 = auth.auth_register('john@gmail.com', 'password', 'John', 'Smith')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Creating standup
    standup.standup_start(user1['token'], channel1['channel_id'], 60)

    with pytest.raises(InputError):
        assert standup.standup_start(user2['token'], channel1['channel_id'], 60)

def test_standup_start_multiple_standups():
    '''
    Running two subseqent standups 
    '''
    other.clear()

    user1 = user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Creating standup
    standup.standup_start(user1['token'], channel1['channel_id'], 1)
    
    # Interacting in inital standup 
    standup.standup_send(user1['token'], channel1['channel_id'], 'Talking')
    standup.standup_send(user1['token'], channel1['channel_id'], 'in')
    standup.standup_send(user1['token'], channel1['channel_id'], 'First')
    standup.standup_send(user1['token'], channel1['channel_id'], 'Standup')

    # Allowing Standup 1 to finish
    time.sleep(1)

    # Starting second standup
    standup2 = standup.standup_start(user1['token'], channel1['channel_id'], 1)

    # Interacting with second standup 
    standup.standup_send(user1['token'], channel1['channel_id'], 'This is')
    standup.standup_send(user1['token'], channel1['channel_id'], 'standup number 2')

    # Allowing Standup 2 to finish
    time.sleep(1)
    
    # Updating standup status 
    standup.standup_active(user1['token'], channel1['channel_id'])
    
    target = {}
    for target in other.data['standup']:
        if  channel1['channel_id'] == target['channel_id']:
            break
    
    user = {}
    for user in other.data['users']:
        if user['token'] == user1['token']:
            user1_handle_str = user['handle_str']
    
    assert target == {
                     'channel_id': channel1['channel_id'],
                     'time_finish': standup2['time_finish'],
                     'is_active': False,
                     'message': [user1_handle_str + ': ' + 'This is' + '\n', user1_handle_str + ': ' + 'standup number 2' + '\n']
                     }

def test_standup_start_successful():
    '''
    Standup successfully started.
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    assert standup.standup_start(user1['token'], channel1['channel_id'], 600) == {
        'time_finish': other.data['standup'][-1]['time_finish']
    }

# Tests for standup_active() function.
###################################################################################
def test_standup_active_invalid_token():
    '''
    Token is invalid
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Creating standup
    standup.standup_start(user1['token'], channel1['channel_id'], 60)

    with pytest.raises(AccessError):
        assert standup.standup_active(123, channel1['channel_id'])

def test_standup_active_invalid_channel_id():
    '''
    Channel ID is invalid.
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    standup.standup_start(user1['token'], channel1['channel_id'], 600)

    with pytest.raises(InputError):
        assert standup.standup_active(user1['token'], 123)

def test_standup_active_inactive():
    '''
    Calling standup_active function when there is no standup occuring
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Private channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', False)

    assert standup.standup_active(user1['token'], channel1['channel_id']) == {
        'is_active': False,
        'time_finish': None
    }

def test_standup_active_successful():
    '''
    Standup successfully detected and correct finishing time returned
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    standup1 = standup.standup_start(user1['token'], channel1['channel_id'], 600)

    assert standup.standup_active(user1['token'], channel1['channel_id']) == {
        'is_active': True,
        'time_finish': standup1['time_finish']
    }

# Tests for standup_send() function.
###################################################################################
def test_standup_send_invalid_token():
    '''
    Token is invalid
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Creating standup
    standup.standup_start(user1['token'], channel1['channel_id'], 60)

    with pytest.raises(AccessError):
        assert standup.standup_send(123, channel1['channel_id'], 'Hello')

def test_standup_send_invalid_channel_id():
    '''
    Channel ID is invalid.
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Creating Standup
    standup.standup_start(user1['token'], channel1['channel_id'], 600)

    with pytest.raises(InputError):
        assert standup.standup_send(user1['token'], 1234, 'Invalid Channel Test')

def test_standup_send_message_too_long():
    '''
    Message is more than 1000 characters long
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Creating Standup
    standup.standup_start(user1['token'], channel1['channel_id'], 600)

    with pytest.raises(InputError):
        assert standup.standup_send(user1['token'], channel1['channel_id'], 1000*'msg too long')

def test_standup_send_message_1000char():
    '''
    Boundary Test: Message is exactly 1000 characters long
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Creating Standup
    standup.standup_start(user1['token'], channel1['channel_id'], 600)

    assert standup.standup_send(user1['token'], channel1['channel_id'], 1000*'A') == {}

    # Finding channel
    standup_channel = {}
    for standup_channel in other.data['standup']:
        if standup_channel['channel_id'] == channel1['channel_id']:
            break

    # Finding user
    user = {}
    for user in other.data['users']:
        if user['token'] == user1['token']:
            break

    assert standup_channel['message'] == [user['handle_str'] + ': ' + 1000*'A' + '\n']

def test_standup_send_no_active_standup():
    '''
    An active standup is not currently running in this channel
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public and Private channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)
    channel2 = channels.channels_create(user1['token'], 'Channel_2', False)

    # Creating Standup for Channel 1 only
    standup.standup_start(user1['token'], channel1['channel_id'], 600)

    with pytest.raises(InputError):
        assert standup.standup_send(user1['token'], channel2['channel_id'], 'No active standup')

def test_standup_send_member_not_user():
    '''
    The authorised user is not a memeber of the channel that the messasge is within
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    user2 = auth.auth_register('john@gmail.com', 'password', 'John', 'Smith')

    # Creating a Private channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', False)

    # Creating Standup for Channel 1 only
    standup.standup_start(user1['token'], channel1['channel_id'], 600)

    with pytest.raises(AccessError):
        assert standup.standup_send(user2['token'], channel1['channel_id'], 'User not member')


def test_standup_send_multiple_users():
    '''
    Users can successfully send messages
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    user2 = auth.auth_register('john@gmail.com', 'password', 'John', 'Smith')
    user3 = auth.auth_register('bruce@gmail.com', 'password', 'Bruce', 'Lee')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Users join channel
    channel.channel_join(user2['token'], channel1['channel_id'])
    channel.channel_join(user3['token'], channel1['channel_id'])

    # Creating Standup
    standup.standup_start(user1['token'], channel1['channel_id'], 60)

    assert standup.standup_send(user1['token'], channel1['channel_id'], 'User 1 Speaking') == {}
    assert standup.standup_send(user2['token'], channel1['channel_id'], 'User 2 Speaking') == {}
    assert standup.standup_send(user3['token'], channel1['channel_id'], 'User 3 Speaking') == {}

    # Finding channel
    standup_channel = {}
    for standup_channel in other.data['standup']:
        if standup_channel['channel_id'] == channel1['channel_id']:
            break

    # Finding user
    user = {}
    for user in other.data['users']:
        if user['token'] == user1['token']:
            user1_handle_str = user['handle_str']
        if user['token'] == user2['token']:
            user2_handle_str = user['handle_str']
        if user['token'] == user3['token']:
            user3_handle_str = user['handle_str']

    assert standup_channel['message'] == [user1_handle_str + ': ' + 'User 1 Speaking' + '\n',
                                          user2_handle_str + ': ' + 'User 2 Speaking' + '\n',
                                          user3_handle_str + ': ' + 'User 3 Speaking' + '\n'
                                         ]
