import pytest
import auth
from error import InputError

################################################################################

# Email entered is not valid
def test_auth_login_invalid_email():
    with pytest.raises(InputError) as e:
        assert auth.auth_login("EMAIL", "PASSWORD")
    auth.delete_users() # Blackbox testing, clear users

# Email entered does not belong to a user
def test_auth_login_invalid_email():
    with pytest.raises(InputError) as e:
        assert auth.auth_login("NOTANEMAIL@gmail.com", "PASSWORD")
    auth.delete_users()

# Password is not correct
def test_auth_login_incorrect_password():
    assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "FIRSTNAME", "LASTNAME") == {'u_id': 1, 'token': 1,}
    with pytest.raises(InputError) as e:
        assert auth.auth_login("EMAIL@gmail.com", "NOTTHEPASSWORD")
    auth.delete_users()

################################################################################

# Email entered is not valid
def test_auth_register_invalid_email():
    with pytest.raises(InputError) as e:
        assert auth.auth_register("EMAIL", "PASSWORD", "FIRSTNAME", "LASTNAME")
    auth.delete_users()

# Email address is already being used
def test_auth_register_invalid_email():
    auth.auth_register("EMAIL@gmail.com", "PASSWORD", "FIRSTNAME", "LASTNAME")
    with pytest.raises(InputError) as e:
        assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "FIRSTNAME", "LASTNAME")
    auth.delete_users()

################################################################################

# Password length is of sufficient length
# Test edge cases
def test_auth_register_password_short():
    with pytest.raises(InputError) as e:
        assert auth.auth_register("EMAIL@gmail.com", "WORDS", "FIRSTNAME", "LASTNAME") # Password is length 5
    auth.delete_users()

def test_auth_register_password_correct():
    assert auth.auth_register("EMAIL@gmail.com", "WORDSS", "FIRSTNAME", "LASTNAME") == {'u_id': 1, 'token': 1,} # Password is length 6
    auth.delete_users()

################################################################################

# name_first is of valid length
def test_auth_register_firstname_short():
    with pytest.raises(InputError) as e:
        assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "", "LASTNAME") # name_first is length 0
    auth.delete_users()

def test_auth_register_firstname_long():
    with pytest.raises(InputError) as e:
        assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "A"*51, "LASTNAME") # name_first is length 51
    auth.delete_users()

def test_auth_register_firstname_valid1():
    assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "A", "LASTNAME") == {'u_id': 1, 'token': 1,} # name_first is length 1
    auth.delete_users()

def test_auth_register_firstname_valid2():
    assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "A"*50, "LASTNAME") == {'u_id': 1, 'token': 1,} # name_first is length 50
    auth.delete_users()

################################################################################

# name_last is of valid length
def test_auth_register_lastname_short():
    with pytest.raises(InputError) as e:
        assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "FIRSTNAME", "") # name_last is length 0
    auth.delete_users()

def test_auth_register_lastname_long():
    with pytest.raises(InputError) as e:
        assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "FIRSTNAME", "A"*51) # name_last is length 51
    auth.delete_users()

def test_auth_register_lastname_valid1():
    assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "FIRSTNAME", "A") == {'u_id': 1, 'token': 1,} # name_last is length 1
    auth.delete_users()

def test_auth_register_lastname_valid2():
    assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "FIRSTNAME", "A"*50) == {'u_id': 1, 'token': 1,} # name_last is length 50
    auth.delete_users()

################################################################################

def test_auth_successful_logout():
    assert auth.auth_register("EMAIL@gmail.com", "PASSWORD", "FIRSTNAME", "LASTNAME") == {'u_id': 1, 'token': 1,}
    assert auth.auth_login("EMAIL@gmail.com", "PASSWORD") == {'u_id': 1, 'token': 1,}
    assert auth.auth_logout(1) == {'is_success': True,}
    auth.delete_users()

def test_auth_unsuccessful_logout():
    assert auth.auth_logout(1) == {'is_success': False,}
    auth.delete_users()
