import other
import re
import auth
from error import InputError, AccessError

def user_profile(token, u_id):
    # Check that the token is valid
    if other.token_to_uid(token) <= 0:
        raise AccessError("user_profile bad token")
    
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
    else: 
        raise InputError('u_id does not refer to a valid user')



def user_profile_setname(token, name_first, name_last):
    current_user = other.token_to_uid(token)
    # Check that the token is valid
    if current_user <= 0:
        raise AccessError("user_profile_setname bad token")

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
    else: 
        raise InputError('u_id does not refer to a valid user')            

    return {
    }

def user_profile_setemail(token, email):
    current_user = other.token_to_uid(token)
    # Check that the token is valid
    if current_user <= 0:
        raise AccessError("user_profile_setemail bad token")

    # is email format valid
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError('Email not of valid format - Cannot register')

    # check if already registered email
    elif auth.is_email_registered(email):
        raise InputError('Email is already registered - Cannot register')

    for user in other.data['users']:
        if user['u_id'] == current_user:
            user['email'] = email
            break
    else: 
        raise InputError('u_id does not refer to a valid user')            

    return {
    }

def user_profile_sethandle(token, handle_str):
    current_user = other.token_to_uid(token)
    # Check that the token is valid
    if current_user <= 0:
        raise AccessError("user_profile_sethandle bad token")

    handle_exists = False

    # Make handle unique
    if other.data['users']:
        for user in other.data['users']:
            handle = user.get('handle_str')
            #check if handle exists
            if handle_str == handle:
                handle_exists = True
    
    if handle_exists:
        handle_str = handle_str + str(current_user)

    for user in other.data['users']:
        if user['u_id'] == current_user:
            user['handle_str'] = handle_str
            break
    else: 
        raise InputError('u_id does not refer to a valid user')            

    return {
    }