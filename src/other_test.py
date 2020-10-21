'''
Tests functions in other.py
'''
import pytest
import other
import auth
from error import InputError, AccessError


@pytest.fixture
def setup():
    '''
    Resets user data for each test
    '''
    # Clear database
    other.clear()

    # Setup users
    user_1 = auth.auth_register(
        'jayden@gmail.com', 'password', 'Jayden', 'Leung')  # Flockr Owner
    user_2 = auth.auth_register(
        'Steven@gmail.com', 'password', 'Steven', 'Luong')
    user_3 = auth.auth_register('sam@gmail.com', 'password', 'Sam', 'He')

    return (user_1, user_2, user_3)

################################################################################


def test_admin_userpermission_change_invalid_uid(setup):
    '''
    Changing user permission of u_id that does not exist
    '''
    # Setup pytest
    user_1, _, _ = setup

    with pytest.raises(InputError):
        assert other.admin_userpermission_change(user_1['token'], 99, 1)


def test_admin_userpermission_change_invalid_permission_id(setup):
    '''
    Changing user permission with wrong permission_id
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    with pytest.raises(InputError):
        assert other.admin_userpermission_change(user_1['token'], user_2['u_id'], 2)


def test_admin_userpermission_change_unauthorised_user(setup):
    '''
    Changing user permission with wrong unauthorised user
    '''
    # Setup pytest
    _, user_2, user_3 = setup

    with pytest.raises(AccessError):
        assert other.admin_userpermission_change(user_2['token'], user_3['u_id'], 1)


def test_admin_userpermission_change_success(setup):
    '''
    Successful admin user permission change
    '''
    # Setup pytest
    user_1, user_2, _ = setup

    other.admin_userpermission_change(user_1['token'], user_2['u_id'], 1)

    successful = False

    for user in other.users_all(user_1['token'])['users']:
        if user['u_id'] == user_2['u_id']:
            if user['permission_id'] == 1:
                successful = True

    assert successful

################################################################################
