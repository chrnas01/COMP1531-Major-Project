'''
Contains miscellaneous functions
'''
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

    return -1


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
