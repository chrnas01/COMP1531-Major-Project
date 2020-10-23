import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import channels
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
    return dumps(other.clear())


# channels_list 
@APP.route("/channels/list", methods = ['GET'])
def channels_list():
    data = request.get_json()
    return dumps(channels.channels_list(data['token']))

# channels_listall 
@APP.route("/channels/listall", methods = ['GET'])
def channels_listall(): 
    data = request.get_json()
    return dumps(channels.channels_listall(data['token']))

# channels_create 
@APP.route("/channels/create", methods = ['POST'])
def channels_create(): 
    data = request.get_json()
    return dumps(channels.channels_create(data['token'], data['name'], data['is_public']))

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
