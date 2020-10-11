'''
    Tests functions in user.py
'''
import pytest
import auth
import user
from error import InputError
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
    user.user_profile_sethandle(user_1['token'], 'newhandle')

    assert user.user_profile(user_1['token'], user_1['u_id']) == {
        'user': {
            'email': 'jayden@gmail.com',
            'u_id': 1,
            'name_first': 'Jayden',
            'name_last': 'Leung',
            'handle_str': 'newhandle',
            }
        }

def test_user_profile_sethandle_already_exists():
    '''
    Tests that user_profile_sethandle sets the correct handle_str when there are duplicates
    '''
    other.clear()
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
    auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong') # Flockr Owner

    user.user_profile_sethandle(user_1['token'], 'stevenluong')

    assert user.user_profile(user_1['token'], user_1['u_id']) == {
        'user': {
            'email': 'jayden@gmail.com',
            'u_id': 1,
            'name_first': 'Jayden',
            'name_last': 'Leung',
            'handle_str': 'stevenluong1',
            }
        }

########################################################