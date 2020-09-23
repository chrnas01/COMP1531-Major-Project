import pytest
import channel
from error import InputError

def test_channel_invite():
    pass

def test_channel_details():
    assert channel.channel_details(1,1) == {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def test_channel_messages():
    pass

def test_channel_leave():
    pass

def test_channel_join():
    pass    

def test_channel_addowner():
    pass

def test_channel_removeowner():
    pass