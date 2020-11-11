'''
This File will hold the standup functions.
'''

from datetime import datetime, timedelta
from error import InputError, AccessError
import other

standup_data = []

def standup_start(token, channel_id, length):
    '''
    For a given channel, start the standup period whereby for the next "length" seconds if
    someone calls "standup_send" with a message,
    it is buffered during the X second window then at the end of the X second window a message
    will be added to the message queue in the
    channel from the user who started the standup. X is an integer that denotes the number of
    seconds that the standup occurs for
    '''

    # Check if channel is valid
    if not any(channels['channel_id'] == channel_id for channels in other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    # Check if an active standup is currently running on this channel
    if standup_active(token, channel_id)['is_active']:
        raise InputError('An active standup is currently running in this channel')

    standup_data.append({
        'channel_id': channel_id,
        'time_finish': datetime.now() + timedelta(seconds=length),
        'is_active': True,
        'msg_queue': []
    })

    return {
        'time_finish': standup_data[-1]['time_finish']   # Access last element of list
    }

def standup_active(token, channel_id):
    '''
    For a given channel, return whether a standup is active in it, and what time
    the standup finishes. If no standup is active, then time_finish returns None.
    '''

    # Check if channel is valid
    if not any(channels['channel_id'] == channel_id for channels in other.data['channels']):
        raise InputError('Channel ID is not a valid channel')

    # Find which element the standup of interest is
    index = -1
    for j in range(0, len(standup_data)):
        if standup_data[j]['channel_id'] == channel_id:
            index = j

    # No standup is active return None
    if index == -1:
        return {
            'is_active': False,
            'time_finish': None
        }

    # Testing if standup period is still in progress
    if datetime.now() >= standup_data[index]['time_finish']:
        standup_data[index]['is_active'] = False


    return {
        'is_active': standup_data[index]['is_active'],
        'time_finish': standup_data[index]['time_finish']
    }

def standup_send(token, channel_id, message):
    '''
    Sending a message to get buffered in the standup queue, assuming a standup is currently active
    '''

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
                raise AccessError('The authorised user is not a memeber of the channel that the message is within')

    return {}
