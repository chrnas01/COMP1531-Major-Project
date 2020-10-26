from datetime import datetime, timezone
from error import InputError, AccessError
import other

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
        'time_created': int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
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

    msg = {}
    msg_exist = False

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

    for i in range(len(other.data['messages'])):
        if other.data['messages'][i]['message_id'] == message_id:
            break

    #check they are deleting their own message
    if other.data['messages'][i]['u_id'] != other.token_to_uid(token):
        raise AccessError('''Message with message_id was not sent
                 by the authorised user making this request''')

    #check if they are a channel or flockr owner
    if not other.check_if_flockr_owner(other.token_to_uid(token)):
        if other.token_to_uid(token) not in other.data['channels'][
                    other.data['messages'][i]['channel_id'] - 1]['owner_members']:
            raise AccessError('The authorised user is not an owner of this channel or the flockr')

    if not message:
        message_remove(token, message_id)
    else:
        other.data['messages'][i]['message'] = message

    return {
    }
