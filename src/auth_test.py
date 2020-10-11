'''
Tests for auth.py
'''
import pytest
import auth
import other
from error import InputError

################################################################################
# Tests on login
def test_auth_login_invalid_email():
    '''
    Email entered is not valid
    '''
    other.clear() # Blackbox testing, clear users
    with pytest.raises(InputError):
        assert auth.auth_login('EMAIL', 'PASSWORD')

def test_auth_login_not_registered():
    '''
    Email entered does not belong to a user
    '''
    other.clear()
    with pytest.raises(InputError):
        assert auth.auth_login('NOTANEMAIL@gmail.com', 'PASSWORD')

def test_auth_login_incorrect_password():
    '''
    Password is not correct
    '''
    other.clear()
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')
    expected = {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert test_in == expected
    with pytest.raises(InputError):
        assert auth.auth_login('EMAIL@gmail.com', 'NOTTHEPASSWORD')

def test_auth_login_correct_password():
    '''
    Password is correct
    '''
    other.clear()
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')
    expected = {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert test_in == expected
    test_in = auth.auth_login('EMAIL@gmail.com', 'PASSWORD')
    expected = {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert test_in == expected


################################################################################
# Tests on email
def test_auth_register_invalid_email():
    '''
    Email entered is not valid
    '''
    other.clear()
    with pytest.raises(InputError):
        assert auth.auth_register('EMAIL', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')

def test_auth_register_used_email():
    '''
    Email address is already being used
    '''
    other.clear()
    auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')
    with pytest.raises(InputError):
        assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')


################################################################################
# Tests on password
# Test edge cases
def test_auth_register_password_short():
    '''
    Password length is of insufficient length
    '''
    other.clear()
    with pytest.raises(InputError):
        # Password is length 5
        assert auth.auth_register('EMAIL@gmail.com', 'WORDS', 'FIRSTNAME', 'LASTNAME')

def test_auth_register_password_correct():
    '''
    Password length is of sufficient length
    '''
    other.clear()
    # Password is length 6
    test_in = auth.auth_register('EMAIL@gmail.com', 'WORDSS', 'FIRSTNAME', 'LASTNAME')
    expected = {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert test_in == expected


################################################################################
# Tests on name_first
def test_auth_register_firstname_short():
    '''
    name_first is too short
    '''
    other.clear()
    with pytest.raises(InputError):
        # name_first is length 0
        assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', '', 'LASTNAME')

def test_auth_register_firstname_long():
    '''
    name_first is too long
    '''
    other.clear()
    with pytest.raises(InputError):
        # name_first is length 51
        assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'A'*51, 'LASTNAME')

def test_auth_register_firstname_valid1():
    '''
    name_first is of valid length
    '''
    other.clear()
    # name_first is length 1
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'A', 'LASTNAME')
    expected = {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert test_in == expected

def test_auth_register_firstname_valid2():
    '''
    name_first is exactly the character limit
    '''
    other.clear()
    # name_first is length 50
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'A'*50, 'LASTNAME')
    expected = {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert test_in == expected


################################################################################
# Tests on name_last
def test_auth_register_lastname_short():
    '''
    name_last is too short
    '''
    other.clear()
    with pytest.raises(InputError):
        # name_last is length 0
        assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', '')

def test_auth_register_lastname_long():
    '''
    name_last is too long
    '''
    other.clear()
    with pytest.raises(InputError):
        # name_last is length 51
        assert auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'A'*51)

def test_auth_register_lastname_valid1():
    '''
    name_last is of valid length
    '''
    other.clear()
    # name_last is length 1
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'A')
    expected = {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert test_in == expected

def test_auth_register_lastname_valid2():
    '''
    name_last is of valid length
    '''
    other.clear()
    # name_last is length 50
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'A'*50)
    expected = {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert test_in == expected


################################################################################
# Tests on logout
def test_auth_successful_logout():
    '''
    testing successful logouts
    '''
    other.clear()
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')
    expected = {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert test_in == expected

    test_in = auth.auth_login('EMAIL@gmail.com', 'PASSWORD')
    expected = {'u_id': 1, 'token': 'EMAIL@gmail.com',}
    assert test_in == expected

    assert auth.auth_logout('EMAIL@gmail.com') == {'is_success ': True}

def test_auth_unsuccessful_logout():
    '''
    logout was unsuccessful
    '''
    other.clear()
    assert auth.auth_logout('EMAIL@gmail.com') == {'is_success ': False}

################################################################################
# Tests for handle_str

def test_handle_str1():
    '''
    testing that the handle string randomisation is working
    '''
    other.clear()
    auth.auth_register('EMAIL@gmail.com', 'WORDSS', 'FIRSTNAME', 'LASTNAME')
    auth.auth_register('EMAIL2@gmail.com', 'WORDSS', 'FIRSTNAME', 'LASTNAME')
    assert other.data['users'][1]['handle_str'] == 'firstnamelastname2'

def test_handle_str20char():
    '''
    testing that the handle string randomisation is working for names longer
    than 20 characters
    '''
    other.clear()
    auth.auth_register('EMAIL@gmail.com', 'WORDSS', 'twentycharacters', 'isthisname')
    auth.auth_register('EMAIL2@gmail.com', 'WORDSS', 'twentycharacters', 'isthisname')
    assert other.data['users'][0]['handle_str'] == 'twentycharactersisth'
    assert other.data['users'][1]['handle_str'] == 'twentycharactersisth2'
