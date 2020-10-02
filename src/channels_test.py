import pytest
import auth 
import channel 
import channels 
from error import InputError         

# Assumptions for these tests: 
    # The user is registered and logged in with a valid token. 
    # The user cannot join channels with invalid access i.e. can join a private channel if they have been invited only.
    # The user can successfully join and leave channels.  

# Tests for channels_list() function. 
################################################################################################################################

# Successfuly provides a list of all channels that the authorized user is part of: 
def test_channels_list_successful():
    auth.delete_users()
    # Include clear() function to clear channels 
    user1 = auth.auth_register("chris@gmail.com", "password", "Chris", "Nassif") 
    user2 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")

    # Creating a private and a public channel 
    channel1 = channels.channels_create(user1['token'], "Channel_1", True) 
    channel2 = channels.channels_create(user2['token'], "Channel_2", False)

    # Shouldn't include channel 2 as user1 is not in this channel 
    assert channels_list(user1['token']) == {[{'channel_id': channel1['channel_id'], 'name': "Channel_1"}]}

# User doesnt belong to any channels
def test_channels_list_no_channels: 
    auth.delete_users()
    # Include clear() function to clear channels 
    user1 = auth.auth_register("chris@gmail.com", "password", "Chris", "Nassif") 
    user2 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")

    # Only user 1 creates channel 
    channel1 = channels.channels_create(u1['token'], "Channel_1", True) 
    
    # User 2 belongs to no channels hence an empty list is returned 
    assert channels_list(user2['token']) == {[]}

# Tests for channels_listall() function. 
###############################################################################################################################

# Successfully provides a list of all channels and their associated details 
def test_channels_listall_successful(): 
    auth.delete_users()
    # Include clear() function to clear channels 
    user1 = auth.auth_register("chris@gmail.com", "password", "Chris", "Nassif")
    user2 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")

    # Created a private and a public channel 
    channel1 = channels.channels_create(user1['token'], "Channel_1", True) 
    channel2 = channels.channels_create(user2['token'], "Channel_2", False)
    
    assert channels.channels_listall(user1['token']) == {[{'channel_id': channel1['channel_id'], 'name': "Channel_1"}, {'channel_id': channel2['channel_id'], 'name': "Channel_2"}]}

# If there are no existing channels channels_listall() should return an empty list 
def test_channels_listall_no_existing_channels():
    auth.delete_users()
    # Include clear() function to clear channels 
    user1 = auth.auth_register("chris@gmail.com", "password", "Chris", "Nassif")
    assert channels.channels_listall(user1['token']) == {[]}
 
# Tests for channels_create() function.
################################################################################################################################

# Public channel name is greather than 20 charcters long 
def test_channels_create_invalid_channel_name1(): 
    auth.delete_users()
    # Include clear() function to clear channels 
    user1 = auth.auth_register("chris@gmail.com", "password", "Chris", "Nassif")
    with pytest.raises(InputError) as e:
        assert channels.channels_create(user1['token'], "ChannelNameGreaterthan20characters", True)            # For Public Channel. 

# Private channel name is greather than 20 characters long   
def test_channels_create_invalid_channel_name2():
    auth.delete_users()
    # Include clear() function to clear channels 
    user1 = auth.auth_register("chris@gmail.com", "password", "Chris", "Nassif")
    with pytest.raises(InputError) as e:
        assert channels.channels_create(user1['token'], "ChannelNameGreaterthan20characters", False)           # For Private Channel. 

# Public channel is successfully created 
def test_channels_create_successful_public():
    auth.delete_users()
    # Include clear() function to clear channels 
    user1 = auth.auth_register("chris@gmail.com", "password", "Chris", "Nassif")
    assert channels.channels_create(user1['token'], "ChannelName", True) == {'channel_id': 1}                  
    
# Private channel is successfully created 
def test_channels_create_successful_private():
    auth.delete_users()
    # Include clear() function to clear channels 
    user1 = auth.auth_register("chris@gmail.com", "password", "Chris", "Nassif")
    assert channels.channels_create(user1['token'], "ChannelName", False) == {'channel_id': 1}   
    
# Channel name already exists 
def test_channels_create_name_exists():
    auth.delete_users()
    # Include clear() function to clear channels 
    user1 = auth.auth_register("chris@gmail.com", "password", "Chris", "Nassif")
    user2 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    
    channels.channels_create(user1['token'], "ChannelName", True)
    with pytest.raises(InputError) as e: 
        assert channels.channels_create(user2['token'], "ChannelName", True)

# Channel name is not input i.e. trying to make a channel without a name
def test_channels_create_nameless_channel():
    auth.delete_users()
    user1 = auth.auth_register("chris@gmail.com", "password", "Chris", "Nassif")
    channels.channels_create(user1['token'], "", True)
    with pytest.raises(InputError) as e: 
        assert channels.channels_create(user2['token'], "", True)
