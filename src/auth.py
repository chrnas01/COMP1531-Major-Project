'''
functions for authentication of user
'''
import re
from error import InputError, AccessError
import other
import string
import random
import smtplib

def auth_login(email, password):
    '''
    Given a registered users' email and password and generates a valid
    token for the user to remain authenticated
    '''
    password = other.password_encrypt(password)
    # is email format valid
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError('Email not of valid format - Cannot login')

    # email is registered
    u_id = is_email_registered(email)
    if not is_email_registered(email):
        raise InputError('Email is not registered - Cannot login')

    # password is correct
    if not is_password_correct(u_id, password):
        raise InputError('Password is incorrect - Cannot login')

    # calculate token
    token = other.encrypt_token(u_id).decode("utf-8")

    other.update_user_reacts(u_id)

    return {
        'u_id': u_id,
        'token': token
    }

# provided a token, determines if logout is_success
def auth_logout(token):
    '''
    Given an active token, invalidates the token to log the user out.
    If a valid token is given, and the user is successfully logged out,
    it returns true, otherwise false.
    '''

    for user in other.data['users']:
        if user['token'] == token:
            return {'is_success': True}
    return {'is_success': False}

def auth_register(email, password, name_first, name_last):
    '''
    Given a user's first and last name, email address, and password,
    create a new account for them and return a new token for
    authentication in their session. A handle is generated that is the
    concatentation of a lowercase-only first name and last name. If the
    concatenation is longer than 20 characters, it is cutoff at 20 characters.
    If the handle is already taken, you may modify the handle in any way you
    see fit to make it unique.
    '''
    
    # is email format valid
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError('Email not of valid format - Cannot register')

    # password valid length
    if len(password) < 6:
        raise InputError('length of password is invalid - Cannot register')

    # name_first valid length
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('length of first name is invalid - Cannot register')

    # name_last valid length
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('length of last name is invalid - Cannot register')

    # check if already registered email
    if is_email_registered(email):
        raise InputError('Email is already registered - Cannot register')
    
    password = other.password_encrypt(password)
    
    # register
    if not other.data['users']:
        u_id = 1
    else:
        u_id = other.data['users'][-1]['u_id'] + 1 # first person u_id 1, second 2,...

    token = other.encrypt_token(u_id).decode("utf-8")

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
        handle_str = handle_str[:20 - len(str(u_id))]
        handle_str = handle_str + str(u_id)

    new_register = {
        'u_id': u_id,
        'token': token,
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle_str,
        'profile_img_url': '',
        'permission_id': 1 if u_id == 1 else 2 # flockr owner for first person registered 
    }

    other.data['users'].append(new_register)

    return {
        'u_id': u_id,
        'token': token
    }

def is_email_registered(email):
    '''
    given an email, check if it is already registered
    '''
    for user in other.data['users']:
        if user['email'] == email:
            return user['u_id']
    return False

def is_password_correct(u_id, password):
    '''
    given u_id and password, check if they match the user
    '''
    # index 0 holds u_id 1
    if other.data['users'][u_id - 1]['password'] == password:
        return True
    return False

def auth_password_request(email):
    '''
    Request a change in password
    '''
    # What if email is not registered
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls() 
    s.login("comp1531dummyemailingbot@gmail.com", "COMP1531Rules") 
    s.sendmail("comp1531dummyemailingbot@gmail.com", email, code) 
    s.quit()

    # New reset_code:
    new_reset_details = {
        'email': email,
        'code': code
    }

    other.data['reset_codes'].append(new_reset_details)
    return {}

def auth_password_reset(reset_code, new_password):
    '''
    Reset password
    '''
    if not is_reset_code_valid(reset_code):
        raise InputError('reset_code is invalid')
    
    # password valid length
    if len(new_password) < 6:
        raise InputError('length of password is invalid - Cannot register')

    user_email = is_reset_code_valid(reset_code)

    user_to_delete = {
        'code': reset_code,
        'email': user_email
    }
    other.data['reset_codes'].remove(user_to_delete)

    for user in other.data['users']:
        if user['email'] == user_email:
            user['password'] = other.password_encrypt(new_password)

    return {}

def is_reset_code_valid(given_code):
    '''
    Check that is_reset code is valid
    '''
    for reset_user in other.data['reset_codes']:
        if reset_user['code'] == given_code:
            return reset_user['email']
    return False
