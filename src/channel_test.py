'''
tests for channel.py
'''
import pytest
import auth
import channel
import channels
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
    user_2 = auth.auth_register('steven@gmail.com', 'password', 'Steven', 'Luong')
    user_3 = auth.auth_register('sam@gmail.com', 'password', 'Sam', 'He')

    return (user_1, user_2, user_3)

########################################################

def test_channel_invite_invalid_channel_id(setup):
    '''
    inviting to a channel which does not exist
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    with pytest.raises(InputError):
        assert channel.channel_invite(user_1['token'], 99, user_2['u_id'])

def test_channel_invite_invalid_uid(setup):
    '''
    inviting a user who does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    # Create a private channel
    channel_data = channels.channels_create(user_1['token'], 'test channel', False)

    with pytest.raises(InputError):
        assert channel.channel_invite(user_1['token'], channel_data['channel_id'], 99)

def test_channel_invite_invalid_access(setup):
    '''
    channel is private and user is not a member
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', False) # channel_id 1

    # Invite sam as steven
    with pytest.raises(AccessError):
        assert channel.channel_invite(user_2['token'], channel_data['channel_id'], user_3['u_id'])

def test_channel_invite_success(setup):
    '''
    channel invite success
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', True) # channel_id 1

    # Successful channel invite
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])

    result = channel.channel_details(user_1['token'], channel_data['channel_id'])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            }
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
    }

    assert result == expected_result


########################################################

def test_channel_details_invalid_channel_id(setup):
    '''
    channel does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    # Channel does not exist
    with pytest.raises(InputError):
        assert channel.channel_details(user_1['token'], 99)

def test_channel_details_invalid_access(setup):
    '''
    user is not a member of that channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', False) # channel_id 1

    # Call channel_details with the user that is not in the channel
    with pytest.raises(AccessError):
        assert channel.channel_details(user_2['token'], channel_data['channel_id'])

def test_channel_details_success(setup):
    '''
    successful call
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', True) # channel_id 1

    # Successful channel invite
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])

    result = channel.channel_details(user_2['token'], channel_data['channel_id'])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            }
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
    }

    assert result == expected_result

########################################################

def test_channel_messages_invalid_channel_id(setup):
    '''
    channel does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    # Throw InputError
    with pytest.raises(InputError):
        assert channel.channel_messages(user_1['token'], 1, 0)


def test_channel_messages_invalid_start(setup):
    '''
    starting point for messages is invalid
    '''
    # Setup pytest
    _, user_2, user_3 = setup

    # Create a private channel
    channel_data = channels.channels_create(user_3['token'], 'test channel', True)

    # Successful channel invite
    channel.channel_invite(user_3['token'], channel_data['channel_id'], user_2['u_id'])

    # Throw InputError
    with pytest.raises(InputError):
        assert channel.channel_messages(user_3['token'], channel_data['channel_id'], 99)


def test_channel_messages_invalid_access(setup):
    '''
    user is not a member of the channel
    '''
    # Setup pytest
    user_1, _, user_3 = setup

    # Create a private channel
    channel_data = channels.channels_create(user_3['token'], 'test channel', True)

    # Throw AccessError
    with pytest.raises(AccessError):
        assert channel.channel_messages(user_1['token'], channel_data['channel_id'], 0)


def test_channel_messages_success(setup):
    '''
    successful call
    '''
    # Setup pytest
    _, _, user_3 = setup

    # Create a private channel
    channel_data = channels.channels_create(user_3['token'], 'test channel', True)

    assert channel.channel_messages(user_3['token'], channel_data['channel_id'], 0) == {
        'messages': [], 'start': 0, 'end': -1}

########################################################

def test_channel_leave_invalid_channel_id(setup):
    '''
    channel does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    # Call channel_leave to a channel that does not exist
    with pytest.raises(InputError):
        assert channel.channel_leave(user_1['token'], 99)

def test_channel_leave_not_already_in_channel(setup):
    '''
    user is not in the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', False) # channel_id 1

    # Call channel_leave when the user is not in the channel
    with pytest.raises(AccessError):
        assert channel.channel_leave(user_2['token'], channel_data['channel_id'])

def test_channel_leave_success_all_members(setup):
    '''
    successful call for one user to leave the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', False) # channel_id 1

    # Join channel
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])

    # Leave channel
    channel.channel_leave(user_2['token'], channel_data['channel_id'])

    result = channel.channel_details(user_1['token'], channel_data['channel_id'])

    assert not user_2['u_id'] in result['owner_members']
    assert not user_2['u_id'] in result['all_members']

def test_channel_leave_empty_channel(setup):
    '''
    successful call for both users to leave the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', False) # channel_id 1

    # Join channel
    channel.channel_invite(user_1['token'], channel_data['channel_id'], user_2['u_id'])

    # Leave channel
    channel.channel_leave(user_2['token'], channel_data['channel_id'])
    channel.channel_leave(user_1['token'], channel_data['channel_id'])

    assert not user_1['u_id'] in other.data['channels'][channel_data['channel_id'] - 1][
            'all_members']
    assert not user_2['u_id'] in other.data['channels'][channel_data['channel_id'] - 1][
            'all_members']

########################################################

def test_channel_join_invalid_channel_id(setup):
    '''
    channel does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    with pytest.raises(InputError):
        assert channel.channel_join(user_1['token'], 99)

def test_channel_join_invalid_access(setup):
    '''
    user does not have permissions to join the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', False) # channel_id 1

    with pytest.raises(AccessError):
        assert channel.channel_join(user_2['token'], channel_data['channel_id'])

def test_channel_join_as_flockr_owner(setup):
    '''
    successful call with user as flockr owner
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a private channel as user_2
    channel_data = channels.channels_create(user_2['token'], 'test channel', False) # channel_id 1

    # join private channel as flockr owner
    channel.channel_join(user_1['token'], channel_data['channel_id'])

    result = channel.channel_details(user_1['token'], channel_data['channel_id'])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
    }

    assert result == expected_result


def test_channel_join_success(setup):
    '''
    successful call
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', True) # channel_id 1

    # Join channel
    channel.channel_join(user_2['token'], channel_data['channel_id'])
    channel.channel_join(user_3['token'], channel_data['channel_id'])

    result = channel.channel_details(user_2['token'], channel_data['channel_id'])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert result == expected_result

########################################################

def test_channel_addowner_invalid_channel_id(setup):
    '''
    channel does not exist
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    with pytest.raises(InputError):
        assert channel.channel_addowner(user_1['token'], 99, user_2['u_id'])

def test_channel_addowner_invalid_uid(setup):
    '''
    uid does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', False) # channel_id 1

    with pytest.raises(InputError):
        assert channel.channel_addowner(user_1['token'], channel_data['channel_id'], 99)

def test_channel_addowner_already_existing_owner(setup):
    '''
    the user is already an owner
    '''
    # Setup pytest
    user_1, _, _ = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', False) # channel_id 1

    # Add yourself into the channel
    with pytest.raises(InputError):
        assert channel.channel_addowner(user_1['token'], channel_data['channel_id'], user_1['u_id'])

def test_channel_addowner_self_escalation(setup):
    '''
    user attempts to set themselves as owner
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(user_2['token'], channel_data['channel_id'])

    with pytest.raises(AccessError):
        assert channel.channel_addowner(user_2['token'], channel_data['channel_id'], user_2['u_id'])

def test_channel_addowner_not_owner_of_channel(setup):
    '''
    user does not have permissions to set other user as owner
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', True) # channel_id 1

    # Get both users to join the channel
    channel.channel_join(user_2['token'], channel_data['channel_id'])
    channel.channel_join(user_3['token'], channel_data['channel_id'])

    with pytest.raises(AccessError):
        assert channel.channel_addowner(user_2['token'], channel_data['channel_id'], user_3['u_id'])

def test_channel_addowner_success(setup):
    '''
    successful call
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', True) # channel_id 1

    # Join channel
    channel.channel_join(user_2['token'], channel_data['channel_id'])
    channel.channel_join(user_3['token'], channel_data['channel_id'])

    # add owners
    channel.channel_addowner(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    channel.channel_addowner(user_2['token'], channel_data['channel_id'], user_3['u_id'])

    result = channel.channel_details(user_2['token'], channel_data['channel_id'])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert result == expected_result


def test_channel_addowner_as_flockr_owner(setup):
    '''
    successful call with user as flockr owner
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(user_2['token'], 'test channel', True) # channel_id 1

    # Join channel
    channel.channel_join(user_1['token'], channel_data['channel_id'])
    channel.channel_join(user_3['token'], channel_data['channel_id'])

    # add owners
    channel.channel_addowner(user_1['token'], channel_data['channel_id'], user_3['u_id'])

    # add himself
    channel.channel_addowner(user_1['token'], channel_data['channel_id'], user_1['u_id'])

    result = channel.channel_details(user_2['token'], channel_data['channel_id'])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert result == expected_result

########################################################

def test_channel_removeowner_invalid_channel_id(setup):
    '''
    channel does not exist
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    with pytest.raises(InputError):
        assert channel.channel_removeowner(user_1['token'], 99, user_2['u_id'])

def test_channel_removeowner_not_valid_uid(setup):
    '''
    uid is invalid
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(user_2['token'], channel_data['channel_id'])

    with pytest.raises(InputError):
        assert channel.channel_removeowner(user_1['token'], channel_data[
            'channel_id'], 99)

def test_channel_removeowner_not_owner_of_channel(setup):
    '''
    the user, perms being removed, is not an owner of the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(user_2['token'], channel_data['channel_id'])

    with pytest.raises(InputError):
        assert channel.channel_removeowner(user_1['token'], channel_data[
                'channel_id'], user_2['u_id'])

def test_channel_removeowner_invalid_perm(setup):
    '''
    the user, removing perms, is not an owner of the channel
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(user_2['token'], channel_data['channel_id'])

    with pytest.raises(AccessError):
        assert channel.channel_removeowner(user_2['token'], channel_data[
                'channel_id'], user_1['u_id'])

def test_channel_removeowner_success(setup):
    '''
    successful call
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(user_1['token'], 'test channel', True) # channel_id 1

    # Join channel
    channel.channel_join(user_2['token'], channel_data['channel_id'])
    channel.channel_join(user_3['token'], channel_data['channel_id'])

    # add owners
    channel.channel_addowner(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    channel.channel_addowner(user_2['token'], channel_data['channel_id'], user_3['u_id'])

    # remove owners
    channel.channel_removeowner(user_3['token'], channel_data['channel_id'], user_2['u_id'])
    channel.channel_removeowner(user_1['token'], channel_data['channel_id'], user_3['u_id'])
    channel.channel_removeowner(user_1['token'], channel_data['channel_id'], user_1['u_id'])

    result = channel.channel_details(user_2['token'], channel_data['channel_id'])

    expected_result = {
        'name': 'test channel',
        'owner_members': [

        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert result == expected_result

def test_channel_removeowner_as_flockr_owner(setup):
    '''
    successful call with user, removing perms, as flock owner
    '''
    # Setup pytest
    user_1, user_2, user_3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(user_2['token'], 'test channel', True) # channel_id 1

    # Join channel
    channel.channel_join(user_1['token'], channel_data['channel_id'])
    channel.channel_join(user_3['token'], channel_data['channel_id'])

    # add owner
    channel.channel_addowner(user_2['token'], channel_data['channel_id'], user_3['u_id'])

    # remove owners
    channel.channel_removeowner(user_1['token'], channel_data['channel_id'], user_2['u_id'])
    channel.channel_removeowner(user_1['token'], channel_data['channel_id'], user_3['u_id'])

    result = channel.channel_details(user_1['token'], channel_data['channel_id'])

    expected_result = {
        'name': 'test channel',
        'owner_members': [

        ],
        'all_members': [
            {
                'u_id': user_1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': user_2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': user_3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert result == expected_result

########################################################

def test_invalid_token(setup):
    '''
    Checking that the invalid token checks are working
    '''

    # Setup pytest
    user_1, user_2, _ = setup

    channel_data = channels.channels_create(user_1['token'], 'test channel', True)

    with pytest.raises(AccessError):
        assert channel.channel_details('invalid-token', channel_data['channel_id'])
        assert channel.channel_addowner('invalid-token', channel_data['channel_id'], user_2['u_id'])
        assert channel.channel_invite('invalid-token', channel_data['channel_id'], user_2['u_id'])
        assert channel.channel_join('invalid-token', channel_data['channel_id'])
        assert channel.channel_leave('invalid-token', channel_data['channel_id'])
        assert channel.channel_messages('invalid-token', channel_data['channel_id'], 0)
        assert channel.channel_removeowner('invalid-token', channel_data['channel_id'], user_1['u_id'])