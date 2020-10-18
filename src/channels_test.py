'''
tests for channels.py
'''
import pytest
import auth
import channels
import other
from error import InputError

# Tests for channels_list() function.
###################################################################################

def test_channels_list_successful():
    '''
    Successfuly provides a list of all channels that the authorized user is part of:
    '''
    other.clear()
    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Creating a private and a public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)

    # Shouldn't include channel 2 as user1 is not in this channel
    assert channels.channels_list(user1['token']) == {'channels': [
        {
            'channel_name': 'Channel_1',
            'channel_id': channel1['channel_id'],
            'is_public': True,
            'owner_members': [user1['u_id'],],
            'all_members': [user1['u_id'],],
            'messages': []
        },
    ]}

def test_channels_list_successful_two_channels():
    '''
    Successfuly provides a list of all channels that the authorized user is part of:
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')

    # Created a private and a public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)
    channel2 = channels.channels_create(user1['token'], 'Channel_2', False)

    assert channels.channels_listall(user1['token']) == {'channels': [
        {
            'channel_name': 'Channel_1',
            'channel_id': channel1['channel_id'],
            'is_public': True,
            'owner_members': [user1['u_id'],],
            'all_members': [user1['u_id'],],
            'messages': []
        },
        {
            'channel_name': 'Channel_2',
            'channel_id': channel2['channel_id'],
            'is_public': False,
            'owner_members': [user1['u_id'],],
            'all_members': [user1['u_id'],],
            'messages': []
        },
    ]}


def test_channels_list_no_channels():
    '''
    User doesnt belong to any channels
    '''
    other.clear()
    user1 = auth.auth_register('johnsmith@gmail.com', 'password', 'John', 'Smith')

    # User 2 belongs to no channels hence an empty list is returned
    assert channels.channels_list(user1['token']) == {'channels': []}

# Tests for channels_listall() function.
###################################################################################

def test_channels_listall_successful():
    '''
    Successfully provides a list of all channels and their associated details
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    user2 = auth.auth_register('johnsmith@gmail.com', 'password', 'John', 'Smith')

    # Created a private and a public channel
    channel1 = channels.channels_create(user1['token'], 'Channel_1', True)
    channel2 = channels.channels_create(user2['token'], 'Channel_2', False)

    assert channels.channels_listall(user1['token']) == {'channels': [
        {
            'channel_name': 'Channel_1',
            'channel_id': channel1['channel_id'],
            'is_public': True,
            'owner_members': [user1['u_id'],],
            'all_members': [user1['u_id'],],
            'messages': []
        },
        {
            'channel_name': 'Channel_2',
            'channel_id': channel2['channel_id'],
            'is_public': False,
            'owner_members': [user2['u_id'],],
            'all_members': [user2['u_id'],],
            'messages': []
        },
    ]}

def test_channels_listall_no_existing_channels():
    '''
    If there are no existing channels channels_listall() should return an empty list
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    assert channels.channels_listall(user1['token']) == {'channels': []}


# Tests for channels_create() function.
###################################################################################

def test_channels_create_invalid_channel_name1():
    '''
    Public channel name is greater than 20 characters long
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    with pytest.raises(InputError):
        # For Public Channel.
        assert channels.channels_create(
            user1['token'], 'ChannelNameGreaterthan20characters', True)

def test_channels_create_invalid_channel_name2():
    '''
    Private channel name is greater than 20 characters long
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    with pytest.raises(InputError):
        # For Private Channel.
        assert channels.channels_create(
            user1['token'], 'ChannelNameGreaterthan20characters', False)

def test_channels_create_20char_channel_name():
    '''
    Boundary Test: Channel name is exactly 20 characters long
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    assert channels.channels_create(user1['token'], 20*'a', True) == {'channel_id': 1}

def test_channels_create_successful_public():
    '''
    Public channel is successfully created
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    assert channels.channels_create(user1['token'], 'ChannelName', True) == {'channel_id': 1}

def test_channels_create_successful_private():
    '''
    Private channel is successfully created
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    assert channels.channels_create(user1['token'], 'ChannelName', False) == {'channel_id': 1}

def test_channels_create_name_exists():
    '''
    Channel name already exists
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    user2 = auth.auth_register('johnsmith@gmail.com', 'password', 'John', 'Smith')

    channels.channels_create(user1['token'], 'ChannelName', True)
    with pytest.raises(InputError):
        assert channels.channels_create(user2['token'], 'ChannelName', True)

def test_channels_create_nameless_channel():
    '''
    Channel name is not input i.e. trying to make a channel without a name
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    with pytest.raises(InputError):
        assert channels.channels_create(user1['token'], '', True)

def test_channels_create_successful_private_multi():
    '''
    Private channel is successfully created
    '''
    other.clear()

    user1 = auth.auth_register('chris@gmail.com', 'password', 'Chris', 'Nassif')
    assert channels.channels_create(user1['token'], 'ChannelName', False) == {'channel_id': 1}
    assert channels.channels_create(user1['token'], 'ChannelName2', False) == {'channel_id': 2}
    assert channels.channels_create(user1['token'], 'ChannelName3', False) == {'channel_id': 3}