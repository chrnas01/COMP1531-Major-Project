'''
tests for auth.py
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
    expected = {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}
    assert test_in == expected
    with pytest.raises(InputError):
        assert auth.auth_login('EMAIL@gmail.com', 'NOTTHEPASSWORD')

def test_auth_login_correct_password():
    '''
    Password is correct
    '''
    other.clear()
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')
    expected = {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}
    assert test_in == expected
    test_in = auth.auth_login('EMAIL@gmail.com', 'PASSWORD')
    expected = {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}
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
    expected = {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}
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
    expected = {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}
    assert test_in == expected

def test_auth_register_firstname_valid2():
    '''
    name_first is exactly the character limit
    '''
    other.clear()
    # name_first is length 50
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'A'*50, 'LASTNAME')
    expected = {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}
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
    expected = {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}
    assert test_in == expected

def test_auth_register_lastname_valid2():
    '''
    name_last is of valid length
    '''
    other.clear()
    # name_last is length 50
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'A'*50)
    expected = {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}
    assert test_in == expected


################################################################################
# Tests on logout
def test_auth_successful_logout():
    '''
    testing successful logouts
    '''
    other.clear()
    test_in = auth.auth_register('EMAIL@gmail.com', 'PASSWORD', 'FIRSTNAME', 'LASTNAME')
    expected = {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}
    assert test_in == expected

    test_in = auth.auth_login('EMAIL@gmail.com', 'PASSWORD')
    expected = {'u_id': 1, 'token': other.encrypt_token(1).decode("utf-8")}
    assert test_in == expected

    assert auth.auth_logout(other.encrypt_token(1).decode("utf-8")) == {'is_success': True}

def test_auth_unsuccessful_logout():
    '''
    logout was unsuccessful
    '''
    other.clear()
    assert auth.auth_logout(other.encrypt_token(1).decode("utf-8")) == {'is_success': False}

################################################################################
# Tests for handle_str
def test_handle_str1():
    '''
    testing that the handle string randomisation is working
    '''
    other.clear()
    auth.auth_register('EMAIL@gmail.com', 'WORDSS', 'FIRSTNAME', 'LASTNAME')
    auth.auth_register('EMAIL2@gmail.com', 'WORDSS', 'FIRSTNAME', 'LASTNAME')
    assert other.get_user_handle_strs() == ['firstnamelastname', 'firstnamelastname2']

def test_handle_str20char():
    '''
    testing that the handle string randomisation is working for names longer
    than 20 characters
    '''
    other.clear()
    auth.auth_register('EMAIL@gmail.com', 'WORDSS', 'twentycharacters', 'isthisname')
    auth.auth_register('EMAIL2@gmail.com', 'WORDSS', 'twentycharacters', 'isthisname')
    assert other.get_user_handle_strs() == ['twentycharactersisth', 'twentycharactersist2']

################################################################################
# Test password reset
def test_auth_password_request():
    '''
    Check if password request works
    '''
    other.clear()
    assert auth.auth_password_request('email@gmail.com') == {}


def test_auth_password_reset_code_invalid():
    '''
    Check if InputError is raised if reset_code is invalid
    '''
    other.clear()
    with pytest.raises(InputError):
        assert auth.auth_password_reset('', 'PASSWORD')

def test_auth_password_reset_password_invalid():
    '''
    Check if InputError is raised if reset_code is invalid
    '''
    other.clear()
    auth.auth_password_request('email@gmail.com')
    with pytest.raises(InputError):
        # Password of length 5 is invalid
        assert auth.auth_password_reset(other.get_first_reset_codes(), 'WORDS')

def test_auth_password_reset_valid():
    '''
    Check if InputError is raised if reset_code is invalid
    '''
    other.clear()
    auth.auth_password_request('email@gmail.com')
    assert auth.auth_password_reset(other.get_first_reset_codes(), 'PASSWORD') == {}

def test_get_first_reset_codes():
    '''
    Check that reset_codes is empty
    '''
    other.clear()
    with pytest.raises(IndexError):
        assert other.get_first_reset_codes()

def test_is_reset_code_false():
    '''
    Test is reset_code identifies false code
    '''
    other.clear()
    assert not auth.is_reset_code_valid('This_code_is_imaginary')

def test_is_reset_code_valid():
    '''
    Test is reset_code identifies correct code
    '''
    other.clear()
    valid_user = {
        'code': 'ABCDEFG',
        'email': 'email@gmail.com'
    }
    other.data['reset_codes'].append(valid_user)
    assert auth.is_reset_code_valid('ABCDEFG')
