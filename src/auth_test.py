import pytest
import auth
from error import InputError

def test_successful_register():
    # Assumptions: token will temporarily be u_id, we also give the first person registered u_id: 1
    # [Reserving u_id: 0 for admin if required]
    assert(auth.auth_register("EMAIL@gmail.com", "PASSWORD", "NAME", "LASTNAME") == {'u_id': 1, 'token': 1,})
    assert(auth.auth_login("EMAIL@gmail.com", "PASSWORD") == {'u_id': 1, 'token': 1,})
    assert(auth.auth_logout(1) == {'is_success': True,})

# Check correct error was raised
# Checks email is not of a valid format
def test_invaid_email():
    with pytest.raises(InputError) as e:
        assert(auth.auth_register("EMAIL", "PASSWORD", "NAME", "LASTNAME"))

# Checks email that has not been registered
def test_input_incorrect_email():
    with pytest.raises(InputError) as e:
        assert(auth.auth_login("NOTANEMAIL@gmail.com", "PASSWORD"))

# Checks password is incorrect
def test_input_incorrect_password():
    assert(auth.auth_register("EMAIL@gmail.com", "PASSWORD", "NAME", "LASTNAME") == {'u_id': 1, 'token': 1,})
    with pytest.raises(InputError) as e:
        assert(auth.auth_login("EMAIL@gmail.com", "NOTTHEPASSWORD"))
