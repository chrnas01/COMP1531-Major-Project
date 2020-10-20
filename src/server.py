import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import channel

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
    token = request.get_json('token')
    channel_id = int(request.get_json('channel_id'))
    u_id = int(request.get_json('u_id'))

    return dumps(channel.channel_invite(token, channel_id, u_id))

@APP.route("/channel/details", methods=['GET'])
def http_channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    return dumps(channel.channel_details(token, channel_id))

####################
# CHANNEL MESSAGES
####################

@APP.route("/channel/leave", methods=['POST'])
def http_channel_leave():
    token = request.get_json('token')
    channel_id = int(request.get_json('channel_id'))

    return dumps(channel.channel_leave(token, channel_id))

@APP.route("/channel/join", methods=['POST'])
def http_channel_join():
    token = request.get_json('token')
    channel_id = int(request.get_json('channel_id'))

    return dumps(channel.channel_join(token, channel_id))

@APP.route("/channel_addowner", methods=['POST'])
def httpchannel_addowner():
    token = request.get_json('token')
    channel_id = int(request.get_json('channel_id'))
    u_id = int(request.get_json('u_id'))

    return dumps(channel.channel_addowner(token, channel_id, u_id))

@APP.route("/channel_removeowner", methods=['POST'])
def http_channel_removeowner():
    token = request.get_json('token')
    channel_id = int(request.get_json('channel_id'))
    u_id = int(request.get_json('u_id'))

    return dumps(channel.channel_removeowner(token, channel_id, u_id))


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
