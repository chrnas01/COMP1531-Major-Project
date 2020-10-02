import pytest
import auth 
import channel 
import channels 
from error import InputError         

# Assumtiopns for these tests: 
    # The user is registered and logged in with a valid token. 
    # The user cannot join channels with invalid access i.e. can join a private channel if they have been invited only.
    # The user can successfully join and leave channels.  

###################################################################################################

# Successfuly provides a list of all channels that the authorized user is part of: 
def test_channels_list_successful():
    auth.delete_users()
    u1 = auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif") 
    u2 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")

    # Created a private and a public channel 
    c1 = channels.channels_create(u1['token'], "Channel_1", True) 
    c2 = channels.channels_create(u2['token'], "Channel_2", False)

    # Shouldnt include channel 2 as user1 is not in this channel 
    assert channels_list(u1['token']) == [{'channel_id': c1['channel_id'], 'name': "Channel_1"}]

# User doesnt belong to any channels
def test_channels_list_no_channels: 
    auth.delete_users()
    u1 = auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif") 
    u2 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")

    # Only user 1 creates channel 
    c1 = channels.channels_create(u1['token'], "Channel_1", True) 
    
    # User 2 belongs to no channels hence an empty list is returned 
    assert channels_list(u2['token']) == []


###############################################################################################################################

# Successfully provides a list of all channels and their associated details 
def test_channels_listall_successful(): 
    auth.delete_users()
    u1 = auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif")
    u2 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")

    # Created a private and a public channel 
    c1 = channels.channels_create(u1['token'], "Channel_1", True) 
    c2 = channels.channels_create(u2['token'], "Channel_2", False)
    
    assert channels.channels_listall(u1['token']) == [{'channel_id': c1['channel_id'], 'name': "Channel_1"}, {'channel_id': c2['channel_id'], 'name': "Channel_2"}] 

# If there are no existing channels channels_listall() should return an empty list 
def test_channels_listall_no_existing_channels():
    auth.delete_users()
    u1 = auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif")
    assert channels.channels_listall(u1['token']) == []
 
################################################################################################################################

# Public channel name is greather than 20 charcters long 
def test_channels_create_invalid_channel_name1(): 
    auth.delete_users()
    u1 = auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif")
    with pytest.raises(InputError) as e:
        assert channels.channels_create(u1['token'], "ChannelNameGreaterthan20characters", True)            # For Public Channel. 

# Private channel name is greather than 20 characters long   
def test_channels_create_invalid_channel_name2():
    auth.delete_users()
    u1 = auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif")
    with pytest.raises(InputError) as e:
        assert channels.channels_create(u1['token'], "ChannelNameGreaterthan20characters", False)           # For Private Channel. 

# Public channel is successfully created 
def test_channels_create_successful_public():
    auth.delete_users()
    u1 = auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif")
    assert channels.channels_create(u1['token'], "ChannelName", True) == {'channel_id': 1}                  
    
# Private channel is successfully created 
def test_channels_create_successful_private():
    auth.delete_users()
    u1 = auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif")
    assert channels.channels_create(u1['token'], "ChannelName", False) == {'channel_id': 1}   
    
# Channel name already exists 
def test_channels_create_name_exists():
    auth.delete_users()
    u1 = auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif")
    u2 = auth.auth_register("johnsmith@gmail.com", "password", "John", "Smith")
    
    channels.channels_create(u1['token'], "ChannelName", True)
    with pytest.raises(InputError) as e: 
        assert channels.channels_create(u2['token'], "ChannelName", True)