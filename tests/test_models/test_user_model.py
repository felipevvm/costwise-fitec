from time import time

import jwt
import pytest
from flask import current_app

from src import db
from src.models import User


def test_user_projects(database_with_data):
    """
    Given a user with projects,
    When I call the projects property of the user object,
    Then the property should return a list of the user's projects.
    """
    user = db.session.get(User, 1)
    assert user is not None
    assert user.projects is not None
    assert len(user.projects) == 1
    assert user.projects[0].name_project == 'test_project'


def test_user_repr(database_with_data):
    """
    Given a user,
    When I call the repr method of the user object,
    Then the method should return a string with the user id and username.
    """
    user = db.session.get(User, 1)
    assert user is not None
    assert repr(user) == f'<User {user.id}-{user.username}>'


def test_url(database_with_data):
    """
    Given a user,
    When I call the url property of the user object,
    Then the URL should be '/api/v1/users/<user_id>'.
    """
    user = db.session.get(User, 1)
    assert user is not None
    assert user.url == '/api/v1/users/' + str(user.id)


def test_password(database_with_data):
    """
    Given a user with a password,
    When I call the password property of the user object,
    Then the property should raise an AttributeError.
    """
    user = db.session.get(User, 1)
    assert user is not None
    assert not user.verify_password('test0')
    with pytest.raises(AttributeError):
        assert user.password


def test_password_setter(database_with_data):
    """
    Given a user,
    When I set the password property of the user object,
    Then the value should be hashed and set to the password_hash.
    """
    user = db.session.get(User, 1)
    assert user is not None
    user.password = 'test0'
    assert user.verify_password('test0')
    assert not user.verify_password('test1')


def test_verify_password(database_with_data):
    """
    Given a user with a password,
    When I call the verify_password method of the user object,
    Then the method should return True if the password is correct, otherwise False.
    """
    user = db.session.get(User, 1)
    assert user is not None
    assert user.verify_password('test1')
    assert not user.verify_password('test0')


def test_generate_auth_token(database_with_data):
    """
    Given a user,
    When the generate_auth_token method is called,
    Then the method should return a token object
    """
    user = db.session.get(User, 1)
    token = user.generate_auth_token()
    db.session.add(token)
    db.session.commit()
    assert token is not None
    assert token.user == user
    assert token.access_token is not None
    assert token.refresh_token is not None
    assert token.access_expiration is not None
    assert token.refresh_expiration is not None


def test_verify_access_token(database_with_data, tokens):
    """
    Given a user and a token,
    When the verify_access_token method is called,
    Then the method should return the user object if the token is valid.
    """
    user = db.session.get(User, 1)
    access_token, _ = tokens
    assert user.verify_access_token(access_token) == user
    assert user.verify_access_token('invalid') is None


def test_verify_refresh_token(database_with_data, tokens):
    """
    Given a user and a token,
    When the verify_refresh_token method is called,
    Then the method should return the token object if the token is valid.
    """
    user = db.session.get(User, 1)
    access_token, refresh_token = tokens
    token = user.verify_refresh_token(refresh_token, access_token)
    assert token is not None
    assert token.user == user


def test_verify_refresh_token_revoke(database_with_data, tokens):
    """
    Given a user and an expired refresh token,
    When the verify_refresh_token method is called,
    Then the method should revoke all tokens from the user.
    """
    user = db.session.get(User, 1)
    access_token, refresh_token = tokens
    token = user.verify_refresh_token(refresh_token, access_token)
    assert token is not None
    token.expire()
    db.session.add(token)
    db.session.commit()
    user.verify_refresh_token(refresh_token, access_token)
    assert user.tokens == []


def test_revoke_all(database_with_data, tokens):
    """
    Given a user,
    When the revoke_all method is called,
    Then all tokens should be revoked.
    """
    user = db.session.get(User, 1)
    assert user.tokens != []
    user.revoke_all()
    assert user.tokens == []


def test_generate_reset_token(database_with_data):
    """
    Given a user,
    When the generate_reset_token method is called,
    Then the method should return a token object
    """
    user = db.session.get(User, 1)
    reset_token = user.generate_reset_token()
    time_now = time()
    reset_token_jwt = jwt.encode(
        {
            'exp': time_now + current_app.config['RESET_TOKEN_MINUTES'] * 60,
            'email': user.email
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    assert reset_token is not None
    assert reset_token == reset_token_jwt


def test_verify_reset_token(database_with_data):
    """
    Given a user and a token,
    When the verify_reset_token method is called,
    Then the method should return the user object if the token is valid.
    """
    user = db.session.get(User, 1)
    reset_token = user.generate_reset_token()
    assert user.verify_reset_token(reset_token) == user
    assert user.verify_reset_token('invalid') is None
    assert user.verify_reset_token('') is None
