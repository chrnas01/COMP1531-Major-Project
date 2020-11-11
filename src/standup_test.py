'''
tests for standup.py 
''' 
import auth
import channels
import pytest
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
    standup.standup_data.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    with pytest.raises(InputError):
        assert standup.standup_start(user1['token'], 321, 60)

def test_standup_start_standup_already_running():
    '''
    Standup already running on this channel. 
    '''

    other.clear()
    standup.standup_data.clear()

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
    standup.standup_data.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a Public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    assert standup.standup_start(user1['token'], channel1['channel_id'], 600) == {'time_finish': standup.standup_data[-1]['time_finish']}


# Tests for standup_active() function.
###################################################################################


# Tests for standup_send() function.
###################################################################################



