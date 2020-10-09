import auth
import channels

data = {
    'users': [],
    'channels': [],
    'messages': [],
}

def clear():
    data['users'].clear()
    data['channels'].clear()
    data['messages'].clear()

def users_all(token):
    return data['users']

def admin_userpermission_change(token, u_id, permission_id):
    pass

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

# Coverts the users token to a valid user_id 
def token_to_uid(token):
    for user in data['users']:
        if user['token'] == token:
            return user['u_id']
    else:
        return -1 