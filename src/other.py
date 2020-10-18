import auth
import channels
import jwt
import hashlib


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

def password_encrypt(password):
    encrypted_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return encrypted_password

def encrypt_token(u_id):
    SECRET = 'IOAE@*#)_IEI@#U()IOJF}_@w30p}"ASDAP9*&@*_!$^_$983y17ae1)(#&@!)wed2891ydhaq;sd'
    encrypted_token = jwt.encode({'token': u_id}, SECRET, "HS256")
    return encrypted_token

def decrypt_token(encrypted_token):
    SECRET = 'IOAE@*#)_IEI@#U()IOJF}_@w30p}"ASDAP9*&@*_!$^_$983y17ae1)(#&@!)wed2891ydhaq;sd'
    decrypted_token = jwt.decode(encrypted_token, SECRET, "HS256")
    return decrypted_token
