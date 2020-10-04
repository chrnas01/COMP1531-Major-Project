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