import pytest
import auth
import channel
import channels
from error import InputError, AccessError
import other

########################################################

@pytest.fixture
def setup():
    # Clear database
    other.clear()

    # Setup users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("Steven@gmail.com", "password", "Steven", "Luong")
    u3 = auth.auth_register("sam@gmail.com", "password", "Sam", "He") 
    
    return u1, u2, u3

########################################################

def test_channel_invite_invalid_channel_id(setup):
    # Setup pytest
    u1, u2, u3 = setup
    
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(u1["token"], 99, u2["u_id"])

def test_channel_invite_invalid_uid(setup):
    # Setup pytest
    u1, u2, u3 = setup
    
    # Create a private channel
    channel_data = channels.channels_create(u1["token"], "test channel", False)

    with pytest.raises(InputError) as e:
        assert channel.channel_invite(u1["token"], channel_data["channel_id"], 99)

def test_channel_invite_invalid_access(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", False) # channel_id 1

    # Invite sam as steven
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite(u2["token"], channel_data["channel_id"], u3["u_id"])

def test_channel_invite_success(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", True) # channel_id 1

    # Successful channel invite
    channel.channel_invite(u1["token"], channel_data["channel_id"], u2["u_id"])

    result = channel.channel_details(u1["token"], channel_data["channel_id"])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            }
        ],
        'all_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
    }

    assert result == expected_result


########################################################

def test_channel_details_invalid_channel_id(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Channel does not exist
    with pytest.raises(InputError) as e:
        assert channel.channel_details(u1["token"], 99)

def test_channel_details_invalid_access(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", False) # channel_id 1

    # Call channel_details with the user that is not in the channel
    with pytest.raises(AccessError) as e:
        assert channel.channel_details(u2["token"], channel_data["channel_id"])

def test_channel_details_success(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", True) # channel_id 1

    # Successful channel invite
    channel.channel_invite(u1["token"], channel_data["channel_id"], u2["u_id"])

    result = channel.channel_details(u2["token"], channel_data["channel_id"])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            }
        ],
        'all_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
    }

    assert result == expected_result

########################################################

def test_channel_messages_invalid_channel_id(setup):
    # Setup pytest
    u1, u2, u3 = setup
    pass

def test_channel_messages_invalid_start(setup):
    # Setup pytest
    u1, u2, u3 = setup
    # Throw InputError 
    pass

def test_channel_messages_invalid_access(setup):
    # Setup pytest
    u1, u2, u3 = setup
    # Throw AccessError 
    pass


def test_channel_messages_success(setup):
    # Setup pytest
    u1, u2, u3 = setup
    pass

########################################################

def test_channel_leave_invalid_channel_id(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Call channel_leave to a channel that does not exist
    with pytest.raises(InputError) as e:
        assert channel.channel_leave(u1["token"], 99)

def test_channel_leave_not_already_in_channel(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", False) # channel_id 1

    # Call channel_leave when the user is not in the channel
    with pytest.raises(AccessError) as e:
        assert channel.channel_leave(u2["token"], channel_data["channel_id"])

def test_channel_leave_success_all_members(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", False) # channel_id 1

    # Join channel 
    channel.channel_invite(u1["token"], channel_data["channel_id"], u2["u_id"])

    # Leave channel
    channel.channel_leave(u2["token"], channel_data["channel_id"])

    result = channel.channel_details(u1["token"], channel_data["channel_id"])

    assert not u2['u_id'] in result['owner_members']
    assert not u2['u_id'] in result['all_members']

def test_channel_leave_empty_channel(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", False) # channel_id 1

    # Join channel 
    channel.channel_invite(u1["token"], channel_data["channel_id"], u2["u_id"])

    # Leave channel
    channel.channel_leave(u2["token"], channel_data["channel_id"])
    channel.channel_leave(u1["token"], channel_data["channel_id"])

    assert not u1["u_id"] in other.data['channels'][channel_data["channel_id"] - 1]['all_members']
    assert not u2["u_id"] in other.data['channels'][channel_data["channel_id"] - 1]['all_members']

########################################################

def test_channel_join_invalid_channel_id(setup):
    # Setup pytest
    u1, u2, u3 = setup
    
    with pytest.raises(InputError) as e:
        assert channel.channel_join(u1["token"], 99)
 
def test_channel_join_invalid_access(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a private channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", False) # channel_id 1

    with pytest.raises(AccessError) as e:
        assert channel.channel_join(u2["token"], channel_data["channel_id"])

def test_channel_join_as_flockr_owner(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a private channel as u2
    channel_data = channels.channels_create(u2["token"], "test channel", False) # channel_id 1

    # join private channel as flockr owner
    channel.channel_join(u1["token"], channel_data["channel_id"])

    result = channel.channel_details(u1["token"], channel_data["channel_id"])
    
    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
        'all_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
        ],
    }

    assert result == expected_result


def test_channel_join_success(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", True) # channel_id 1

    # Join channel 
    channel.channel_join(u2["token"], channel_data["channel_id"])
    channel.channel_join(u3["token"], channel_data["channel_id"])

    result = channel.channel_details(u2["token"], channel_data["channel_id"])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
        ],
        'all_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': u3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert result == expected_result

########################################################

def test_channel_addowner_invalid_channel_id(setup):
    # Setup pytest
    u1, u2, u3 = setup
    
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(u1["token"], 99, u2["u_id"])

def test_channel_addowner_already_existing_owner(setup):
    # Setup pytest
    u1, u2, u3 = setup
    
    # Create a private channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", False) # channel_id 1

    # Add yourself into the channel
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(u1["token"], channel_data["channel_id"], u1["u_id"])

def test_channel_addowner_not_owner_of_flockr(setup):
    # Setup pytest
    u1, u2, u3 = setup
    
    # Create a public channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(u2["token"], channel_data["channel_id"])

    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(u2["token"], channel_data["channel_id"], u2["u_id"])

def test_channel_addowner_not_owner_of_channel(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", True) # channel_id 1

    # Get both users to join the channel
    channel.channel_join(u2["token"], channel_data["channel_id"])
    channel.channel_join(u3["token"], channel_data["channel_id"])

    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(u2["token"], channel_data["channel_id"], u3["u_id"])

def test_channel_addowner_success(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", True) # channel_id 1

    # Join channel 
    channel.channel_join(u2["token"], channel_data["channel_id"])
    channel.channel_join(u3["token"], channel_data["channel_id"])

    # add owners
    channel.channel_addowner(u1["token"], channel_data["channel_id"], u2["u_id"])
    channel.channel_addowner(u2["token"], channel_data["channel_id"], u3["u_id"])

    result = channel.channel_details(u2["token"], channel_data["channel_id"])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': u3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
        'all_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': u3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }

    assert result == expected_result


def test_channel_addowner_as_flockr_owner(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(u2["token"], "test channel", True) # channel_id 1

    # Join channel 
    channel.channel_join(u1["token"], channel_data["channel_id"])
    channel.channel_join(u3["token"], channel_data["channel_id"])

    # add owners
    channel.channel_addowner(u1["token"], channel_data["channel_id"], u3["u_id"])

    # add himself
    channel.channel_addowner(u1["token"], channel_data["channel_id"], u1["u_id"])

    result = channel.channel_details(u2["token"], channel_data["channel_id"])

    expected_result = {
        'name': 'test channel',
        'owner_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': u3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
        'all_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': u3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }
    
    assert result == expected_result

########################################################

def test_channel_removeowner_invalid_channel_id(setup):
    # Setup pytest
    u1, u2, u3 = setup
    
    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(u1["token"], 99, u2["u_id"])

def test_channel_removeowner_not_owner_of_channel(setup):
    # Setup pytest
    u1, u2, u3 = setup
    
    # Create a public channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(u2["token"], channel_data["channel_id"])

    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(u1["token"], channel_data["channel_id"], u2["u_id"])

def test_channel_removeowner_not_owner_of_flockr(setup):
    # Setup pytest
    u1, u2, u3 = setup
    
    # Create a public channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(u2["token"], channel_data["channel_id"])

    with pytest.raises(AccessError) as e:
        assert channel.channel_removeowner(u2["token"], channel_data["channel_id"], u1["u_id"])

def test_channel_removeowner_success(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(u1["token"], "test channel", True) # channel_id 1

    # Join channel 
    channel.channel_join(u2["token"], channel_data["channel_id"])
    channel.channel_join(u3["token"], channel_data["channel_id"])

    # add owners
    channel.channel_addowner(u1["token"], channel_data["channel_id"], u2["u_id"])
    channel.channel_addowner(u2["token"], channel_data["channel_id"], u3["u_id"])

    # remove owners
    channel.channel_removeowner(u3["token"], channel_data["channel_id"], u2["u_id"])
    channel.channel_removeowner(u1["token"], channel_data["channel_id"], u3["u_id"])
    channel.channel_removeowner(u1["token"], channel_data["channel_id"], u1["u_id"])

    result = channel.channel_details(u2["token"], channel_data["channel_id"])

    expected_result = {
        'name': 'test channel',
        'owner_members': [

        ],
        'all_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': u3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }
    
    assert result == expected_result

def test_channel_removeowner_as_flockr_owner(setup):
    # Setup pytest
    u1, u2, u3 = setup

    # Create a public channel as jayden
    channel_data = channels.channels_create(u2["token"], "test channel", True) # channel_id 1

    # Join channel 
    channel.channel_join(u1["token"], channel_data["channel_id"])
    channel.channel_join(u3["token"], channel_data["channel_id"])

    # add owner
    channel.channel_addowner(u2["token"], channel_data["channel_id"], u3["u_id"])

    # remove owners
    channel.channel_removeowner(u1["token"], channel_data["channel_id"], u2["u_id"])
    channel.channel_removeowner(u1["token"], channel_data["channel_id"], u3["u_id"])

    result = channel.channel_details(u1["token"], channel_data["channel_id"])

    expected_result = {
        'name': 'test channel',
        'owner_members': [

        ],
        'all_members': [
            {
                'u_id': u1['u_id'],
                'name_first': 'Jayden',
                'name_last': 'Leung',
            },
            {
                'u_id': u2['u_id'],
                'name_first': 'Steven',
                'name_last': 'Luong',
            },
            {
                'u_id': u3['u_id'],
                'name_first': 'Sam',
                'name_last': 'He',
            },
        ],
    }
    
    assert result == expected_result

########################################################
