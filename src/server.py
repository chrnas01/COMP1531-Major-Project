import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
import channel
from error import InputError, AccessError
import channels
import auth 
import re
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

@APP.route("/channel/invite", methods=['POST'])
def http_channel_invite():
    data = request.get_json()
    return dumps(channel.channel_invite(data['token'], data['channel_id'], data['u_id']))

@APP.route("/channel/details", methods=['GET'])
def http_channel_details():
    data = request.get_json()
    return dumps(channel.channel_details(data['token'], data['channel_id']))

####################
# CHANNEL MESSAGES
####################

@APP.route("/channel/leave", methods=['POST'])
def http_channel_leave():
    data = request.get_json()
    return dumps(channel.channel_leave(data['token'], data['channel_id']))

@APP.route("/channel/join", methods=['POST'])
def http_channel_join():
    data = request.get_json()
    return dumps(channel.channel_join(data['token'], data['channel_id']))

@APP.route("/channel/addowner", methods=['POST'])
def httpchannel_addowner():
    data = request.get_json()
    return dumps(channel.channel_addowner(data['token'], data['channel_id'], data['u_id']))

@APP.route("/channel/removeowner", methods=['POST'])
def http_channel_removeowner():
    data = request.get_json()
    return dumps(channel.channel_removeowner(data['token'], data['channel_id'], data['u_id']))
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

@APP.route("/admin/userpermission/change", methods=['POST'])
def admin_userpermission_change():
    '''
    Change permissions
    '''
    data = request.get_json()
    return other.admin_userpermission_change(data['token'], data['u_id'], data['permission_id'])

@APP.route("/other/successful/permissions", methods=['POST'])
def other_if_successful_permission():
    '''
    Check if permission change was successful
    '''
    data = request.get_json()
    return dumps(other.is_successful_in_change_permissions(data['user_1'], data['user_2']))

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
@APP.route('/other/show', methods=['GET'])
def show():
    '''
    shows
    '''
    return dumps(other.data)

@APP.route('/other/is_empty', methods=['GET'])
def show_is_empty():
    '''
    shows if empty
    '''
    return dumps(other.is_empty())

@APP.route('/other/show/handle_str', methods=['GET'])
def show_handle_strs():
    '''
    shows handle strings
    '''
    return dumps(other.get_user_handle_strs())


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
