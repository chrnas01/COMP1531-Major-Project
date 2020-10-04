import pytest
from auth import all_users, auth_register
from channels import data, channels_create
from error import InputError, AccessError
import other
        
def token_to_uid(token):
    for user in all_users:
        if user['token'] == token:
            return user['u_id']
    else:
        return -1 

def valid_user(u_id):
    for user in all_users:
        if user['u_id'] == u_id:
            return True
    else:
        return False 
    
def channel_invite(token, channel_id, u_id):
    # Check for channel_id exists
    if channel_id > len(data['channels']):
        raise InputError("channel_id does not refer to a valid")

    # Check if token user exists
    if not valid_user(token_to_uid(token)): 
        raise InputError("token does not refer to a valid user")

    # Check if user exists
    if not valid_user(u_id):
        raise InputError("u_id does not refer to a valid user")
       
    # Check that the user is a member of the channel
    if not token_to_uid(token) in data['channels'][channel_id - 1]['all_members']:
        raise AccessError("the authorised user is not already a member of the channel")
         
    # add the user the the channel
    data['channels'][channel_id - 1]['all_members'].append(u_id)
    
    data['channels'][channel_id - 1]['all_members'].sort()

def channel_details(token, channel_id):
    # Check for channel_id exists
    if channel_id > len(data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check that the user is a member of the channel
    if not token_to_uid(token) in data['channels'][channel_id - 1]['all_members']:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    name = data['channels'][channel_id - 1]['channel_name']
    owner_members = data['channels'][channel_id - 1]['owner_members']
    all_members = data['channels'][channel_id - 1]['all_members']

    list_owner_members = []
    for u_id in owner_members:
        # seach for uid
        for user in all_users:
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
        for user in all_users:
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
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):
    # Check for channel_id exists
    if channel_id > len(data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check that the user is a member of the channel
    if not token_to_uid(token) in data['channels'][channel_id - 1]['all_members']:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    data['channels'][channel_id - 1]['all_members'].remove(token_to_uid(token))

    if token_to_uid(token) in data['channels'][channel_id - 1]['owner_members']:
        data['channels'][channel_id - 1]['owner_members'].remove(token_to_uid(token))

def channel_join(token, channel_id):
    # Check for channel_id exists
    if channel_id > len(data['channels']):
        raise InputError("Channel ID is not a valid channel")
    
    # for not global owner(flockr owner)
    if token_to_uid(token) != 1:
        if data['channels'][channel_id - 1]['is_public'] == False:
            raise AccessError("channel_id refers to a channel that is private")

    data['channels'][channel_id - 1]['all_members'].append(token_to_uid(token))
    
    # remove duplicates
    data['channels'][channel_id - 1]['all_members'] = list(set(data['channels'][channel_id - 1]['all_members']))
    
    data['channels'][channel_id - 1]['all_members'].sort()

def channel_addowner(token, channel_id, u_id):
    # Check for channel_id exists
    if channel_id > len(data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check if user exists
    if not valid_user(u_id):
        raise InputError("u_id does not refer to a valid user")
    
    # Check for already an owner
    if u_id in data['channels'][channel_id - 1]['owner_members']:
        raise InputError("When user with user id u_id is already an owner of the channel")

    # Check for not flockr owner and a member
    if token_to_uid(token) != 1:
        if not token_to_uid(token) in data['channels'][channel_id - 1]['owner_members']:
            raise AccessError("when the authorised user is not an owner of the flockr, or an owner of this channel")

    data['channels'][channel_id - 1]['owner_members'].append(u_id)
    
    # remove duplicates
    data['channels'][channel_id - 1]['owner_members'] = list(set(data['channels'][channel_id - 1]['owner_members']))
    
    data['channels'][channel_id - 1]['owner_members'].sort()
        
def channel_removeowner(token, channel_id, u_id):
    # Check for channel_id exists
    if channel_id > len(data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check if user exists
    if not valid_user(u_id):
        raise InputError("u_id does not refer to a valid user")

    # Check if they are in owner_members
    if not u_id in data['channels'][channel_id - 1]['owner_members']:
        raise InputError("When user with user id u_id is not an owner of the channel")

    # Check for not flockr owner and a member
    if token_to_uid(token) != 1:
        if not token_to_uid(token) in data['channels'][channel_id - 1]['owner_members']:
            raise AccessError("when the authorised user is not an owner of the flockr, or an owner of this channel")

    data['channels'][channel_id - 1]['owner_members'].remove(u_id)

    data['channels'][channel_id - 1]['owner_members'].sort()
        
