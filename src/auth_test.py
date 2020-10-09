import pytest
import auth
import other
from error import InputError

################################################################################
# Tests on login
# Email entered is not valid
def test_auth_login_invalid_email():
    other.clear() # Blackbox testing, clear users
    with pytest.raises(InputError) as e:
        assert auth.auth_login('EMAIL', 'PASSWORD')
    
# Email entered does not belong to a user
def test_auth_login_not_registered():
    other.clear()
    with pytest.raises(InputError) as e:
        assert auth.auth_login('NOTANEMAIL@gmail.com', 'PASSWORD')
    

# Password is not correct
def test_auth_login_incorrect_password():
    other.clear()
    assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME') == {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    with pytest.raises(InputError) as e:
        assert auth.auth_login('EMAIL@gmail.com', 'NOTTHEPASSWORD')
    
# Password is correct
def test_auth_login_correct_password():
    other.clear()
    assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME') == {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert auth.auth_login('EMAIL@gmail.com', 'PASSWORD') == {'u_id': 1, 'token': 'EMAIL@gmail.com',}


################################################################################
# Tests on email
# Email entered is not valid
def test_auth_register_invalid_email():
    other.clear()
    with pytest.raises(InputError) as e:
        assert auth.auth_register('EMAIL', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')
    
# Email address is already being used
def test_auth_register_used_email():
    other.clear()
    auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')
    with pytest.raises(InputError) as e:
        assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')
    

################################################################################
# Tests on password
# Password length is of sufficient length
# Test edge cases
def test_auth_register_password_short():
    other.clear()
    with pytest.raises(InputError) as e:
        assert auth.auth_register('EMAIL@gmail.com', 'WORDS', 'FIRSTNAME', 'LASTNAME') # Password is length 5
    
def test_auth_register_password_correct():
    other.clear()
    assert auth.auth_register('EMAIL@gmail.com', 'WORDSS', 'FIRSTNAME', 'LASTNAME') == {'u_id': 1, 'token': 'EMAIL@gmail.com',} # Password is length 6
    

################################################################################
# Tests on name_first
# name_first is of valid length
def test_auth_register_firstname_short():
    other.clear()
    with pytest.raises(InputError) as e:
        assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', '', 'LASTNAME') # name_first is length 0
    
def test_auth_register_firstname_long():
    other.clear()
    with pytest.raises(InputError) as e:
        assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'A'*51, 'LASTNAME') # name_first is length 51
    
def test_auth_register_firstname_valid1():
    other.clear()
    assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'A', 'LASTNAME') == {'u_id': 1, 'token': 'EMAIL@gmail.com',} # name_first is length 1
    
def test_auth_register_firstname_valid2():
    other.clear()
    assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'A'*50, 'LASTNAME') == {'u_id': 1, 'token': 'EMAIL@gmail.com',} # name_first is length 50
    

################################################################################
# Tests on name_last
# name_last is of valid length
def test_auth_register_lastname_short():
    other.clear()
    with pytest.raises(InputError) as e:
        assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', '') # name_last is length 0
    
def test_auth_register_lastname_long():
    other.clear()
    with pytest.raises(InputError) as e:
        assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'A'*51) # name_last is length 51
    
def test_auth_register_lastname_valid1():
    other.clear()
    assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'A') == {'u_id': 1, 'token': 'EMAIL@gmail.com',} # name_last is length 1
    
def test_auth_register_lastname_valid2():
    other.clear()
    assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'A'*50) == {'u_id': 1, 'token': 'EMAIL@gmail.com',} # name_last is length 50
    

################################################################################
# Tests on logout
def test_auth_successful_logout():
    other.clear()
    assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME') == {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert auth.auth_login('EMAIL@gmail.com', 'PASSWORD') == {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert auth.auth_logout('EMAIL@gmail.com') == {'is_success ': True}
    
def test_auth_unsuccessful_logout():
    other.clear()
    assert auth.auth_logout('EMAIL@gmail.com') == {'is_success ': False}

################################################################################
# Tests for handle_str

def test_handle_str1():
    other.clear()
    auth.auth_register('EMAIL@gmail.com', 'WORDSS', 'FIRSTNAME', 'LASTNAME')
    auth.auth_register('EMAIL2@gmail.com', 'WORDSS', 'FIRSTNAME', 'LASTNAME')
    assert other.data['users'][1]['handle_str'] == 'firstnamelastname2'

def test_handle_str20char():
    other.clear()
    auth.auth_register('EMAIL@gmail.com', 'WORDSS', 'twentycharacters', 'isthisname')
    auth.auth_register('EMAIL2@gmail.com', 'WORDSS', 'twentycharacters', 'isthisname')
    assert other.data['users'][0]['handle_str'] == 'twentycharactersisth'
    assert other.data['users'][1]['handle_str'] == 'twentycharactersisth2'