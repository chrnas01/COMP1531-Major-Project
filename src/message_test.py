'''
tests for message.py
'''
import pytest
import auth
import channel
import channels
import message
from error import InputError, AccessError
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
    assert other.data['channels'][channel_data['channel_id'] - 1]['messages'] == [{
        'message_id': 1,
        'token': user_1['token'],
        'message': msg
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
    assert other.data['channels'][channel_data['channel_id'] - 1]['messages'] == [{
        'message_id': 1,
        'token': user_1['token'],
        'message': msg
    }]

    assert message.message_send(user_2['token'], channel_data['channel_id'], msg2) == {'message_id': 2}
    assert other.data['channels'][channel_data['channel_id'] - 1]['messages'] == [
        {
        'message_id': 1,
        'token': user_1['token'],
        'message': msg
        },
        {
        'message_id': 2,
        'token': user_2['token'],
        'message': msg2
        }
    ]