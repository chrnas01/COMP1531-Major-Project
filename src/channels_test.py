import pytest
import auth 
import channel 
import channels 
from error import InputError         


def test_channels_list(): 

# Assume channels_create function is working 
# Assume user is registered and logged in:  [For Tests 1 - 4]
    auth.auth_register("chris@gmai.com, "password", "Chris", "Nassif")
    auth.auth_login("chris@gmail.com, "password")



def test_channels_listall(): 

    # Assume user is registered and logged in
    auth.auth_register("chris@gmai.com", "password", "Chris", "Nassif")
    auth.auth_login("chris@gmail.com", "password")

    # Assume there are 3 existing channels 
    channels.channels_create("chris@gmail.com", "Channel_1", True) == {channel id }
    channels.channels_create("chris@gmail.com", "Channel_2", True)
    channels.channels_create("chris@gmail.com", "Channel_3", False)
    
    channels.channels_listall("chris@gmai.com")



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
    with pytest.raises(InputError) as e: 
        assert channels.channels_create("unregistered@gmail.com", "ChannelName", True)
    with pytest.raises(InputError) as e: 
        assert channels.channels_create("unregistered@gmail.com", "ChannelName", False)