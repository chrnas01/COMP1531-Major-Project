import auth
import channels

def clear():
    auth.delete_users()
    channels.delete_data()

def users_all(token):
    return auth.all_users

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