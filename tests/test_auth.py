from datetime import datetime

import pytest

from src import db
from src.models import Token


def test_create_tokens(database_with_data):
    """
    Given a user with valid credentials,
    When the user authenticates,
    Then the user should receive an access token and a refresh token.
    """
    response = database_with_data.post('api/v1/tokens', auth=('test1', 'test1'))
    assert response.status_code == 200
    assert response.json['access_token'] is not None
    assert response.json['refresh_token'] is not None


invalid_credentials = [
    ('test1', 'test2'),
    ('test2', 'test1'),
    ('test2', 'test2'),
    ('test1', ''),
    ('', 'test1'),
    ('', ''),
]


@pytest.mark.parametrize('credentials', invalid_credentials)
def test_invalid_credentials(database_with_data, credentials):
    """
    Given invalid credentials,
    When the user authenticates,
    Then the user should not receive an access token and a refresh token.
    """
    response = database_with_data.post('api/v1/tokens', auth=credentials)
    assert response.status_code == 401


def test_access_token(database_with_data, tokens):
    """
    Given an access token,
    When a protected route is requested with a valid acess token,
    Then the user should be able to access the route.
    """
    access_token, _ = tokens

    response = database_with_data.get('api/v1/users', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200


def test_access_token_expired(database_with_data, tokens):
    """
    Given an access token,
    When the access token is expired,
    Then the access token should be invalid.
    """
    access_token, _ = tokens
    token = Token.from_jwt(access_token)
    token.expire()
    db.session.add(token)
    db.session.commit()

    response = database_with_data.put('api/v1/users', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 401


def test_refresh_token(database_with_data, tokens):
    """
    Given an expired access token,
    When the user refreshes the tokens,
    Then the user should receive new tokens.
    """
    access_token, refresh_token = tokens
    token = Token.from_jwt(access_token)
    token.access_expiration = datetime(1000, 12, 30)

    response = database_with_data.put('api/v1/tokens', json={
        'access_token': access_token, 'refresh_token': refresh_token
    })
    assert response.status_code == 200
    assert response.json['access_token']
    assert response.json['refresh_token']


def test_refresh_token_invalid(database_with_data, tokens):
    """
    Given an expired access token and an expired refresh token,
    When the user refreshes the tokens,
    Then the user should not receive new tokens.
    """
    access_token, refresh_token = tokens
    token = Token.from_jwt(access_token)
    token.access_expiration = datetime(1000, 12, 30)
    token.refresh_expiration = datetime(1000, 12, 30)

    response = database_with_data.put('api/v1/tokens', json={
        'access_token': access_token, 'refresh_token': refresh_token
    })
    assert response.status_code == 401


def test_token_revoked(database_with_data, tokens):
    """
    Given tokens,
    When the tokens are revoked,
    Then the tokens should be invalid.
    """
    access_token, refresh_token = tokens

    response = database_with_data.delete('api/v1/tokens', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 204

    response = database_with_data.put('api/v1/tokens', json={
        'access_token': access_token, 'refresh_token': refresh_token
    })
    assert response.status_code == 401
