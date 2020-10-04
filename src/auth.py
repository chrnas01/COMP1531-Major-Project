import re
from error import InputError
import other


# input email and password
def auth_login(email, password):
    # is email format valid
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError('Email not of valid format - Cannot login')

    # email is registered
    u_id = is_email_registered(email)
    if not is_email_registered(email):
        raise InputError('Email is not registered - Cannot login')

    # password is correct
    elif not is_password_correct(u_id, password):
        raise InputError('Password is incorrect - Cannot login')

    # calculate token
    token = email

    return {
        'u_id': u_id,
        'token': token,
    }

# provided a token, determines if logout is_success
def auth_logout(token):
    for user in other.data['users']:
        if user['token'] == token:
            return {
                'is_success': True,
            }
    return {
        'is_success': False,
    }

# provided email, password, name_first, name_last
# validate no input error was made
# return u_id and token
def auth_register(email, password, name_first, name_last):
    # is email format valid
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError('Email not of valid format - Cannot register')

    # password valid length
    elif len(password) < 6:
        raise InputError('length of password is invalid - Cannot register')

    # name_first valid length
    elif len(name_first) < 1 or len(name_first) > 50:
        raise InputError('length of first name is invalid - Cannot register')
    
    # name_last valid length
    elif len(name_last) < 1 or len(name_last) > 50:
        raise InputError('length of last name is invalid - Cannot register')

    # check if already registered email
    elif is_email_registered(email):
        raise InputError('Email is already registered - Cannot register')

    # register
    u_id = len(other.data['users']) + 1 # first person u_id 1, second 2,...
    token = email # iteration 1, token is email

    # concatenate
    handle_str = name_first.lower() + name_last.lower()
    handle_str = handle_str[:20]
    handle_exists = False

    # Make handle unique
    if other.data['users']:
        for user in other.data['users']:
            handle = user.get('handle_str')
            #check if handle exists
            if handle_str == handle:
                handle_exists = True
    
    if handle_exists:
        handle_str = handle_str + str(u_id)

    new_register = {
        'u_id': u_id, 
        'token': token, 
        'email': email, 
        'password': password, 
        'name_first': name_first, 
        'name_last': name_last, 
        'handle_str': handle_str,
    }

    other.data['users'].append(new_register)
    
    return {
        'u_id': u_id,
        'token': token,
    }

# given an email, check if it is already registered
def is_email_registered(email):
    for user in other.data['users']:
        if user['email'] == email:
            return user['u_id']
    return False

# given u_id and password, check if they match the user
def is_password_correct(u_id, password):
    # index 0 holds u_id 1
    if other.data['users'][u_id - 1]['password'] == password:
        return True
    return False
