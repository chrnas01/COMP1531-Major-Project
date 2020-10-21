import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError, AccessError
import re
import auth
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

    data = request.get_json()
    return dumps(auth.auth_login(data['email'], data['password']))

# auth logout
@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    '''
    Given an active token, invalidates the token to log the user out.
    If a valid token is given, and the user is successfully logged out,
    it returns true, otherwise false.
    '''
    data = request.get_json()
    return dumps(auth.auth_logout(data['token']))

# auth register
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
    data = request.get_json()
    return dumps(auth.auth_register(data['email'], data['password'], data['name_first'], data['name_last']))

@APP.route("/clear", methods=['DELETE'])
def other_clear():
    '''
    Clear database
    '''
    other.clear()


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
