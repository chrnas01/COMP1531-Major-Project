import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError, AccessError
import re
from auth import is_email_registered, is_password_correct
import other

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# auth login
@APP.route("/auth/login", methods=['POST'])
def auth_login():

    email = request.get_json('email')
    password = request.get_json('password')

    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError(description='Email not of valid format - Cannot login')

    # email is registered
    u_id = is_email_registered(email)
    if not is_email_registered(email):
        raise InputError(description='Email is not registered - Cannot login')

    # password is correct
    if not is_password_correct(u_id, password):
        raise InputError(description='Password is incorrect - Cannot login')

    token = other.encrypt_token(u_id)
    
    return dumps({
        'u_id': u_id,
        'token': token
    })

@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    '''
    Given an active token, invalidates the token to log the user out.
    If a valid token is given, and the user is successfully logged out,
    it returns true, otherwise false.
    '''
    token = request.get_json('token')
    for user in other.data['users']:
        if user['token'] == token:
            return dumps({'is_success': True})
    return dumps({'is_success': False})

@APP.route("/auth/register", methods=['POST'])
def auth_register():
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
    email = request.get_json('email')
    password = request.get_json('password')
    name_first = request.get_json('name_first')
    name_last = request.get_json('name_last')
    
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError(description='Email not of valid format - Cannot register')

    # password valid length
    if len(password) < 6:
        raise InputError(description='length of password is invalid - Cannot register')

    # name_first valid length
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='length of first name is invalid - Cannot register')

    # name_last valid length
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description='length of last name is invalid - Cannot register')

    # check if already registered email
    if is_email_registered(email):
        raise InputError(description='Email is already registered - Cannot register')

    # register
    u_id = len(other.data['users']) + 1 # first person u_id 1, second 2,...
    token = other.encrypt_token(u_id)

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

    return dumps({
        'u_id': u_id,
        'token': token
    })


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
