import pytest
import channel
from error import InputError, AccessError

########################################################

def test_channel_invite_invalid_channel_id():
    # Throw InputError 
    pass

def test_channel_invite_invalid_uid():
    # Throw InputError 
    pass

def test_channel_invite_invalid_access():
    # Throw AccessError 
    pass

########################################################

def test_channel_invalid_channel():
    # Throw InputError 
    pass

def test_channel_invalid_access():
    # Throw AccessError  
    pass

# def test_channel_details():
#     assert channel.channel_details(1, 1) == {
#         'name': 'Hayden',
#         'owner_members': [
#             {
#                 'u_id': 1,
#                 'name_first': 'Hayden',
#                 'name_last': 'Jacobs',
#             }
#         ],
#         'all_members': [
#             {
#                 'u_id': 1,
#                 'name_first': 'Hayden',
#                 'name_last': 'Jacobs',
#             }
#         ],
#     }

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
    # Throw InputError 
    pass

def test_channel_leave_not_already_in_channel():
    # Throw AccessError 
    pass

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
    # Throw InputError 
    pass
 
def test_channel_join_invalid_access():
    # Throw AccessError  
    pass

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
    # Throw InputError 
    pass


def test_channel_addowner_already_existing_owner():
    # Throw InputError 
    pass

def test_channel_addowner_not_owner_of_flockr():
    # Throw AccessError 
    pass

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