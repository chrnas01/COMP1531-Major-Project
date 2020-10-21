'''
Contains miscellaneous functions
'''
import auth
import channels
import jwt
import hashlib
from error import InputError, AccessError


data = {
    'users': [],
    'channels': [],
    'messages': [],
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
            if permission_id not in range(0, 2):
                raise InputError(
                    'permission_id does not refer to a value permission')

            user['permission_id'] = permission_id
            break
    else:
        raise InputError('u_id does not refer to a valid user')

    return {}


def search(token, query_str):
    '''
    Given a token and query_str searches for a message
    '''
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
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

def decrypt_token(encrypted_token):
    SECRET = 'IOAE@*#)_IEI@#U()IOJF}_@w30p}"ASDAP9*&@*_!$^_$983y17ae1)(#&@!)wed2891ydhaq;sd'
    decrypted_token = jwt.decode(encrypted_token, SECRET, "HS256")
    return decrypted_token

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