import pytest
import auth
import channel
import channels
from error import InputError, AccessError

########################################################

def test_channel_invite_invalid_channel_id():
    # Register the users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("Steven@gmail.com", "password", "Steven", "Luong")
    
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(u1["token"], 99, u2["u_id"])


def test_channel_invite_invalid_uid():
    # Register the users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    
    # Create a private channel
    channel_id = channels.channels_create(u1["token"], "EPIC CHANNEL", False)

    with pytest.raises(InputError) as e:
        assert channel.channel_invite(u1["token"], channel_id, 99)

def test_channel_invite_invalid_access():
    # Register the users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    u3 = auth.auth_register("sam@gmail.com", "password", "Sam", "He") # uid 3

    # Create a private channel as jayden
    channel_id = channels.channels_create(u1["token"], "EPIC CHANNEL", False) # channel_id 1

    # Invite sam as steven
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite(u2["token"], channel_id, u3["u_id"])

########################################################

def test_channel_details_invalid_channel_id():
    # Register the users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner

    # Channel does not exist
    with pytest.raises(InputError) as e:
        assert channel.channel_details(u1["token"], 99)

def test_channel_details_invalid_access():
    # Register the users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    u3 = auth.auth_register("sam@gmail.com", "password", "Sam", "He") # uid 3

    # Create a private channel as jayden
    channel_id = channels.channels_create(u1["token"], "EPIC CHANNEL", False) # channel_id 1

    # Call channel_details with the user that is not in the channel
    with pytest.raises(AccessError) as e:
        assert channel.channel_details(u2["token"], channel_id)

########################################################

def test_channel_messages_invalid_channel_id():
    # Register the users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner

    # Call channel_leave to a channel that does not exist
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(u1["token"], 99, 1)

def test_channel_messages_invalid_start():
    # Throw InputError 
    pass

def test_channel_messages_invalid_access():
    # Throw AccessError 
    pass

########################################################

def test_channel_leave_invalid_channel_id():
    # Register the users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner

    # Call channel_leave to a channel that does not exist
    with pytest.raises(InputError) as e:
        assert channel.channel_leave(u1["token"], 99)

def test_channel_leave_not_already_in_channel():
    # Register the users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    u3 = auth.auth_register("sam@gmail.com", "password", "Sam", "He") # uid 3

    # Create a private channel as jayden
    channel_id = channels.channels_create(u1["token"], "EPIC CHANNEL", False) # channel_id 1

    # Call channel_leave when the user is not in the channel
    with pytest.raises(AccessError) as e:
        assert channel.channel_leave(u2["token"], channel_id)

########################################################

def test_channel_join_invalid_channel_id():
    # Register user
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    
    with pytest.raises(InputError) as e:
        assert channel.channel_join(u1["token"], 99)
 
def test_channel_join_invalid_access():
    # Register user
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    # Create a private channel as jayden
    channel_id = channels.channels_create(u1["token"], "EPIC CHANNEL", False) # channel_id 1

    with pytest.raises(AccessError) as e:
        assert channel.channel_join(u2["token"], channel_id)
 
########################################################

def test_channel_addowner_invalid_channel_id():
    # Register user
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(u1["token"], 99, u2["u_id"])

def test_channel_addowner_already_existing_owner():
    # Register users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    # Create a private channel as jayden
    channel_id = channels.channels_create(u1["token"], "EPIC CHANNEL", False) # channel_id 1

    # Add yourself to the channel
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(u1["token"], channel_id, u1["u_id"])

def test_channel_addowner_not_owner_of_flockr():
    # Register users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    # Create a public channel as jayden
    channel_id = channels.channels_create(u1["token"], "EPIC CHANNEL", True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(u2["token"], channel_id)

    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(u2["token"], channel_id, u1["u_id"])

def test_channel_addowner_not_owner_of_channel():
    # Register users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    u3 = auth.auth_register("sam@gmail.com", "password", "Sam", "He") # uid 3
    
    # Create a public channel as jayden
    channel_id = channels.channels_create(u1["token"], "EPIC CHANNEL", True) # channel_id 1

    # Get both users to join the channel
    channel.channel_join(u2["token"], channel_id)
    channel.channel_join(u3["token"], channel_id)

    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(u2["token"], channel_id, u3["u_id"])

########################################################

def test_channel_removeowner_invalid_channel_id():
    # Register user
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(u1["token"], 99, u2["u_id"])

def test_channel_removeowner_not_owner_of_channel():
    # Register users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    # Create a public channel as jayden
    channel_id = channels.channels_create(u1["token"], "EPIC CHANNEL", True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(u2["token"], channel_id)

    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(u1["token"], channel_id, u2["u_id"])

def test_channel_removeowner_not_owner_of_flockr():
    # Register users
    u1 = auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    u2 = auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    # Create a public channel as jayden
    channel_id = channels.channels_create(u1["token"], "EPIC CHANNEL", True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(u2["token"], channel_id)

    with pytest.raises(AccessError) as e:
        assert channel.channel_removeowner(u2["token"], channel_id, u1["u_id"])

########################################################