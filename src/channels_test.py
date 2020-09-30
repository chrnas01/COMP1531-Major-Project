import pytest
import auth 
import channel 
import channels 
from error import InputError         

    ### Functions to be seperated out and file to be formatted and styled correctly ###
    ## Include auth.delete_users() to ensure more accurate testing. 
def test_channels_list(): 

    # Assume user is registered and logged in:  [For Tests 1 - 4]
    auth.auth_register("chris@gmai.com, "password", "Chris", "Nassif")
    auth.auth_login("chris@gmail.com, "password")

    # Test 1: 
    channels.channels_create("chris@gmail.com", "Channel_1", True) == {'channel_id': 1,}
    channel.channel_join()



    # Test 1: Unsuccessful for unregistered user 
    with pytest raises(InputError) as e: 
        assert channels.channels_list("invaliduser@gmail.com") 

    # Test 2: Registered users that dont belong to a channel should returh an empty dictionary 
    auth.auth_register("JohnSmith@gmai.com, "password", "John", "Smith")
    assert channels.channels_list("JohnSmith@gmail.com") == {}

    # Test 3:

def test_channels_listall(): 

    # Assume user is registered and logged in
    auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif")
    auth.auth_login("chris@gmail.com", "password")

    # Assume there is an existing private and public channel. 
    channels.channels_create("chris@gmail.com", "Channel_1", True) == {'channel_id': 1,}
    channels.channels_create("chris@gmail.com", "Channel_2", False) == {'channel_id': 2,}
    
    # Test 1:  Successful for registered and logged in user 
    assert channels.channels_listall("chris@gmail.com") == 'channels': [{'channel_id': 1,'name': 'Channel_1',}, 
    {'channel_id': 2,'name': 'Channel_2',}]

    # Test 2: Unsuccessful for unregistered user 
    with pytest.raises(InputError) as e: 
        assert channels.channels_listall("unregistered@gmail.com")
    
   
def test_channels_create(): 


    # Assume user is registered and logged in:  [For Tests 1 - 4]
    auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif")
    auth.auth_login("chris@gmail.com", "password")
    # The token "chris@gmail.com is valid" 

    # Test 1: Public channel name is greater than 20 characters long: 
    with pytest.raises(InputError) as e:
        assert channels.channels_create("chris@gmail.com", "ChannelNameGreaterthan20characters", True) 
    
    # Test 2: Private channel name is greather than 20 characterss long: 
    with pytest.raises(InputError) as e: 
        assert channels.channels_create("chris@gmai.com", "ChannelNameGreaterthan20characters", False) 

    # Test 3: Successfully creates Public Channel
    assert channels.channels_create("chris@gmail.com", "ChannelName", True) == {'channel_id': 1}

    # Tets 4: Successfuly creates Private Channel 
    assert channels.channels_create(chris@gmail.com, "ChannelName", False) == {'channel_id': 1}

    # Test 5: Unregistered/ Invalid user attempts to create channel 
    ######## For Public 
                ### Use auth.delete_users() function for better testing ###
    
    with pytest.raises(InputError) as e: 
        assert channels.channels_create("unregistered@gmail.com", "ChannelName", True)
    ######## For Private
    with pytest.raises(InputError) as e: 
        assert channels.channels_create("unregistered@gmail.com", "ChannelName", False)

    # Test 6: Channel name already exists 
    
    with pytest.raises(InputError) as e: 
        assert channels.channels_create("unregistered@gmail.com", "ChannelName", False)