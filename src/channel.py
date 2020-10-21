'''
functions to manage users within a channel
'''
from error import InputError, AccessError
import other

def channel_invite(token, channel_id, u_id):
    '''
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately
    '''
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError('channel_id does not refer to a valid')

    # Check if user exists
    if not other.valid_user(u_id):
        raise InputError('u_id does not refer to a valid user')

    # Check that the user is a member of the channel
    if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['all_members']:
        raise AccessError('the authorised user is not already a member of the channel')

    # add the user the the channel
    other.data['channels'][channel_id - 1]['all_members'].append(u_id)

    other.data['channels'][channel_id - 1]['all_members'].sort()
    
    return {}

def channel_details(token, channel_id):
    '''
    Given a Channel with ID channel_id that the authorised user
    is part of, provide basic details about the channel
    '''
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    # Check that the user is a member of the channel
    if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['all_members']:
        raise AccessError('Authorised user is not a member of channel with channel_id')

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
    '''
    Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50".
    Message with index 0 is the most recent message in the channel.
    This function returns a new index "end" which is the value of "start + 50",
    or, if this function has returned the least recent messages in the channel,
    returns -1 in "end" to indicate there are no more messages to load after this return.
    '''
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    #Check that the start is within the number of messages
    if start > len(other.data['messages']):
        raise InputError('Start is greater than the total number of messages in the channel')

    # Check that the user is a member of the channel
    if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['all_members']:
        raise AccessError('Authorised user is not a member of channel with channel_id')

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
    '''
    Given a channel ID, the user removed as a member of this channel
    '''
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    # Check that the user is a member of the channel
    if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['all_members']:
        raise AccessError('Authorised user is not a member of channel with channel_id')

    other.data['channels'][channel_id - 1]['all_members'].remove(other.token_to_uid(token))

    if other.token_to_uid(token) in other.data['channels'][channel_id - 1]['owner_members']:
        other.data['channels'][channel_id - 1]['owner_members'].remove(other.token_to_uid(token))

    return {}

def channel_join(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can
    join, adds them to that channel
    '''
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    # for not global owner(flockr owner)
    if not other.check_if_flockr_owner(other.token_to_uid(token)):
        if not other.data['channels'][channel_id - 1]['is_public']:
            raise AccessError('channel_id refers to a channel that is private')

    other.data['channels'][channel_id - 1]['all_members'].append(other.token_to_uid(token))

    # remove duplicates
    other.data['channels'][channel_id - 1]['all_members'] = list(
        set(other.data['channels'][channel_id - 1]['all_members']))

    other.data['channels'][channel_id - 1]['all_members'].sort()

    return {}

def channel_addowner(token, channel_id, u_id):
    '''
    Make user with user id u_id an owner of this channel
    '''
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    # Check if user exists
    if not other.valid_user(u_id):
        raise InputError('u_id does not refer to a valid user')

    # Check for already an owner
    if u_id in other.data['channels'][channel_id - 1]['owner_members']:
        raise InputError('When user with user id u_id is already an owner of the channel')

    # Check for not flockr owner and a member
    if not other.check_if_flockr_owner(other.token_to_uid(token)):
        if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['owner_members']:
            raise AccessError('''The authorised user is not an
                 owner of the flockr, or an owner of this channel''')

    other.data['channels'][channel_id - 1]['owner_members'].append(u_id)

    # remove duplicates
    other.data['channels'][channel_id - 1]['owner_members'] = list(
        set(other.data['channels'][channel_id - 1]['owner_members']))

    other.data['channels'][channel_id - 1]['owner_members'].sort()

    return {}

def channel_removeowner(token, channel_id, u_id):
    '''
    Remove user with user id u_id an owner of this channel
    '''
    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    # Check if user exists
    if not other.valid_user(u_id):
        raise InputError('u_id does not refer to a valid user')

    # Check if they are in owner_members
    if u_id not in other.data['channels'][channel_id - 1]['owner_members']:
        raise InputError('When user with user id u_id is not an owner of the channel')

    # Check for not flockr owner and a member
    if not other.check_if_flockr_owner(other.token_to_uid(token)):
        if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['owner_members']:
            raise AccessError('''The authorised user is not an
                 owner of the flockr, or an owner of this channel''')

    other.data['channels'][channel_id - 1]['owner_members'].remove(u_id)

    other.data['channels'][channel_id - 1]['owner_members'].sort()

    return {}
