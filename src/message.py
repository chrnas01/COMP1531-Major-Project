from datetime import datetime, timezone
import time
from error import InputError, AccessError
import other
import channels
import auth

def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id
    '''
    #token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    # Check that the user is a member of the channel
    if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['all_members']:
        raise AccessError('Authorised user is not a member of channel with channel_id')

    # Check that the message is within the character limit
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')

    if not other.data['messages']:
        message_id = 1
    else:
        #new message_id will be the highest id + 1
        message_id = other.data['messages'][-1]['message_id'] + 1

    message_struct = {
        'message_id': message_id,
        'channel_id': channel_id,
        'u_id': other.token_to_uid(token),
        'message': message,
        'time_created': int(datetime.now().replace(tzinfo=timezone.utc).timestamp()),
        'reacts': other.valid_reacts,
        'is_pinned': False
    }

    other.data['messages'].append(message_struct)

    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    '''
    Given a message_id for a message, this message is removed from the channel
    '''
    #token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    msg_exist = False

    msg = {}

    for msg in other.data['messages']:
        if msg['message_id'] == message_id:
            msg_exist = True
            break

    #check if the message exists
    if not msg_exist:
        raise InputError('Message (based on ID) no longer exists')

    #check they are deleting their own message
    if msg['u_id'] != other.token_to_uid(token):
        raise AccessError('''Message with message_id was not sent by
                 the authorised user making this request''')

    #check if they are a channel owner
    #check if they are a channel or flockr owner
    if not other.check_if_flockr_owner(other.token_to_uid(token)):
        if other.token_to_uid(token) not in other.data['channels'][
                msg['channel_id'] - 1]['owner_members']:
            raise AccessError('The authorised user is not an owner of this channel or the flockr')

    other.data['messages'].remove(msg)

    return {
    }

def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text.
    If the new message is an empty string, the message is deleted.
    '''
    #token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    msg = {}

    for msg in other.data['messages']:
        if msg['message_id'] == message_id:
            break

    #check they are deleting their own message
    if msg['u_id'] != other.token_to_uid(token):
        raise AccessError('''Message with message_id was not sent
                 by the authorised user making this request''')

    #check if they are a channel or flockr owner
    if not other.check_if_flockr_owner(other.token_to_uid(token)):
        if other.token_to_uid(token) not in other.data['channels'][msg['channel_id'] - 1]['owner_members']:
            raise AccessError('The authorised user is not an owner of this channel or the flockr')

    if not message:
        message_remove(token, message_id)
    else:
        msg['message'] = message

    return {
    }

def message_send_later(token, channel_id, message, time_sent):
    '''
    Send a message from authorised_user to the channel specified by channel_id
    at a specific time
    '''
    #token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    # Check for channel_id exists
    if channel_id > len(other.data['channels']):
        raise InputError('channel_id does not refer to a valid channel')

    # Check that the message is within the character limit
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')

    # Check that the time sent is not in the past
    curr_time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    if time_sent < curr_time:
        raise InputError('Time sent is a time in the past')

    # Check that the user is a member of the channel
    if other.token_to_uid(token) not in other.data['channels'][channel_id - 1]['all_members']:
        raise AccessError('Authorised user is not a member of channel with channel_id')

    if not other.data['messages']:
        message_id = 1
    else:
        #new message_id will be the highest id + 1
        message_id = other.data['messages'][-1]['message_id'] + 1

    message_struct = {
        'message_id': message_id,
        'channel_id': channel_id,
        'u_id': other.token_to_uid(token),
        'message': message,
        'time_created': time_sent,
        'reacts': other.valid_reacts,
        'is_pinned': False
    }

    other.data['messages'].append(message_struct)

    return {
        'message_id': message_id,
    }

def message_react(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of,
    add a "react" to that particular message
    '''
    #token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    msg = {}

    for msg in other.data['messages']:
        if msg['message_id'] == message_id:
            break
    
    # Check that the user is a member of the channel in which the message was sent
    if other.token_to_uid(token) not in other.data['channels'][msg['channel_id'] - 1]['all_members']:
        raise InputError('message_id is not a valid message within a channel that the authorised user has joined')

    # Check that the react is valid
    if all(react_id != react['react_id'] for react in other.valid_reacts):
        raise InputError('react_id is not a valid React ID')
    
    if msg['reacts'][0]['is_this_user_reacted']:
        print('test')
        raise InputError('''Message with ID message_id already contains an active 
                React with ID react_id from the authorised user''')

    for react in msg['reacts']:
        if react['react_id'] == react_id:
            react['u_ids'].append(other.token_to_uid(token))
            react['is_this_user_reacted'] = True
            break

    return {}

def message_unreact(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of,
    remove a "react" to that particular message
    '''
    #token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    msg = {}

    for msg in other.data['messages']:
        if msg['message_id'] == message_id:
            break

    # Check that the user is a member of the channel in which the message was sent
    if other.token_to_uid(token) not in other.data['channels'][msg['channel_id'] - 1]['all_members']:
        raise InputError('message_id is not a valid message within a channel that the authorised user has joined')

    # Check that the react is valid
    if all(react_id != react['react_id'] for react in other.valid_reacts):
        raise InputError('react_id is not a valid React ID')

    if not msg['reacts'][0]['is_this_user_reacted']:
        raise InputError('''Message with ID message_id does not 
                contain an active React with ID react_id''')

    for react in msg['reacts']:
        if react['react_id'] == react_id:
            react['u_ids'].remove(other.token_to_uid(token))
            react['is_this_user_reacted'] = False
            break

    return {}

def message_pin(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to be given special
    display treatment by the frontend
    '''
    #token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    msg_exist = False

    msg = {}

    for msg in other.data['messages']:
        if msg['message_id'] == message_id:
            msg_exist = True
            break

    #check if the message exists
    if not msg_exist:
        raise InputError('message_id is not a valid message')

    if msg['is_pinned']:
        raise InputError('Message with ID message_id is already pinned')

    # Check that the user is a member of the channel in which the message was sent
    if other.token_to_uid(token) not in other.data['channels'][msg['channel_id'] - 1]['all_members']:
        raise AccessError('message_id is not a valid message within a channel that the authorised user has joined')

    #check if they are a channel or flockr owner
    if not other.check_if_flockr_owner(other.token_to_uid(token)):
        if other.token_to_uid(token) not in other.data['channels'][msg['channel_id'] - 1]['owner_members']:
            raise AccessError('The authorised user is not an owner of this channel or the flockr')
    
    msg['is_pinned'] = True

    return {}

def message_unpin(token, message_id):
    '''
    Given a message within a channel, remove it's mark as unpinned
    '''
    #token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    msg_exist = False

    msg = {}

    for msg in other.data['messages']:
        if msg['message_id'] == message_id:
            msg_exist = True
            break

    #check if the message exists
    if not msg_exist:
        raise InputError('message_id is not a valid message')

    if not msg['is_pinned']:
        raise InputError('Message with ID message_id is already unpinned')

    # Check that the user is a member of the channel in which the message was sent
    if other.token_to_uid(token) not in other.data['channels'][msg['channel_id'] - 1]['all_members']:
        raise AccessError('message_id is not a valid message within a channel that the authorised user has joined')

    #check if they are a channel or flockr owner
    if not other.check_if_flockr_owner(other.token_to_uid(token)):
        if other.token_to_uid(token) not in other.data['channels'][msg['channel_id'] - 1]['owner_members']:
            raise AccessError('The authorised user is not an owner of this channel or the flockr')
    
    msg['is_pinned'] = False

    return {}