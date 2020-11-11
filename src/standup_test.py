'''
tests for standup.py
'''

import pytest
import auth
import channels
import standup
import other
from error import InputError, AccessError

# Tests for standup_start() function.
###################################################################################
def test_standup_start_invalid_channel_id():
    '''
    Channel ID is invalid.
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    with pytest.raises(InputError):
        assert standup.standup_start(user1['token'], 321, 60)

def test_standup_start_standup_already_running():
    '''
    Standup already running on this channel.
    '''

    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    standup.standup_start(user1['token'], channel1['channel_id'], 600)

    with pytest.raises(InputError):
        assert standup.standup_start(user1['token'], channel1['channel_id'], 123)

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
        assert standup.standup_active(user1['token'], 321)

def test_standup_active_inactive():
    '''
    Calling standup_active function when there is no standup occuring
    '''

    other.clear()
    

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

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

    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Creating Standup for Channel 1 only
    standup.standup_start(user1['token'], channel1['channel_id'], 600)

    with pytest.raises(AccessError):
        assert standup.standup_send(user2['token'], channel1['channel_id'], 'User not member')



''' 
NOTE:
Write test to include standup twice on same channel
''' 