import requests
import json
from echo_http_test import url
import other
from PIL import ImageFile

# Borrowed from https://stackoverflow.com/questions/7460218/get-image-size-without-downloading-it-in-python
def getsizes(uri):
    # get file size *and* image size (None if not known)
    file = requests.get(uri, stream=True)
    size = file.headers['content-length']
    if size:
        size = int(size)
    p = ImageFile.Parser()
    while True:
        data = file.raw.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return p.image.size
            break
    file.close()

    return(None)


def test_user_profile_uploadphoto_bad_url(url):
    '''
    Tests a bad url for upload photo
    '''
    requests.delete(url + 'clear')

    # Setup user
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://jdfklajklfjkkjfl.com.au',
        'x_start': '0',
        'y_start': '0',
        'x_end': '20',
        'y_end': '20',
    }
    resp = requests.post(url + '/user/profile/uploadphoto', json=payload)

    assert resp.status_code == 400


def test_user_profile_uploadphoto_invalid_x_start_small(url):
    '''
    Tests a bad url for upload photo
    '''
    requests.delete(url + 'clear')

    # Setup user
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg',
        'x_start': '-1',
        'y_start': '0',
        'x_end': '20',
        'y_end': '20',
    }
    resp = requests.post(url + '/user/profile/uploadphoto', json=payload)

    assert resp.status_code == 400


def test_user_profile_uploadphoto_invalid_x_start_big(url):
    '''
    Tests a bad url for upload photo
    '''
    requests.delete(url + 'clear')

    # Setup user
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg',
        'x_start': '9999999999',
        'y_start': '0',
        'x_end': '20',
        'y_end': '20',
    }
    resp = requests.post(url + '/user/profile/uploadphoto', json=payload)

    assert resp.status_code == 400


def test_user_profile_uploadphoto_invalid_y_start_small(url):
    '''
    Tests a bad url for upload photo
    '''
    requests.delete(url + 'clear')

    # Setup user
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg',
        'x_start': '0',
        'y_start': '-1',
        'x_end': '20',
        'y_end': '20',
    }
    resp = requests.post(url + '/user/profile/uploadphoto', json=payload)

    assert resp.status_code == 400


def test_user_profile_uploadphoto_invalid_y_start_big(url):
    '''
    Tests a bad url for upload photo
    '''
    requests.delete(url + 'clear')

    # Setup user
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg',
        'x_start': '0',
        'y_start': '99999999',
        'x_end': '20',
        'y_end': '20',
    }
    resp = requests.post(url + '/user/profile/uploadphoto', json=payload)

    assert resp.status_code == 400


def test_user_profile_uploadphoto_invalid_x_end_small(url):
    '''
    Tests a bad url for upload photo
    '''
    requests.delete(url + 'clear')

    # Setup user
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg',
        'x_start': '0',
        'y_start': '0',
        'x_end': '-1',
        'y_end': '20',
    }
    resp = requests.post(url + '/user/profile/uploadphoto', json=payload)

    assert resp.status_code == 400


def test_user_profile_uploadphoto_invalid_x_end_big(url):
    '''
    Tests a bad url for upload photo
    '''
    requests.delete(url + 'clear')

    # Setup user
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg',
        'x_start': '0',
        'y_start': '0',
        'x_end': '999999',
        'y_end': '20',
    }
    resp = requests.post(url + '/user/profile/uploadphoto', json=payload)

    assert resp.status_code == 400


def test_user_profile_uploadphoto_invalid_y_start_small(url):
    '''
    Tests a bad url for upload photo
    '''
    requests.delete(url + 'clear')

    # Setup user
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg',
        'x_start': '0',
        'y_start': '0',
        'x_end': '20',
        'y_end': '-1',
    }
    resp = requests.post(url + '/user/profile/uploadphoto', json=payload)

    assert resp.status_code == 400


def test_user_profile_uploadphoto_not_JPG(url):
    '''
    Tests a bad url for upload photo
    '''
    requests.delete(url + 'clear')

    # Setup user
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://png.pngitem.com/pimgs/s/484-4849159_shrek-head-png-image-shrek-png-transparent-png.png',
        'x_start': '0',
        'y_start': '0',
        'x_end': '20',
        'y_end': '20',
    }
    resp = requests.post(url + '/user/profile/uploadphoto', json=payload)

    assert resp.status_code == 400


def test_user_profile_uploadphoto_success(url):
    '''
    Tests a bad url for upload photo
    '''
    requests.delete(url + 'clear')

    # Setup user
    payload = {
        'email': 'jayden@gmail.com',
        'password': 'password',
        'name_first': 'Jayden',
        'name_last': 'Leung'
    }
    user_1 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg',
        'x_start': '0',
        'y_start': '0',
        'x_end': '38',
        'y_end': '11',
    }
    requests.post(url + '/user/profile/uploadphoto', json=payload)

    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    profile_img_url = str(resp['user']['profile_img_url'])
    # print(profile_img_url)

    assert getsizes(profile_img_url) == (38, 11)
