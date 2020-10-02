import pytest
import auth
from channels import data
from error import InputError, AccessError

# data = {
#     'channels': [
#         {
#                 'channel_name': "channel 1"
#                 'channel_id': 1               # always one number behind the index
#                 'privacy_status': true 

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
#                 'privacy_status': true 

#                 'owner_members': [
#                     1,
#                 ],
#                 'all_members': [
#                     1,
#                 ],
#         },
#     ],
# }


def channel_invite(token, channel_id, u_id):
    pass
    # # Check for channel_id does not refer to a valid
    # if channel_id > len(data['channels'])
    #     raise InputError("channel_id does not refer to a valid")

    # # Check for u_id does not refer to a valid user

    # # Check for when the authorised user is not already a member of the channel

    # data['channels'][channel_id - 1]['all_members'].append(u_id)
    




def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
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
    return {
    }

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }