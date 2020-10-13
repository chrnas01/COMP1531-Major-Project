'''
    contains functions that manipulate user data
'''
import re
import other
import auth
from error import InputError

def user_profile(_, u_id):
    '''
    Given a u_id it will return a dictionary of a user
    returning email, u_id first name last name and handle str
    '''

    # seach for uid
    for user in other.data['users']:
        if user['u_id'] == u_id:
            temp_dict = {
                'email': user['email'],
                'u_id': user['u_id'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
            }
            return {'user': temp_dict}

    # Didnt find the user
    raise InputError('u_id does not refer to a valid user')




def user_profile_setname(token, name_first, name_last):
    '''
    Given a first and last name,
    changes the first and last name of current user
    '''

    current_user = other.token_to_uid(token)

    # name_first valid length
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('length of first name is invalid - Cannot register')

    # name_last valid length
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('length of last name is invalid - Cannot register')

    for user in other.data['users']:
        if user['u_id'] == current_user:
            user['name_first'] = name_first
            user['name_last'] = name_last
            break


    return {
    }

def user_profile_setemail(token, email):
    '''
    Given email changed the email of the current user
    '''

    current_user = other.token_to_uid(token)

    # is email format valid
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError('Email not of valid format - Cannot register')

    # check if already registered email
    if auth.is_email_registered(email):
        raise InputError('Email is already registered - Cannot register')

    for user in other.data['users']:
        if user['u_id'] == current_user:
            user['email'] = email
            break


    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    Given handle string changed the handle_str of the current user
    '''

    current_user = other.token_to_uid(token)

    # handle_str must be between 3 and 20 characters not inclusive
    if len(handle_str) <= 3 or len(handle_str) >= 20:
        raise InputError('length of first name is invalid - Cannot register')



    # Make handle unique
    if other.data['users']:
        for user in other.data['users']:
            handle = user.get('handle_str')
            #check if handle exists
            if handle_str == handle:
                raise InputError('handle is already used by another user')
  

    for user in other.data['users']:
        if user['u_id'] == current_user:
            user['handle_str'] = handle_str
            break


    return {
    }
