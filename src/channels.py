from error import InputError
import auth 

data = {
    'channels': [

    ]   
}

# Provide a list of all channels 
# (and their associated details) that the authorised user is part of
# Return type: { channels }
def channels_list(token):
    # User of interest
    user_uid = token_to_uid(token)
    # Total number of channels  
    total_channels = len(data['channels'])
    # Output 
    user_channels = {
                'channels': [],
            }
    
     for i in range(total_channels):
        if user_uid in data['channels'][i]['all_members']
            user_channels['channels'].append(data['channels'][i])
            
    return user_channels


# Provide a list of all channels (and their associated details)
# Return type { channels }
def channels_listall(token):
    return data

# Assumption channel name cannot be left blank
# Creates a new channel with that name that is either 
# a public or private channel
# Input Error: When name is more than 20 characters long 
# Return type: { channel id }
def channels_create(token, name, is_public):
    # First check to see if inputted name is valid:
    if len(name) > 20 
        raise InputError('Channel name is greater than 20 characters long - Cannot create channel')
    
    if not data['channels']: 
        channel_id = 1 
    else:
        channel_id = len(data['channels'])

    # Assumtpion: When a channel is created the creator becomes owner by default 
    new_channel = {
            'channel_name': name,  
            'channel_id': channel_id,
            'is_public': is_public,
            'owner_members': [token_to_uid(token),],
            'all_members': [],
    }   

    data['channels'].append(new_channel)
   
    return {
        'channel_id': channel_id,
    }



def token_to_uid(token):
    for user in all_users:
        if user['token'] == token:
            return user['u_id']
    else:
        return -1 

def delete_data():
    data['channels'].clear()
    return