import pytest
import auth
import channel
import channels
import user
from error import InputError, AccessError
import other

########################################################

def test_user_profile_success():
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
    other.clear()
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner

    with pytest.raises(InputError):
        user.user_profile(user_1['token'], 99)

########################################################

def test_user_profile_setname_success():
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
    other.clear()
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner

    with pytest.raises(InputError):
        assert user.user_profile_setname(user_1['token'], '', 'LASTNAME') # name_first is length 0
    
def test_user_profile_firstname_long():
    other.clear()
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner

    with pytest.raises(InputError):
        assert user.user_profile_setname(user_1['token'], 'A'*51, 'LASTNAME') # name_first is length 51

def test_user_profile_lastname_short():
    other.clear()
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner

    with pytest.raises(InputError):
        assert user.user_profile_setname(user_1['token'], 'FIRSTNAME', '') # name_last is length 0
    
def test_user_profile_lastname_long():
    other.clear()
    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner

    with pytest.raises(InputError):
        assert user.user_profile_setname(user_1['token'], 'FIRSTNAME', 'A'*51) # name_last is length 51
  

########################################################

def test_user_profile_setemail_success():
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
    other.clear()

    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner

    with pytest.raises(InputError):
        assert user.user_profile_setemail(user_1['token'], 'EMAIL')
    
def test_user_profile_setemail_used_email():
    other.clear()

    # Setup users
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
    user_2 = auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong')

    with pytest.raises(InputError):
        assert user.user_profile_setemail(user_1['token'], 'Steven@gmail.com')

########################################################

def test_user_profile_sethandle_success():
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
    other.clear()
    user_1 = auth.auth_register('jayden@gmail.com', 'password', 'Jayden', 'Leung') # Flockr Owner
    user_2 = auth.auth_register('Steven@gmail.com', 'password', 'Steven', 'Luong')
    
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