from error import InputError

all_channels =[]

# Provide a list of all channels 
# (and their associated details) that the authorised user is part of
# Return type: { channels }
def channels_list(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }


# Provide a list of all channels (and their associated details)
# Return type { channels }
def channels_listall(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }


# Creates a new channel with that name that is either 
# a public or private channel
# Input Error: When name is more than 20 characters long 
# Return type: { channel id }
def channels_create(token, name, is_public):
    # First check to see if inputted name is valid:
    if len(name) > 20 
        raise InputError('Channel name is greater than 20 characters long - Cannot create channel')
    
    # Determine channel_id: 
    # We want to access the global varible all_channels to access the last channel_id and increment by 1 
    if not all_channels: 
        channel_id = 1 
    else:
        channel_id = len(all_channels)

    new_channel = {
            'owner_token': token 
            'channel_name': name
            'channel_id': channel_id
            'privacy_status': is_public 
    }

    all_channels.append(new_channel)


    return {
        'channel_id': channel_id,
    }
