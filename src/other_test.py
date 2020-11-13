'''
Tests functions in other.py
'''
import pytest
import other
import auth
import message
import channels
import channel
from datetime import datetime, timezone
from error import InputError, AccessError
 
 
@pytest.fixture
def setup():
    '''
    Resets user data for each test
    '''
    # Clear database
    other.clear()
 
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung')  # Flockr Owner
    user_2 = auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong')
    user_3 = auth.auth_register('sam@gmail.com', 'password', 'Sam', 'He')
 
    return (user_1, user_2, user_3)
 
################################################################################
 
 
def test_admin_userpermission_change_invalid_uid(setup):
    '''
    Changing user permission of u_id that does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup
 
    with pytest.raises(InputError):
        assert other.admin_userpermission_change(user_1['token'], 99, 1)
 
 
def test_admin_userpermission_change_invalid_permission_id(setup):
    '''
    Changing user permission with wrong permission_id
    '''
    # Setup pytest
    user_1, user_2, _ = setup
 
    with pytest.raises(InputError):
        assert other.admin_userpermission_change(user_1['token'], user_2['u_id'], 0)
 
 
def test_admin_userpermission_change_unauthorised_user(setup):
    '''
    Changing user permission with wrong unauthorised user
    '''
    # Setup pytest
    _, user_2, user_3 = setup
 
    with pytest.raises(AccessError):
        assert other.admin_userpermission_change(user_2['token'], user_3['u_id'], 1)
 
 
def test_admin_userpermission_change_success(setup):
    '''
    Successful admin user permission change
    '''
    # Setup pytest
    user_1, user_2, _ = setup
 
    other.admin_userpermission_change(user_1['token'], user_2['u_id'], 1)
 
    assert other.get_user_permission(user_2['u_id']) == 1
 
################################################################################
 
def test_search(setup):
    '''
    searching in a channel
    '''
    user_1, user_2, _ = setup
 
    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])
 
    message.message_send(user_1['token'], channel_data['channel_id'], 'msg')
    message.message_send(user_1['token'], channel_data['channel_id'], 'test')
    message.message_send(user_1['token'], channel_data['channel_id'], 'Hello')
    message.message_send(user_2['token'], channel_data['channel_id'], 'test2')
    result = other.search(user_1['token'], 'est')
    assert result == {
        'messages': [
            {
                'message_id': 2,
                'channel_id': channel_data['channel_id'],
                'u_id': other.token_to_uid(user_1['token']),
                'message': 'test',
                'time_created': result['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            },
            {
                'message_id': 4,
                'channel_id': channel_data['channel_id'],
                'u_id': other.token_to_uid(user_2['token']),
                'message': 'test2',
                'time_created': result['messages'][1]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            }
        ]
    }
 
def test_search_other_channel(setup):
    '''
    searching in a separate channel
    '''
    user_1, user_2, _ = setup
 
    channel_data = channels.channels_create(user_1['token'], 'test channel', False)
    channel_data2 = channels.channels_create(user_2['token'], 'test channel2', False)
 
    message.message_send(user_1['token'], channel_data['channel_id'], 'msg')
    message.message_send(user_1['token'], channel_data['channel_id'], 'test')
    message.message_send(user_1['token'], channel_data['channel_id'], 'Hello')
    message.message_send(user_2['token'], channel_data2['channel_id'], 'test2')
    result = other.search(user_1['token'], 'e')
    assert result == {
        'messages': [
            {
                'message_id': 2,
                'channel_id': channel_data['channel_id'],
                'u_id': other.token_to_uid(user_1['token']),
                'message': 'test',
                'time_created': result['messages'][0]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            },
            {
                'message_id': 3,
                'channel_id': channel_data['channel_id'],
                'u_id': other.token_to_uid(user_1['token']),
                'message': 'Hello',
                'time_created': result['messages'][1]['time_created'],
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            }
        ]
    }

################################################################################

def test_invalid_token(setup):
    '''
    Checking that the invalid token checks are working
    '''

    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', True)
    message.message_send(user_1['token'], channel_data['channel_id'], 'msg')

    with pytest.raises(AccessError):
        assert other.users_all('invalid-token')
    
    with pytest.raises(AccessError):
        assert other.admin_userpermission_change('invalid-token', user_2['u_id'], 1)
    
    with pytest.raises(AccessError):
        assert other.search('invalid-token', 'a')
