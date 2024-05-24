from datetime import datetime, timedelta

import pytest

from src import db
from src.models import Token, User

invalid_credentials = [
    ('test1', 'test2'),
    ('test2', 'test1'),
    ('test2', 'test2'),
    ('test1', ''),
    ('', 'test1'),
    ('', ''),
]


@pytest.mark.parametrize('credentials', invalid_credentials)
def test_new_tokens_invalid_credentials(database_with_data, credentials):
    """
    Given the endpoint /tokens,
    When the method is POST and the user provides invalid credentials,
    Then the user should receive a 401 status code.
    """
    response = database_with_data.post('api/v1/tokens', auth=credentials)
    assert response.status_code == 401


def test_new_tokens(database_with_data):
    """
    Given the endpoint /tokens,
    When the method is POST and the user provides valid credentials,
    Then the user should receive a 200 status code and an access token and a refresh token.
    """
    response = database_with_data.post('api/v1/tokens', auth=('test1', 'test1'))
    assert response.status_code == 200
    assert response.json['access_token'] is not None
    assert response.json['refresh_token'] is not None


def test_access_token(database_with_data, tokens):
    """
    Given a protected endpoint,
    When the user provides a valid access token,
    Then the user should receive a 200 status code and access the endpoint.
    """
    access_token, _ = tokens

    response = database_with_data.put('api/v1/users', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200


def test_access_token_expired(database_with_data, tokens):
    """
    Given a protected endpoint,
    When the user provides an expired access token,
    Then the user should receive a 401 status code.
    """
    access_token, _ = tokens

    token = Token.from_jwt(access_token)
    token.access_expiration = datetime.now() - timedelta(days=10)

    response = database_with_data.put('api/v1/users', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 401


def test_refresh_access_token(database_with_data, tokens):
    """
    Given the endpoint /tokens,
    When the method is PUT and the user provides a valid access token and a valid refresh token,
    Then the user should receive a 200 status code and a new access token and a new refresh token.
    """
    access_token, refresh_token = tokens

    token = Token.from_jwt(access_token)
    token.access_expiration = datetime.now() - timedelta(days=10)

    response = database_with_data.put('api/v1/tokens', json={
        'access_token': access_token, 'refresh_token': refresh_token
    })
    assert response.status_code == 200
    assert response.json['access_token']
    assert response.json['refresh_token']


def test_refresh_token_expired(database_with_data, tokens):
    """
    Given the endpoint /tokens,
    When the method is PUT and the user provides an expired access token and an expired refresh token,
    Then the user should receive a 401 status code.
    """
    access_token, refresh_token = tokens

    token = Token.from_jwt(access_token)
    assert token is not None
    token.expire()

    response = database_with_data.put('api/v1/tokens', json={
        'access_token': access_token, 'refresh_token': refresh_token
    })
    assert response.status_code == 401


def test_revoke_token(database_with_data, tokens):
    """
    Given the endpoint /tokens,
    When the method is DELETE and the user provides a valid access token,
    Then the user should receive a 204 status code.
    """
    access_token, _ = tokens

    response = database_with_data.delete('api/v1/tokens', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 204


def test_revoke_token_invalid_access_token(database_with_data):
    """
    Given the endpoint /tokens,
    When the method is DELETE and the user provides an invalid access token,
    Then the user should receive a 401 status code.
    """
    response = database_with_data.delete('api/v1/tokens', headers={'Authorization': 'Bearer invalid'})
    assert response.status_code == 401


def test_request_reset(database_with_data):
    """
    Given the endpoint /tokens/reset,
    When the method is POST and the user provides a valid email,
    Then the user should receive a 200 status code.
    """
    response = database_with_data.post('api/v1/tokens/reset', json={'email': 'test@test.com'})
    assert response.status_code == 204


def test_request_reset_invalid_email(database_with_data):
    """
    Given the endpoint /tokens/reset,
    When the method is POST and the user provides an invalid email,
    Then the user should receive a 404 status code.
    """
    response = database_with_data.post('api/v1/tokens/reset', json={'email': 'test@abc.com'})
    assert response.status_code == 404


def test_password_reset(database_with_data):
    """
    Given the endpoint /tokens/reset,
    When the method is PUT and the user provides a valid reset token and a valid new password,
    Then the user should receive a 204 status code and the new password should be set.
    """
    user = db.session.get(User, 1)
    reset_token = user.generate_reset_token()
    assert reset_token is not None

    response = database_with_data.put('api/v1/tokens/reset', json={
        'token': reset_token, 'new_password': 'test_password_reset'
    })
    assert response.status_code == 204
    assert user.verify_password('test_password_reset')


def test_password_reset_invalid_reset_token(database_with_data):
    """
    Given the endpoint /tokens/reset,
    When the method is PUT and the user provides an invalid reset token and a valid new password,
    Then the user should receive a 400 status code.
    """
    response = database_with_data.put('api/v1/tokens/reset', json={
        'token': 'invalid', 'new_password': 'test_password_reset'
    })
    assert response.status_code == 400
