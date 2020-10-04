import pytest
from auth import auth_register
from channels import channels_create
from error import InputError, AccessError
import other

def valid_user(u_id):
    for user in other.data['users']:
        if user['u_id'] == u_id:
            return True
    else:
        return False 
    
def channel_invite(token, channel_id, u_id):
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError("channel_id does not refer to a valid")

    # Check if token user exists
    if not valid_user(other.token_to_uid(token)): 
        raise InputError("token does not refer to a valid user")

    # Check if user exists
    if not valid_user(u_id):
        raise InputError("u_id does not refer to a valid user")
       
    # Check that the user is a member of the channel
    if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['all_members']:
        raise AccessError("the authorised user is not already a member of the channel")
         
    # add the user the the channel
    other.data['channels'][channel_id - 1]['all_members'].append(u_id)
    
    other.data['channels'][channel_id - 1]['all_members'].sort()

def channel_details(token, channel_id):
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check that the user is a member of the channel
    if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['all_members']:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    name = other.data['channels'][channel_id - 1]['channel_name']
    owner_members = other.data['channels'][channel_id - 1]['owner_members']
    all_members = other.data['channels'][channel_id - 1]['all_members']

    list_owner_members = []
    for u_id in owner_members:
        # seach for uid
        for user in other.data['users']:
            if user['u_id'] == u_id:
                temp_dict = {
                    'u_id': user['u_id'],
                    'name_first': user['name_first'],
                    'name_last': user['name_last']
                }
                list_owner_members.append(temp_dict)
                break

    list_all_members = []
    for u_id in all_members:
        # seach for uid
        for user in other.data['users']:
            if user['u_id'] == u_id:
                temp_dict = {
                    'u_id': user['u_id'],
                    'name_first': user['name_first'],
                    'name_last': user['name_last']
                }
                list_all_members.append(temp_dict)
                break


    return {
        'name' : name,
        'owner_members': list_owner_members,
        'all_members': list_all_members
    }


def channel_messages(token, channel_id, start):
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError("Channel ID is not a valid channel")

    #Check that the start is within the number of messages
    if start > len(other.data['messages']):
        raise InputError("Start is greater than the total number of messages in the channel")

    # Check that the user is a member of the channel
    if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['all_members']:
        raise AccessError("Authorised user is not a member of channel with channel_id")    

    end = start + 50
    end_index = end

    if (start + 50) >= len(other.data['messages']):
        end_index = len(other.data['messages']) - 1
        end = -1


    return {
        'messages': other.data['messages'][start:end_index],
        'start': start,
        'end': end
    } 



def channel_leave(token, channel_id):
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check that the user is a member of the channel
    if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['all_members']:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    other.data['channels'][channel_id - 1]['all_members'].remove(other.token_to_uid(token))

    if other.token_to_uid(token) in other.data['channels'][channel_id - 1]['owner_members']:
        other.data['channels'][channel_id - 1]['owner_members'].remove(other.token_to_uid(token))

def channel_join(token, channel_id):
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError("Channel ID is not a valid channel")
    
    # for not global owner(flockr owner)
    if other.token_to_uid(token) != 1:
        if other.data['channels'][channel_id - 1]['is_public'] == False:
            raise AccessError("channel_id refers to a channel that is private")

    other.data['channels'][channel_id - 1]['all_members'].append(other.token_to_uid(token))
    
    # remove duplicates
    other.data['channels'][channel_id - 1]['all_members'] = list(set(other.data['channels'][channel_id - 1]['all_members']))
    
    other.data['channels'][channel_id - 1]['all_members'].sort()

def channel_addowner(token, channel_id, u_id):
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check if user exists
    if not valid_user(u_id):
        raise InputError("u_id does not refer to a valid user")
    
    # Check for already an owner
    if u_id in other.data['channels'][channel_id - 1]['owner_members']:
        raise InputError("When user with user id u_id is already an owner of the channel")

    # Check for not flockr owner and a member
    if other.token_to_uid(token) != 1:
        if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['owner_members']:
            raise AccessError("when the authorised user is not an owner of the flockr, or an owner of this channel")

    other.data['channels'][channel_id - 1]['owner_members'].append(u_id)
    
    # remove duplicates
    other.data['channels'][channel_id - 1]['owner_members'] = list(set(other.data['channels'][channel_id - 1]['owner_members']))
    
    other.data['channels'][channel_id - 1]['owner_members'].sort()
        
def channel_removeowner(token, channel_id, u_id):
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check if user exists
    if not valid_user(u_id):
        raise InputError("u_id does not refer to a valid user")

    # Check if they are in owner_members
    if u_id not in other.data['channels'][channel_id - 1]['owner_members']:
        raise InputError("When user with user id u_id is not an owner of the channel")

    # Check for not flockr owner and a member
    if other.token_to_uid(token) != 1:
        if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['owner_members']:
            raise AccessError("when the authorised user is not an owner of the flockr, or an owner of this channel")

    other.data['channels'][channel_id - 1]['owner_members'].remove(u_id)

    other.data['channels'][channel_id - 1]['owner_members'].sort()
