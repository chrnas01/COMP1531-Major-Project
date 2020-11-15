'''
Contains miscellaneous functions
'''
from flask_mail import Mail, Message
import re
import auth
import channels
import jwt
import hashlib
from error import InputError, AccessError
import channels
import smtplib
import os
from server import APP


data = {
    'users': [],
    'channels': [],
    'messages': [],
    'standup': [],
    'reset_codes': []
}

# Only copy do not directly modify
valid_reacts = [
    {
        'react_id': 1,
        'u_ids': [],
        'is_this_user_reacted': False
    },
    {
        'react_id': 2,
        'u_ids': [],
        'is_this_user_reacted': False
    },
    {
        'react_id': 3,
        'u_ids': [],
        'is_this_user_reacted': False
    }
]


def clear():
    '''
    Resets database
    '''
    data['users'].clear()
    data['channels'].clear()
    data['messages'].clear()
    data['standup'].clear()
    data['reset_codes'].clear()

    global valid_reacts

    for react in valid_reacts:
        react['u_ids'] = []
        react['is_this_user_reacted'] = False

    return {}


def users_all(token):
    '''
    Given token returns a dictionary of users details
    '''
    #token is invalid
    if token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    new_list = []

    for u in data['users']:
        new_dict = {
            'u_id': u['u_id'],
            'email': u['email'],
            'name_first': u['name_first'],
            'name_last': u['name_last'],
            'handle_str': u['handle_str'],
            'profile_img_url': u['profile_img_url'],
        }
        new_list.append(new_dict)

    return {'users': new_list}


def admin_userpermission_change(token, u_id, permission_id):
    '''
    Given token, u_id and permission_id, changes flockr admin perms
    '''
    #token is invalid
    if token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    # The authorised user is not an owner
    for user in data['users']:
        if user['u_id'] == token_to_uid(token):
            if user['permission_id'] != 1:
                raise AccessError('The authorised user is not an owner')

    for user in data['users']:
        if user['u_id'] == u_id:
            # Not 0 or 1
            if permission_id not in range(1, 3):
                raise InputError(
                    'permission_id does not refer to a value permission')

            user['permission_id'] = permission_id
            break
    else:
        raise InputError('u_id does not refer to a valid user')

    return {}


def search(token, query_str):
    '''
    Given a query string, return a collection of messages in all of
    the channels that the user has joined that match the query
    '''
    #token is invalid
    if token_to_uid(token) == -1:
        raise AccessError('Invalid Token')

    messages = []
    user_channels = channels.channels_list(token)

    for msg in data['messages']:
        if any(channel['channel_id'] == msg['channel_id'] for channel in user_channels['channels']):
            if query_str in msg['message']:
                messages.append(msg)

    return {
        'messages': messages
    }

# Coverts the users token to a valid user_id


def token_to_uid(token):
    '''
    Given token, returns u_id
    '''
    for user in data['users']:
        if user['token'] == token:
            return user['u_id']

    return -1


def password_encrypt(password):
    encrypted_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return encrypted_password


def encrypt_token(u_id):
    SECRET = 'IOAE@*#)_IEI@#U()IOJF}_@w30p}"ASDAP9*&@*_!$^_$983y17ae1)(#&@!)wed2891ydhaq;sd'
    encrypted_token = jwt.encode({'token': u_id}, SECRET, "HS256")
    return encrypted_token


def is_empty():
    '''
    Helper function to check that it dict is empty
    '''

    return not (data['users'] and data['channels'] and data['messages'])


def check_if_flockr_owner(u_id):
    '''
    Checks if the given u_id is a global admin
    '''
    for user in data['users']:
        if user['u_id'] == u_id:
            if user['permission_id'] == 1:
                return True

    return False


def valid_user(u_id):
    '''
    Checks if the given u_id is a valid user
    '''
    for user in data['users']:
        if user['u_id'] == u_id:
            return True
    return False


def get_user_handle_strs():
    '''
    Get all handle strs
    '''
    ret = []
    for user in data['users']:
        ret.append(user['handle_str'])
    return ret


def get_user_permission(u_id):
    '''
    Helper function to get user permission
    '''
    perm = 0
    for user in data['users']:
        if user['u_id'] == u_id:
            perm = user['permission_id']

    return perm


def get_first_reset_codes():
    '''
    Blackbox testing other functions
    '''
    return data['reset_codes'][0]['code']


def update_user_reacts(u_id):
    '''
    Helper function to update user reacts
    '''
    for message in data['messages']:
        for react in message['reacts']:
            if u_id in react['u_ids']:
                react['is_this_user_reacted'] = True
            else:
                react['is_this_user_reacted'] = False


def get_messages():
    '''
    Helper function to get all messages
    '''
    messages = []

    for msg in data['messages']:
        messages.append(msg)

    return {
        'messages': messages
    }


def email_send(token, email, message):
    '''
    Send email extra feature
    '''
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError('Invalid email!')

    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": "comp1531dummyemailingbot@gmail.com",
        "MAIL_PASSWORD": "COMP1531Rules"
    }

    APP.config.update(mail_settings)
    mail = Mail(APP)
    for user in data['users']:
        if token_to_uid(token) == user['u_id']:
            name = f"{user['name_first']} {user['name_last']}"
            break

    with APP.app_context():
        msg = Message(
            subject=f"Flockr Message from {name}",
            sender=APP.config.get("MAIL_USERNAME"),
            recipients=[email],
            body=f"On Flockr, {name} sent:\n {message} \n\n Regards, Flockr team \n\n Do not reply to this email."
        )
        mail.send(msg)
    return {}
