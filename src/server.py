import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError, AccessError
import re
from auth import is_email_registered, is_password_correct

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


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
