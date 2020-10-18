'''
tests for message.py
'''
import pytest
import auth
import channel
import channels
import message
from error import InputError, AccessError
from datetime import datetime, timezone
import other

########################################################

@pytest.fixture
def setup():
    '''
    resets user data for each test
    '''
    # Clear database
    other.clear()

    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
    user_2 = auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong')
    user_3 = auth.auth_register('sam@gmail.com', 'password', 'Sam', 'He')

    return (user_1, user_2, user_3)

########################################################

def test_invalid_user(setup):
    '''
    sending message when not part of the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = 'test'

    with pytest.raises(AccessError):
        assert message.message_send(user_2['token'], channel_data['channel_id'], msg)

def test_invalid_message(setup):
    '''
    sending message that is too long
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = ''
    for i in range(1001):
        msg += 'a'

    with pytest.raises(InputError):
        assert message.message_send(user_1['token'], channel_data['channel_id'], msg)

def test_valid_message(setup):
    '''
    sending valid message
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = 'test'

    assert message.message_send(user_1['token'], channel_data['channel_id'], msg) == {'message_id': 1}
    assert other.data['messages'] == [{
        'message_id': 1,
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id'],
        'message': msg,
        'time_created': int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    }]

def test_valid_message_multi(setup):
    '''
    sending 2 valid messages
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = 'test'
    msg2 = 'test2'

    assert message.message_send(user_1['token'], channel_data['channel_id'], msg) == {'message_id': 1}
    assert other.data['messages'] == [{
        'message_id': 1,
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id'],
        'message': msg,
        'time_created': int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    }]

    assert message.message_send(user_2['token'], channel_data['channel_id'], msg2) == {'message_id': 2}
    assert other.data['messages'] == [
        {
        'message_id': 1,
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id'],
        'message': msg,
        'time_created': int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        },
        {
        'message_id': 2,
        'channel_id': channel_data['channel_id'],
        'u_id': user_2['u_id'],
        'message': msg2,
        'time_created': int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        }
    ]

def test_message_remove_nonexistent(setup):
    '''
    removing a message which doesn't exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    channels.channels_create(user_1['token'], 'test channel', False)

    with pytest.raises(InputError):
        assert message.message_remove(user_1['token'], 1)

def test_message_remove_other_user(setup):
    '''
    removing a message sent by another user
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = 'test'

    message.message_send(user_2['token'], channel_data['channel_id'], msg)
    message.message_send(user_2['token'], channel_data['channel_id'], msg)

    with pytest.raises(AccessError):
        assert message.message_remove(user_1['token'], 1)

def test_message_remove_no_perm(setup):
    '''
    removing a message sent by self but user is not an owner
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = 'test'

    message.message_send(user_2['token'], channel_data['channel_id'], msg)
    message.message_send(user_2['token'], channel_data['channel_id'], msg)

    with pytest.raises(AccessError):
        assert message.message_remove(user_2['token'], 1)

def test_message_remove_valid(setup):
    '''
    removing a valid message
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = 'test'

    message.message_send(user_1['token'], channel_data['channel_id'], msg)
    message.message_send(user_1['token'], channel_data['channel_id'], msg)

    message.message_remove(user_1['token'], 1)

    assert other.data['messages'] == [
        {
        'message_id': 2,
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id'],
        'message': msg,
        'time_created': int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        }
    ]

def test_message_edit_other_user(setup):
    '''
    editing a message sent by another user
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = 'test'

    message.message_send(user_2['token'], channel_data['channel_id'], msg)
    message.message_send(user_2['token'], channel_data['channel_id'], msg)

    with pytest.raises(AccessError):
        assert message.message_edit(user_1['token'], 1, 'tset')

def test_message_edit_other_no_perm(setup):
    '''
    editing a message sent by self but user is not an owner
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = 'test'

    message.message_send(user_2['token'], channel_data['channel_id'], msg)
    message.message_send(user_2['token'], channel_data['channel_id'], msg)

    with pytest.raises(AccessError):
        assert message.message_edit(user_2['token'], 1, 'tset')

def test_message_edit_valid(setup):
    '''
    editing a valid message
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = 'test'

    message.message_send(user_1['token'], channel_data['channel_id'], msg)
    message.message_send(user_1['token'], channel_data['channel_id'], msg)

    message.message_edit(user_1['token'], 1, 'tset')

    assert other.data['messages'] == [
        {
        'message_id': 1,
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id'],
        'message': 'tset',
        'time_created': int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        },
        {
        'message_id': 2,
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id'],
        'message': msg,
        'time_created': int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        }
    ]

def test_message_edit_valid_remove(setup):
    '''
    editing a valid message into an empty string
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = 'test'

    message.message_send(user_1['token'], channel_data['channel_id'], msg)
    message.message_send(user_1['token'], channel_data['channel_id'], msg)

    message.message_edit(user_1['token'], 1, '')

    assert other.data['messages'] == [
        {
        'message_id': 2,
        'channel_id': channel_data['channel_id'],
        'u_id': user_1['u_id'],
        'message': msg,
        'time_created': int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        }
    ]