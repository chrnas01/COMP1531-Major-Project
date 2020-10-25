'''
Contains miscellaneous functions
'''
import auth
import channels
import jwt
import hashlib
from error import InputError, AccessError
import channels


data = {
    'users': [],
    'channels': [],
    'messages': []
}


def clear():
    '''
    Resets databse
    '''
    data['users'].clear()
    data['channels'].clear()
    data['messages'].clear()
    return {}


def users_all(token):
    '''
    Given token returns a dictionary with of users
    '''
    
    return {'users': data['users']}


def admin_userpermission_change(token, u_id, permission_id):
    '''
    Given token, u_id and permission_id, changes flockr admin perms
    '''
    # The authorised user is not an owner
    for user in data['users']:
        if user['u_id'] == token_to_uid(token):
            if user['permission_id'] != 1:
                raise AccessError('The authorised user is not an owner')

    for user in data['users']:
        if user['u_id'] == u_id:
            # Not 0 or 1
            if permission_id not in range(1, 3):
                raise InputError(
                    'permission_id does not refer to a value permission')

            user['permission_id'] = permission_id
            break
    else:
        raise InputError('u_id does not refer to a valid user')

    return {}


def search(token, query_str):
    '''
    Given a query string, return a collection of messages in all of
    the channels that the user has joined that match the query
    '''

    messages = []
    user_channels = channels.channels_list(token)

    for msg in data['messages']:
        if any(channel['channel_id'] == msg['channel_id'] for channel in user_channels['channels']):
            if query_str in msg['message']:
                messages.append(msg)

    return {
        'messages': messages
    }

# Coverts the users token to a valid user_id
def token_to_uid(token):
    '''
    Given token, returns u_id
    '''
    for user in data['users']:
        if user['token'] == token:
            return user['u_id']
    else:
        return -1 

def password_encrypt(password):
    encrypted_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return encrypted_password

def encrypt_token(u_id):
    SECRET = 'IOAE@*#)_IEI@#U()IOJF}_@w30p}"ASDAP9*&@*_!$^_$983y17ae1)(#&@!)wed2891ydhaq;sd'
    encrypted_token = jwt.encode({'token': u_id}, SECRET, "HS256")
    return encrypted_token

def is_empty():
    if data['users']:
        return False
    if data['channels']:
        return False
    if data['messages']:
        return False
    return True

def check_if_flockr_owner(u_id):
    '''
    Checks if the given u_id is a global admin
    '''
    for user in data['users']:
        if user['u_id'] == u_id:
            if user['permission_id'] == 1:
                return True

    return False

def valid_user(u_id):
    '''
    Checks if the given u_id is a valid user
    '''
    for user in data['users']:
        if user['u_id'] == u_id:
            return True
    return False

def get_user_handle_strs():
    '''
    Get all handle strs
    '''
    ret = []
    for user in data['users']:
        ret.append(user['handle_str'])
    return ret

def is_successful_in_change_permissions(user_1, user_2):
    '''
    Check that permissions were changed
    '''
    successful = False
    for user in data['users']:
        if user['u_id'] == user_2['u_id']:
            if user['permission_id'] == 1:
                successful = True
    return {'successful': successful}
