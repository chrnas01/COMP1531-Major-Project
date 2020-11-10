import requests
import json
from echo_http_test import url
import other
from PIL import ImageFile, Image
import os


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

    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] == ''


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

    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] == ''


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
    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] == ''


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
    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] == ''


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
    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] == ''


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
    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] == ''


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
    
    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] == ''


def test_user_profile_uploadphoto_invalid_y_end_small(url):
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
    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] == ''


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
    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] == ''


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
        'x_end': '40',
        'y_end': '40',
    }
    requests.post(url + '/user/profile/uploadphoto', json=payload)

    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    profile_img_url = str(resp['user']['profile_img_url'])

    assert profile_img_url != ''
    image_object = Image.open(os.path.join(
        os.path.dirname(__file__) + '/imgurl/', 'pp_1.jpg'))
    assert image_object.size == (40, 40)


def test_user_profile_uploadphoto_success_two_users(url):
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
        'email': 'steven@gmail.com',
        'password': 'password',
        'name_first': 'Steven',
        'name_last': 'Luong'
    }
    user_2 = requests.post(url + 'auth/register', json=payload).json()

    payload = {
        'token': user_1['token'],
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg',
        'x_start': '0',
        'y_start': '0',
        'x_end': '40',
        'y_end': '40',
    }
    requests.post(url + '/user/profile/uploadphoto', json=payload)

    payload = {
        'token': user_2['token'],
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg',
        'x_start': '0',
        'y_start': '0',
        'x_end': '20',
        'y_end': '20',
    }
    requests.post(url + '/user/profile/uploadphoto', json=payload)

    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] != ''

    payload = {
        'token': user_2['token'],
        'u_id': user_2['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    assert resp['user']['profile_img_url'] != ''

    image_object = Image.open(os.path.join(
        os.path.dirname(__file__) + '/imgurl/', 'pp_1.jpg'))
    assert image_object.size == (40, 40)

    image_object = Image.open(os.path.join(
        os.path.dirname(__file__) + '/imgurl/', 'pp_2.jpg'))
    assert image_object.size == (20, 20)


def test_user_profile_uploadphoto_success_jpeg(url):
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
        'img_url': 'https://cdn.hipwallpaper.com/i/93/59/VqSvui.jpg',
        'x_start': '0',
        'y_start': '0',
        'x_end': '40',
        'y_end': '40',
    }
    requests.post(url + '/user/profile/uploadphoto', json=payload)

    payload = {
        'token': user_1['token'],
        'u_id': user_1['u_id'],
    }
    resp = requests.get(url + 'user/profile', params=payload).json()
    profile_img_url = str(resp['user']['profile_img_url'])

    assert profile_img_url != ''
    image_object = Image.open(os.path.join(
        os.path.dirname(__file__) + '/imgurl/', 'pp_1.jpg'))
    assert image_object.size == (40, 40)
