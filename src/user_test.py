'''
    Tests functions in user.py
'''
import pytest
import auth
import user
from error import InputError, AccessError
import other
 
########################################################
 
def test_user_profile_success():
    '''
    Tests that user_profile returns the correct data
    '''
    other.clear()
 
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
 
    assert user.user_profile(user_1['token'], user_1['u_id']) == {
        'user': {
            'email': 'jayden@gmail.com',
            'u_id': 1,
            'name_first': 'Jayden',
            'name_last': 'Leung',
            'handle_str': 'jaydenleung',
            'profile_img_url': '',
            }
        }
 
def test_user_profile_invalid_uid():
    '''
    Tests that user_profile throws an InputError with invalid uid
    '''
 
    other.clear()
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
 
    with pytest.raises(InputError):
        user.user_profile(user_1['token'], 99)
 
########################################################
 
def test_user_profile_setname_success():
    '''
    Tests that user_profile_setname sets the correct first and last name
    '''
 
    other.clear()
 
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
 
    user.user_profile_setname(user_1['token'], 'changed_first', 'changed_last')
 
    assert user.user_profile(user_1['token'], user_1['u_id']) == {
        'user': {
            'email': 'jayden@gmail.com',
            'u_id': 1,
            'name_first': 'changed_first',
            'name_last': 'changed_last',
            'handle_str': 'jaydenleung',
            'profile_img_url': '',
            }
        }
 
def test_user_profile_firstname_short():
    '''
    Tests that user_profile_setname throws InputError when first name is too short
    '''
    other.clear()
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
 
    with pytest.raises(InputError):
        assert user.user_profile_setname(user_1['token'], '', 'LASTNAME') # name_first is length 0
 
def test_user_profile_firstname_long():
    '''
    Tests that user_profile_setname throws InputError when first name is too long
    '''
    other.clear()
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
 
    with pytest.raises(InputError):
        assert user.user_profile_setname(user_1['token'], 'A'*51, 'LASTNAME')
 
def test_user_profile_lastname_short():
    '''
    Tests that user_profile_setname throws InputError when last name is too short
    '''
    other.clear()
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
 
    with pytest.raises(InputError):
        assert user.user_profile_setname(user_1['token'], 'FIRSTNAME', '') # name_last is length 0
 
def test_user_profile_lastname_long():
    '''
    Tests that user_profile_setname throws InputError when last name is too long
    '''
    other.clear()
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
 
    with pytest.raises(InputError):
        assert user.user_profile_setname(user_1['token'], 'FIRSTNAME', 'A'*51)
 
 
########################################################
 
def test_user_profile_setemail_success():
    '''
    Tests that user_profile_setemail sets the correct email
    '''
 
    other.clear()
 
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
    user.user_profile_setemail(user_1['token'], 'test@gmail.com')
 
    assert user.user_profile(user_1['token'], user_1['u_id']) == {
        'user': {
            'email': 'test@gmail.com',
            'u_id': 1,
            'name_first': 'Jayden',
            'name_last': 'Leung',
            'handle_str': 'jaydenleung',
            'profile_img_url': '',
            }
        }
 
def test_user_profile_setemail_invalid_email():
    '''
    Tests that user_profile_setemail throws InputError when email is invalid
    '''
    other.clear()
 
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
 
    with pytest.raises(InputError):
        assert user.user_profile_setemail(user_1['token'], 'EMAIL')
 
def test_user_profile_setemail_used_email():
    '''
    Tests that user_profile_setemail throws InputError when email is already used
    '''
    other.clear()
 
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
    auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong') # Flockr Owner
 
    with pytest.raises(InputError):
        assert user.user_profile_setemail(user_1['token'], 'Steven@gmail.com')
 
########################################################
 
def test_user_profile_sethandle_success():
    '''
    Tests that user_profile_sethandle sets the correct handle_str
    '''
    other.clear()

    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
    user.user_profile_sethandle(user_1['token'], 'jaydenleung')

    assert user.user_profile(user_1['token'], user_1['u_id']) == {
        'user': {
            'email': 'jayden@gmail.com',
            'u_id': 1,
            'name_first': 'Jayden',
            'name_last': 'Leung',
            'handle_str': 'jaydenleung',
            'profile_img_url': '',
            }
        }
 
def test_user_profile_sethandle_already_exists():
    '''
    Tests that user_profile_sethandle sets the correct handle_str when there are duplicates
    '''
    other.clear()
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
    auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong') # Flockr Owner
 
    with pytest.raises(InputError):
        user.user_profile_sethandle(user_1['token'], 'stevenluong')
 
def test_user_profile_sethandle_short():
    '''
    Tests that user_profile_sethandle throws InputError when handle is too short
    '''
    other.clear()
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
    auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong') # Flockr Owner
 
    with pytest.raises(InputError):
        user.user_profile_sethandle(user_1['token'], '')
 
def test_user_profile_sethandle_long():
    '''
    Tests that user_profile_sethandle throws InputError when handele is too long
    '''
    other.clear()
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
    auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong') # Flockr Owner
 
    with pytest.raises(InputError):
        user.user_profile_sethandle(user_1['token'], 'A'*20)
########################################################
 
def test_all_users():
    '''
    Test to show all users
    '''
    other.clear()
 
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
 
    assert other.users_all(user_1['token']) == {'users': [
        {
            'u_id': 1,
            'email': 'jayden@gmail.com',
            'name_first': 'Jayden',
            'name_last': 'Leung',
            'handle_str': 'jaydenleung',
            'profile_img_url': '',
        },
    ]}

########################################################

def test_user_delete_invalid_token():
    '''
    Deleting a user that doesn't exist
    '''
    other.clear()

    with pytest.raises(AccessError):
        user.user_delete('not a token', 1)

def test_user_delete_invalid_user():
    '''
    Deleting a user that doesn't exist
    '''
    other.clear()
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung')

    with pytest.raises(InputError):
        user.user_delete(user_1['token'], 99)

def test_user_delete_invalid_perms():
    '''
    Deleting a user when you are not the flockr owner
    '''
    other.clear()
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung')
    user_2 = auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong')

    with pytest.raises(AccessError):
        user.user_delete(user_2['token'], user_1['u_id'])

def test_user_delete_success():
    '''
    Deleting a user
    '''
    other.clear()
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung')
    user_2 = auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong')

    user.user_delete(user_1['token'], user_2['u_id'])

    assert other.users_all(user_1['token']) == {'users': [
        {
            'u_id': 1,
            'email': 'jayden@gmail.com',
            'name_first': 'Jayden',
            'name_last': 'Leung',
            'handle_str': 'jaydenleung',
            'profile_img_url': '',
        },
    ]}

########################################################

def test_invalid_token():
    '''
    Checking that the invalid token checks are working
    '''
    other.clear()
    auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung')

    with pytest.raises(AccessError):
        assert user.user_profile_setname('invalid-token', 'sam', 'he')
    
    with pytest.raises(AccessError):
        assert user.user_profile_setemail('invalid-token', 'Steven@gmail.com')
    
    with pytest.raises(AccessError):
        assert user.user_profile_sethandle('invalid-token', 'Steven123')
