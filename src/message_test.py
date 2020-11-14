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
        msg += str(i)

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

    assert message.message_send(
            user_1['token'], channel_data['channel_id'], msg) == {'message_id': 1}
    
    result = other.get_messages()
    assert result == {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': msg,
                'time_created': result['messages'][0]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            }
        ]
    }

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

    assert message.message_send(
            user_1['token'], channel_data['channel_id'], msg) == {'message_id': 1}

    result = other.get_messages()
    assert result == {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': msg,
                'time_created': result['messages'][0]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            }
        ]
    }

    assert message.message_send(
            user_2['token'], channel_data['channel_id'], msg2) == {'message_id': 2}
    
    result = other.get_messages()
    assert result == {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': msg,
                'time_created': result['messages'][0]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            },
            {
                'message_id': 2,
                'channel_id': channel_data['channel_id'],
                'u_id': user_2['u_id'],
                'message': msg2,
                'time_created': result['messages'][1]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            }
        ]
    }

def test_message_remove_nonexistent(setup):
    '''
    removing a message which doesn't exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    message.message_send(user_1['token'], channel_data['channel_id'], 'msg')

    with pytest.raises(InputError):
        assert message.message_remove(user_1['token'], 2)

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
    channel.channel_addowner(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = 'test'

    message.message_send(user_2['token'], channel_data['channel_id'], msg)
    message.message_send(user_2['token'], channel_data['channel_id'], msg)

    message.message_remove(user_2['token'], 1)

    result = other.get_messages()

    assert result == {
        'messages': [
            {
                'message_id': 2,
                'channel_id': channel_data['channel_id'],
                'u_id': user_2['u_id'],
                'message': msg,
                'time_created': result['messages'][0]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            }
        ]
    }

########################################################

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
    channel.channel_addowner(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = 'test'

    message.message_send(user_2['token'], channel_data['channel_id'], msg)
    message.message_send(user_2['token'], channel_data['channel_id'], msg)

    message.message_edit(user_2['token'], 1, 'tset')

    result = other.get_messages()
    assert result == {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_2['u_id'],
                'message': 'tset',
                'time_created': result['messages'][0]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            },
            {
                'message_id': 2,
                'channel_id': channel_data['channel_id'],
                'u_id': user_2['u_id'],
                'message': msg,
                'time_created': result['messages'][1]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            }
        ]
    }

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

    result = other.get_messages()
    assert result == {
        'messages': [
            {
                'message_id': 2,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': msg,
                'time_created': result['messages'][0]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            }
        ]
    }

########################################################

def test_send_later_invalid_channel(setup):
    '''
    sending a message later to an invalid channel
    '''
    # Setup pytest
    user_1, _, _ = setup

    channels.channels_create(user_1['token'], 'test channel', False)
    msg = 'test'

    with pytest.raises(InputError):
        assert message.message_send_later(user_1['token'], 99, msg,
                (int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 5))

def test_send_later_invalid_message(setup):
    '''
    sending message later that is too long
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = ''
    for i in range(1001):
        msg += str(i)

    with pytest.raises(InputError):
        assert message.message_send_later(user_1['token'], channel_data['channel_id'], msg,
                (int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 5))

def test_send_later_invalid_time(setup):
    '''
    sending message later at time in the past
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = 'test'

    with pytest.raises(InputError):
        assert message.message_send_later(user_1['token'], channel_data['channel_id'], msg,
                (int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) - 5))

def test_send_later_invalid_access(setup):
    '''
    sending message later when user has not joined the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = 'test'

    with pytest.raises(AccessError):
        assert message.message_send_later(user_2['token'], channel_data['channel_id'], msg,
                (int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 5))

def test_send_later_valid(setup):
    '''
    sending message later
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = 'test'
    time = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 5

    message.message_send_later(user_1['token'], channel_data['channel_id'], msg, time)

    result = other.get_messages()

    assert result == {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': msg,
                'time_created': time,
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            }
        ]
    }

########################################################

def test_react_invalid_message(setup):
    '''
    reacting to a message that is in a channel the user is not a part of
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channels.channels_create(user_2['token'], 'test channel 2', False)
    message.message_send(user_1['token'], channel_data['channel_id'], 'test')

    with pytest.raises(InputError):
        assert message.message_react(user_2['token'], channel_data['channel_id'], 1)

def test_react_invalid_react(setup):
    '''
    reacting to a message with a react that doesn't exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')

    with pytest.raises(InputError):
        assert message.message_react(user_1['token'], msg['message_id'], 99)

def test_react_already_reacted(setup):
    '''
    reacting to a message that you have already reacted to
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')
    message.message_react(user_1['token'], msg['message_id'], 1)

    with pytest.raises(InputError):
        assert message.message_react(user_1['token'], msg['message_id'], 1)

def test_react_valid(setup):
    '''
    reacting to a message
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')
    message.message_react(user_1['token'], msg['message_id'], 1)

    result = other.get_messages()

    assert result == {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'test',
                'time_created': result['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [user_1['u_id']],
                    'is_this_user_reacted': True
                }],
                'is_pinned': False
            }
        ]
    }

########################################################

def test_unreact_invalid_message(setup):
    '''
    reacting to a message that is in a channel the user is not a part of
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channels.channels_create(user_2['token'], 'test channel 2', False)
    message.message_send(user_1['token'], channel_data['channel_id'], 'test')

    with pytest.raises(InputError):
        assert message.message_unreact(user_2['token'], channel_data['channel_id'], 1)

def test_unreact_invalid_react(setup):
    '''
    unreacting to a message with a react that doesn't exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')

    with pytest.raises(InputError):
        assert message.message_unreact(user_1['token'], msg['message_id'], 99)

def test_unreact_already_unreacted(setup):
    '''
    unreacting to a message that you have not reacted to
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')

    with pytest.raises(InputError):
        assert message.message_unreact(user_1['token'], msg['message_id'], 1)

def test_unreact_valid(setup):
    '''
    unreacting to a message
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')
    message.message_react(user_1['token'], msg['message_id'], 1)
    message.message_unreact(user_1['token'], msg['message_id'], 1)

    result = other.get_messages()

    assert result == {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'test',
                'time_created': result['messages'][0]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            }
        ]
    }

########################################################

def test_pin_invalid_message(setup):
    '''
    pinning a message that does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    message.message_send(user_1['token'], channel_data['channel_id'], 'test')

    with pytest.raises(InputError):
        assert message.message_pin(user_1['token'], 99)

def test_pin_invalid_channel(setup):
    '''
    pinning a message that is in a channel the user is not a part of
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channels.channels_create(user_2['token'], 'test channel 2', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')

    with pytest.raises(AccessError):
        assert message.message_pin(user_2['token'], msg['message_id'])

def test_pin_already_pinned(setup):
    '''
    pinning a message that is already pinned
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')
    message.message_pin(user_1['token'], msg['message_id'])

    with pytest.raises(InputError):
        assert message.message_pin(user_1['token'], msg['message_id'])

def test_pin_invalid_perms(setup):
    '''
    pinning a message when you are not an owner
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')

    with pytest.raises(AccessError):
        assert message.message_pin(user_2['token'], msg['message_id'])

def test_pin_valid(setup):
    '''
    pinning to a message
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')
    message.message_pin(user_1['token'], msg['message_id'])

    result = other.get_messages()

    assert result == {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'test',
                'time_created': result['messages'][0]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': True
            }
        ]
    }

########################################################

def test_unpin_invalid_message(setup):
    '''
    unpinning a message that does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    message.message_send(user_1['token'], channel_data['channel_id'], 'test')

    with pytest.raises(InputError):
        assert message.message_unpin(user_1['token'], 99)

def test_unpin_invalid_channel(setup):
    '''
    unpinning a message that is in a channel the user is not a part of
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channels.channels_create(user_2['token'], 'test channel 2', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')
    message.message_pin(user_1['token'], msg['message_id'])

    with pytest.raises(AccessError):
        assert message.message_unpin(user_2['token'], msg['message_id'])

def test_unpin_already_unpinned(setup):
    '''
    unpinning a message that is not pinned
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')

    with pytest.raises(InputError):
        assert message.message_unpin(user_1['token'], msg['message_id'])

def test_unpin_invalid_perms(setup):
    '''
    unpinning a message when you are not an owner
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')
    message.message_pin(user_1['token'], msg['message_id'])

    with pytest.raises(AccessError):
        assert message.message_unpin(user_2['token'], msg['message_id'])

def test_unpin_valid(setup):
    '''
    pinning to a message
    '''
    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    msg = message.message_send(user_1['token'], channel_data['channel_id'], 'test')
    message.message_pin(user_1['token'], msg['message_id'])
    message.message_unpin(user_1['token'], msg['message_id'])

    result = other.get_messages()

    assert result == {
        'messages': [
            {
                'message_id': 1,
                'channel_id': channel_data['channel_id'],
                'u_id': user_1['u_id'],
                'message': 'test',
                'time_created': result['messages'][0]['time_created'],
                'reacts': [
                    {
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    },
                    {
                        'react_id': 2,
                        'u_ids': [],
                        'is_this_user_reacted': False
                        },
                    {
                        'react_id': 3,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                'is_pinned': False
            }
        ]
    }

########################################################

def test_invalid_token(setup):
    '''
    Checking that the invalid token checks are working
    '''

    # Setup pytest
    user_1, _, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', True)
    message.message_send(user_1['token'], channel_data['channel_id'], 'msg')

    with pytest.raises(AccessError):
        assert message.message_send('invalid-token', channel_data['channel_id'], 'test')
    
    with pytest.raises(AccessError):
        assert message.message_remove('invalid-token', 1)
    
    with pytest.raises(AccessError):
        assert message.message_edit('invalid-token', 1, 'test')
    
    with pytest.raises(AccessError):
        assert message.message_send_later('invalid-token', 1, 'test',
                int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 5)
    
    with pytest.raises(AccessError):
        assert message.message_react('invalid-token', 1, 1)

    with pytest.raises(AccessError):
        assert message.message_unreact('invalid-token', 1, 1)
    
    with pytest.raises(AccessError):
        assert message.message_pin('invalid-token', 1)
    
    with pytest.raises(AccessError):
        assert message.message_unpin('invalid-token', 1)