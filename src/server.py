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
import user
import message

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
    return dumps(channel.channel_invite(data['token'], int(data['channel_id']), int(data['u_id'])))

@APP.route("/channel/details", methods=['GET'])
def http_channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    return dumps(channel.channel_details(token, channel_id))

####################

@APP.route("/channel/messages", methods=['GET'])
def http_channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return dumps(channel.channel_messages(token, channel_id, start))

####################

@APP.route("/channel/leave", methods=['POST'])
def http_channel_leave():
    data = request.get_json()
    return dumps(channel.channel_leave(data['token'], int(data['channel_id'])))

@APP.route("/channel/join", methods=['POST'])
def http_channel_join():
    data = request.get_json()
    return dumps(channel.channel_join(data['token'], int(data['channel_id'])))

@APP.route("/channel/addowner", methods=['POST'])
def http_channel_addowner():
    data = request.get_json()
    return dumps(channel.channel_addowner(data['token'], int(data['channel_id']), int(data['u_id'])))

@APP.route("/channel/removeowner", methods=['POST'])
def http_channel_removeowner():
    data = request.get_json()
    return dumps(channel.channel_removeowner(data['token'], int(data['channel_id']), int(data['u_id'])))

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
    return other.admin_userpermission_change(data['token'], int(data['u_id']), int(data['permission_id']))

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
    token = request.args.get('token')
    return dumps(channels.channels_list(token))

# channels_listall 
@APP.route("/channels/listall", methods = ['GET'])
def channels_listall(): 
    token = request.args.get('token')
    return dumps(channels.channels_listall(token))

# channels_create 
@APP.route("/channels/create", methods = ['POST'])
def channels_create(): 
    data = request.get_json()
    return dumps(channels.channels_create(data['token'], data['name'], data['is_public']))

@APP.route('/other/show', methods=['GET'])
def show():
    '''
    shows databse
    '''
    return dumps(other.data)

@APP.route('/other/is_empty', methods=['GET'])
def show_is_empty():
    '''
    shows if empty
    '''
    return dumps(other.is_empty())

@APP.route('/search', methods=['GET'])
def search():
    '''
    search
    '''
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(other.search(token, query_str))

@APP.route('/other/show/handle_str', methods=['GET'])
def show_handle_strs():
    '''
    shows handle strings
    '''
    return dumps(other.get_user_handle_strs())

@APP.route('/user/profile', methods=['GET'])
def user_profile():
    '''
    show user profile
    '''
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    return dumps(user.user_profile(token, u_id))

@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname():
    '''
    change user's name
    '''
    data = request.get_json()
    return dumps(user.user_profile_setname(data['token'], data['name_first'], data['name_last']))

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_setemail():
    '''
    change user's email
    '''
    data = request.get_json()
    return dumps(user.user_profile_setemail(data['token'], data['email']))

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    '''
    change user's handlestr
    '''
    data = request.get_json()
    return dumps(user.user_profile_sethandle(data['token'], data['handle_str']))

@APP.route('/users/all', methods=['GET'])
def users_all():
    '''
    show a list of all users and their associated details
    '''
    token = request.args.get('token')
    return dumps(other.users_all(token))

@APP.route('/message/send', methods=['POST'])
def http_message_send():
    data = request.get_json()
    return dumps(message.message_send(data['token'], int(data['channel_id']), data['message']))

@APP.route('/message/remove', methods=['DELETE'])
def http_message_remove():
    data = request.get_json()
    return dumps(message.message_remove(data['token'], int(data['message_id'])))

@APP.route('/message/edit', methods=['PUT'])
def http_message_edit():
    data = request.get_json()
    return dumps(message.message_edit(data['token'], int(data['message_id']), data['message']))

@APP.route('/message/sendlater', methods=['POST'])
def http_message_send_later():
    data = request.get_json()
    return dumps(message.message_send_later(data['token'], int(data['channel_id']), data['message'], data['time_sent']))

@APP.route('/message/react', methods=['POST'])
def http_message_react():
    data = request.get_json()
    return dumps(message.message_react(data['token'], data['message_id'], data['react_id']))

@APP.route('/message/unreact', methods=['POST'])
def http_message_unreact():
    data = request.get_json()
    return dumps(message.message_unreact(data['token'], data['message_id'], data['react_id']))

@APP.route('/message/pin', methods=['POST'])
def http_message_pin():
    data = request.get_json()
    return dumps(message.message_pin(data['token'], data['message_id']))

@APP.route('/message/unpin', methods=['POST'])
def http_message_unpin():
    data = request.get_json()
    return dumps(message.message_unpin(data['token'], data['message_id']))


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
