import re
from error import InputError

all_users = []

# input email and password
def auth_login(email, password):
    return {
        'u_id': 1,
        'token': 1,
    }

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    # is valid email
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError('Email not of valid format')

    # password valid length
    elif len(password) < 6:
        raise InputError('length of password is invalid')

    # name_first valid length
    elif len(name_first) < 1 or len(name_first) > 50:
        raise InputError('length of first name is invalid')
    
    # name_last valid length
    elif len(name_last) < 1 or len(name_last) > 50:
        raise InputError('length of last name is invalid')

    # check if already registered email
    elif email_registered(email):
        raise InputError('Email is already registered')

    # Part not clear - Need to double check concatenation
    # register
    u_id = len(all_users) + 1 # First person u_id 1, second 2,...
    token = u_id
    new_register = {'u_id': u_id, 'token': token, 'email': email, 'password': password, 'name_first': name_first, 'name_last': name_last,}
    all_users.append(new_register)

    return {
        'u_id': u_id,
        'token': token,
    }

def email_registered(email):
    for user in all_users:
        if user['email'] == email:
            return True
    return False


def delete_users():
    all_users.clear()
    return

def auth_password_correct(email, password):
    pass