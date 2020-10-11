'''
functions to manage channels
'''
from error import InputError
import other

# Provide a list of all channels (and their associated details)
# that the authorised user is part of:
def channels_list(token):
    '''
    Provide a list of all channels (and their associated details)
    that the authorised user is part of
    '''
    # User of interest
    user_uid = other.token_to_uid(token)
    # Total number of channels
    total_channels = len(other.data['channels'])
    # Output (Mimics data stucture already put in place)
    user_channels = []

    for i in range(total_channels):
        if user_uid in other.data['channels'][i]['all_members']:
            user_channels.append(other.data['channels'][i])

    return {'channels': user_channels}


# Provide a list of all channels (and their associated details)
def channels_listall(token):
    '''
    Provide a list of all channels (and their associated details)
    '''
    other.token_to_uid(token)
    # Simply returns data structure which stores all channels information.
    return {'channels': other.data['channels']}

# Creates a new channel with that name that is either
# a public or private channel
def channels_create(token, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private channel
    '''
    # First check to see if inputted name is valid:
    # Cannot be greater than 20 characters long
    if len(name) > 20:
        raise InputError('Channel name is greater than 20 characters long - Cannot create channel')
    # Cannot be left blank
    if len(name) == 0:
        raise InputError('Field, "Channel name" left blank - Cannot create channel')
    # Name cannot already exist
    total_channels = len(other.data['channels'])
    for i in range(total_channels):
        if name in other.data['channels'][i]['channel_name']:
            raise InputError('Channel name already exists - Cannot create channel')

    # Testing if this is the first channel being created.
    if not other.data['channels']:
        channel_id = 1
    else:
        channel_id = len(other.data['channels'])

    new_channel = {
        'channel_name': name,
        'channel_id': channel_id,
        'is_public': is_public,
        'owner_members': [other.token_to_uid(token),],
        'all_members': [other.token_to_uid(token),],
    }

    other.data['channels'].append(new_channel)

    return {'channel_id': channel_id}
