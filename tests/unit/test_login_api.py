import pytest
from app import create_app
import os

def valid_api_response(res):
    if not res.status_code in range(200, 300):
        print(res.status, res.status_code)
        valid_code = False
    else:
        valid_code = True

    if res.status_code != 204:
        if not res.is_json:
            print('Data', res.data)
            return False

        if not res.json.get('success', True):
            if 'reason' in res.json:
                print('Failure reason:', res.json['reason'])
            print(res.json)
            return False

    return valid_code

@pytest.fixture
def logged_client(app):
    with app.test_client() as test_client:
        res = test_client.get('/api/session/get_login_token')
        assert valid_api_response(res)
        assert 'token' in res.json
        assert isinstance(res.json['token'], str)
        print('Got token:', res.json['token'])
        
        res = test_client.post('/api/session/create', json={
            'user': 'victor@torres.com',
            'passwd': 'holavictor',
            'token': res.json['token'],
        })
        assert valid_api_response(res)
        assert res.json['identifier'] == 'cookies'
        assert test_client.get_cookie('sid') is not None

        yield test_client

def test_logout(logged_client):
    res = logged_client.delete('/api/session/close')
    assert valid_api_response(res)



