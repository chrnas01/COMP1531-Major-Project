'''
This File will hold the standup functions.
'''

from datetime import datetime, timezone
from error import InputError, AccessError
import other

def standup_start(token, channel_id, length):
    '''
    For a given channel, start the standup period whereby for the next "length" seconds if
    someone calls "standup_send" with a message,
    it is buffered during the X second window then at the end of the X second window a message
    will be added to the message queue in the
    channel from the user who started the standup. X is an integer that denotes the number of
    seconds that the standup occurs for
    '''
    # Token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    # Check if channel is valid
    if not any(channels['channel_id'] == channel_id for channels in other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    # Check if an active standup is currently running on this channel
    if standup_active(token, channel_id)['is_active']:
        raise InputError('An active standup is currently running in this channel')

    current_time = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

    other.data['standup'].append({
        'token': token,
        'channel_id': channel_id,
        'time_finish': current_time + length,
        'is_active': True,
        'message': [],
        'sent': False
    })

    # Removes Completed Standup
    standup = {}
    for standup in other.data['standup']:
        if standup['channel_id'] == channel_id:
            break

    if standup['time_finish'] <= current_time:
        other.data['standup'].remove(standup)

    return {
        'time_finish': other.data['standup'][-1]['time_finish']   # Access last element of list
    }

def standup_active(token, channel_id):
    '''
    For a given channel, return whether a standup is active in it, and what time
    the standup finishes. If no standup is active, then time_finish returns None.
    '''
    # Token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    # Check if channel is valid
    if not any(channels['channel_id'] == channel_id for channels in other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    # Find which element the standup of interest is
    standup_exists = False
    standup = {}
    for standup in other.data['standup']:
        if standup['channel_id'] == channel_id:
            standup_exists = True
            break

    # No standup is active return None
    if not standup_exists:
        return {
            'is_active': False,
            'time_finish': None
        }

    # Testing if standup period is still in progress
    if int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) >= standup['time_finish']:
        standup['is_active'] = False

    return {
        'is_active': standup['is_active'],
        'time_finish': standup['time_finish']
    }

def standup_send(token, channel_id, message):
    '''
    Sending a message to get buffered in the standup queue, assuming a standup is currently active
    '''

    # Token is invalid
    if other.token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    # Check if channel is valid
    if not any(channels['channel_id'] == channel_id for channels in other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    # Check if message length is more than 1000 characters
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')

    # Check if there is an active standup running in this channel
    if not standup_active(token, channel_id)['is_active']:
        raise InputError('An active standup is not currently running in this channel')

    # Check if the authorised user is a member of the channel
    for channel in other.data['channels']:
        if channel_id == channel['channel_id']:
            if other.token_to_uid(token) not in channel['all_members']:
                raise AccessError('''The authorised user is not a memeber of the channel
                        that the message is within''')

    # Iterates to user handle string
    user = {}
    for user in other.data['users']:
        if user['token'] == token:
            break

    standup_msg = user['handle_str'] + ': ' + message + '\n'

    standup = {}
    for standup in other.data['standup']:
        if standup['channel_id'] == channel_id:
            break

    standup['message'].append(standup_msg)

    return {}
