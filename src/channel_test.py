import pytest
import auth
import channel
import channels
from error import InputError, AccessError

########################################################

def test_channel_invite_invalid_channel_id():

    # Init the variables
    token = "jayden@gmail.com"
    channel_id = 1
    u_id = 2

    # Register the users
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    auth.auth_register("Steven@gmail.com", "password", "Steven", "Luong")
    
    # Create a private channel
    # channels.create(token, "EPIC CHANNEL", False)

    with pytest.raises(InputError) as e:
        assert channel.channel_invite(token, channel_id, u_id)


def test_channel_invite_invalid_uid():
    # Init the variables
    token = "jayden@gmail.com"
    channel_id = 1
    u_id = 99

    # Register the users
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    
    # Create a private channel
    channels.channels_create(token, "EPIC CHANNEL", False)

    with pytest.raises(InputError) as e:
        assert channel.channel_invite(token, channel_id, u_id)

def test_channel_invite_invalid_access():
    # Init the variables
    token = "steven@gmail.com"
    channel_id = 1
    u_id = 99

    # Register the users
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    auth.auth_register("sam@gmail.com", "password", "Sam", "He") # uid 3

    # Create a private channel as jayden
    channels.channels_create("jayden@gmail.com", "EPIC CHANNEL", False) # channel_id 1

    # Invite as steven
    with pytest.raises(AccessError) as e:
        assert channel.channel_invite(token, channel_id, 3)

########################################################

def test_channel_details_invalid_channel_id():
    # Init the variables
    token = "jayden@gmail.com"
    channel_id = 99

    # Register the users
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner

    # Channel does not exist
    with pytest.raises(InputError) as e:
        assert channel.channel_details(token, channel_id)

def test_channel_details_invalid_access():
    # Init the variables
    token = "steven@gmail.com"
    channel_id = 1

    # Register the users
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    auth.auth_register("sam@gmail.com", "password", "Sam", "He") # uid 3

    # Create a private channel as jayden
    channels.channels_create("jayden@gmail.com", "EPIC CHANNEL", False) # channel_id 1

    # Call channel_details with the user that is not in the channel
    with pytest.raises(AccessError) as e:
        assert channel.channel_details(token, channel_id)

########################################################

def test_channel_messages_invalid_channel_id():
    # Throw InputError 
    pass

def test_channel_messages_invalid_start():
    # Throw InputError 
    pass

def test_channel_messages_invalid_access():
    # Throw AccessError 
    pass

########################################################

def test_channel_leave_invalid_channel_id():
    # Init the variables
    token = "steven@gmail.com"
    channel_id = 99

    # Register the users
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    auth.auth_register("sam@gmail.com", "password", "Sam", "He") # uid 3


    # Call channel_leave to a channel that does not exist
    with pytest.raises(InputError) as e:
        assert channel.channel_leave(token, channel_id)

def test_channel_leave_not_already_in_channel():

    # Init the variables
    token = "steven@gmail.com"
    channel_id = 1

    # Register the users
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    auth.auth_register("sam@gmail.com", "password", "Sam", "He") # uid 3

    # Create a private channel as jayden
    channels.channels_create("jayden@gmail.com", "EPIC CHANNEL", False) # channel_id 1

    # Call channel_leave when the user is not in the channel
    with pytest.raises(AccessError) as e:
        assert channel.channel_leave(token, channel_id)


# def test_channel_leave():
#     # Assumes that channel_invite is working
#     # Assumes that channel_join is working
#     # Assumes that channel_details is working

#     token = 1
#     channel_id = 1
#     u_id = 1

#     channel.channel_invite(token, channel_id, u_id)   
#     channel.channel_join(token, channel_id)

#     # Maybe check that the person join successfully
#     channel.channel_leave(token, channel_id)

#     result = channel.channel_details(token, channel_id)

#     # Need to change into a for loop
#     assert result['all_members'][0]['u_id'] != u_id

########################################################

def test_channel_join_invalid_channel_id():
    # Init the variables
    token = "steven@gmail.com"
    channel_id = 99

    # Register user
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    with pytest.raises(InputError) as e:
        assert channel.channel_join(token, channel_id)
 
def test_channel_join_invalid_access():
    # Init the variables
    token = "steven@gmail.com"
    channel_id = 1

    # Register user
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    # Create a private channel as jayden
    channels.channels_create("jayden@gmail.com", "EPIC CHANNEL", False) # channel_id 1

    with pytest.raises(AccessError) as e:
        assert channel.channel_join(token, channel_id)
 

# def test_channel_join():
#     # Assumes that channel_invite is working
#     # Assumes that channel_details is working

#     token = 1
#     channel_id = 1
#     u_id = 1

#     channel.channel_invite(token, channel_id, u_id)   
#     channel.channel_join(token, channel_id)
#     result = channel.channel_details(token, channel_id)
#     assert result['all_members'][0]['u_id'] == u_id

########################################################

def test_channel_addowner_invalid_channel_id():
    # Init the variables
    token = "jayden@gmail.com"
    channel_id = 99

    # Register user
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(token, channel_id, 2)


def test_channel_addowner_already_existing_owner():
    # Init the variables
    token = "jayden@gmail.com"
    channel_id = 1

    # Register users
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    # Create a private channel as jayden
    channels.channels_create("jayden@gmail.com", "EPIC CHANNEL", False) # channel_id 1

    # Add yourself to the channel
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(token, channel_id, 1)

def test_channel_addowner_not_owner_of_flockr():
    # Init the variables
    token = "steven@gmail.com"
    channel_id = 1

    # Register users
    auth.auth_register("jayden@gmail.com", "password", "Jayden", "Leung") # Flockr Owner
    auth.auth_register("steven@gmail.com", "password", "Steven", "Luong") # uid 2
    
    # Create a public channel as jayden
    channels.channels_create("jayden@gmail.com", "EPIC CHANNEL", True) # channel_id 1

    # Get a user to join the channel
    channel.channel_join(token, channel_id)

    # Try to your own escalate perms
    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(token, channel_id, 1)

def test_channel_addowner_not_owner_of_channel():
    # Throw AccessError 
    pass

# def test_channel_addowner():
#     # Assumes that channel_invite is working
#     # Assumes that channel_join is working
#     # Assumes that channel_details is working
    
#     token = 1
#     channel_id = 1
#     u_id = 1

#     channel.channel_invite(token, channel_id, u_id)   
#     channel.channel_join(token, channel_id)
#     # Maybe check that the person join successfully

#     channel.channel_addowner(token, channel_id, u_id)
#     result = channel.channel_details(token, channel_id)
#     # Need to change into a for loop
#     assert result['owner_members'][0]['u_id'] == u_id

########################################################

def test_channel_removeowner_invalid_channel_id():
    # Throw InputError 
    pass

def test_channel_removeowner_not_owner_of_channel():
    # Throw InputError 
    pass

def test_channel_removeowner_not_owner_of_flockr():
    # Throw AccessError 
    pass

# def test_channel_removeowner():
#     # Assumes that channel_invite is working
#     # Assumes that channel_join is working
#     # Assumes that channel_addowner is working
#     # Assumes that channel_details is working

#     token = 1
#     channel_id = 1
#     u_id = 1

#     channel.channel_invite(token, channel_id, u_id)   
#     channel.channel_join(token, channel_id)
#     # Maybe check that the person join successfully

#     channel.channel_addowner(token, channel_id, u_id)
#     channel.channel_removeowner(token, channel_id, u_id)
#     result = channel.channel_details(token, channel_id)
#     # Need to change into a for loop
#     assert result['owner_members'][0]['u_id'] != u_id

########################################################