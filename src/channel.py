import pytest
from auth import all_users, auth_register
from channels import data, channels_create
from error import InputError, AccessError
import other

# data = {
#     'channels': [
#         {
#                 'channel_name': "channel 1"
#                 'channel_id': 1               # always one number behind the index
#                 'is_public': true 

#                 'owner_members': [
#                     1,
#                 ],
#                 'all_members': [
#                     1,
#                 ],
#         },

#         {
#                 'channel_name': "channel 2"
#                 'channel_id': 2               # always one number behind the index
#                 'is_public': true 

#                 'owner_members': [
#                     1,
#                 ],
#                 'all_members': [
#                     1,
#                 ],
#         },
#     ],
# }

# all_users = [
#     {
#         'u_id': u_id, 
#         'token': token, 
#         'email': email, 
#         'password': password, 
#         'name_first': name_first, 
#         'name_last': name_last, 
#      {   'handle_str': handle_str,
#     },
#     
#         'u_id': u_id, 
#         'token': token, 
#         'email': email, 
#         'password': password, 
#         'name_first': name_first, 
#         'name_last': name_last, 
#         'handle_str': handle_str,
#     }
#     ]

def token_to_uid(token):
    for user in all_users:
        if user['token'] == token:
            return user['u_id']
    else:
        return -1 

def channel_invite(token, channel_id, u_id):
    # Check for channel_id exists
    if channel_id > len(data['channels']):
        raise InputError("channel_id does not refer to a valid")

    # Check if user exists
    if token_to_uid(token) <= 0 or token_to_uid(token) > len(all_users):
        raise InputError("u_id does not refer to a valid user")
    
    # Check that the user is a member of the channel
    if token_to_uid(token) in data['channels'][channel_id - 1]['all_members']:
        raise AccessError("the authorised user is not already a member of the channel")
         
    # add the user the the channel
    data['channels'][channel_id - 1]['all_members'].append(u_id)
    
    # Why not
    data['channels'][channel_id - 1]['all_members'].sort()

def channel_details(token, channel_id):
    # Check for channel_id exists
    if channel_id > len(data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check that the user is a member of the channel
    if token_to_uid(token) in data['channels'][channel_id - 1]['all_members']:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    name = data['channels'][channel_id - 1]['channel_name']
    owner_members = data['channels'][channel_id - 1]['owner_members']
    all_members = data['channels'][channel_id - 1]['all_members']

    return {
        'name' : name,
        'owner_members': owner_members,
        'all_members': all_members
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
    if token_to_uid(token) in data['channels'][channel_id - 1]['all_members']:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    data['channels'][channel_id - 1]['all_members'].remove(token_to_uid(token))
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
    data['channels'][channel_id - 1]['all_members'].sort()
        
    # remove duplicates
    data['channels'][channel_id - 1]['all_members'] = list(set(data['channels'][channel_id - 1]['all_members'].append(token_to_uid(token))))


def channel_addowner(token, channel_id, u_id):
    # Check for channel_id exists
    if channel_id > len(data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check for already an owner
    if u_id in data['channels'][channel_id - 1]['owner_members']:
        raise InputError("When user with user id u_id is already an owner of the channel")

    # Check for not flockr owner and a member
    if token_to_uid(token) != 1:
        if not token_to_uid(token) in data['channels'][channel_id - 1]['owner_members']:
            raise AccessError("when the authorised user is not an owner of the flockr, or an owner of this channel")

    data['channels'][channel_id - 1]['owner_members'].append(token_to_uid(token))
    data['channels'][channel_id - 1]['owner_members'].sort()
        
def channel_removeowner(token, channel_id, u_id):
    # Check for channel_id exists
    if channel_id > len(data['channels']):
        raise InputError("Channel ID is not a valid channel")

    # Check if they are in owner_members
    if not u_id in data['channels'][channel_id - 1]['owner_members']:
        raise InputError("When user with user id u_id is not an owner of the channel")

    # Check for not flockr owner and a member
    if token_to_uid(token) != 1:
        if not token_to_uid(token) in data['channels'][channel_id - 1]['owner_members']:
            raise AccessError("when the authorised user is not an owner of the flockr, or an owner of this channel")

    data['channels'][channel_id - 1]['owner_members'].remove(token_to_uid(token))
    data['channels'][channel_id - 1]['owner_members'].sort()
        
