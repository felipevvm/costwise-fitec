from datetime import datetime, timedelta

import jwt
from flask import current_app

from src import db
from src.models import User, Token


def test_access_token_jwt_property(database_with_data):
    """
    Given a token,
    When I call the access_token property of the token object,
    Then the property should return the access token in jwt format.
    """
    user = db.session.get(User, 1)
    token = user.generate_auth_token()
    db.session.add(token)
    db.session.commit()
    access_jwt = jwt.encode({'token': token.access_token},
                            current_app.config['SECRET_KEY'],
                            algorithm='HS256')
    assert token.access_token_jwt == access_jwt


def test_generate(database_with_data):
    """
    Given  a token,
    When the generate method is called,
    Then the token data should be generated.
    """
    user = db.session.get(User, 1)
    token = Token(user=user)
    token.generate()
    db.session.add(token)
    db.session.commit()
    assert token.access_token is not None
    assert token.refresh_token is not None
    assert token.access_expiration > datetime.now()
    assert token.refresh_expiration > datetime.now()


def test_expire(database_with_data, tokens):
    """
    Given a token,
    When the expire method is called,
    Then the token should be expired.
    """
    access_token, refresh_token = tokens
    token = Token.from_jwt(access_token)
    assert token.access_expiration > datetime.now()

    token.expire()
    db.session.commit()

    assert token.access_expiration < datetime.now()
    db.session.delete(token)
    db.session.commit()


def test_clean(database_with_data):
    """
    Given a 1 day expired token,
    When the clean method is called,
    Then the token should be deleted.
    """
    user = db.session.get(User, 1)
    token = Token(
        user=user,
        access_token='a',
        access_expiration=datetime.now() - timedelta(days=1),
        refresh_token='r',
        refresh_expiration=datetime.now() - timedelta(days=1)
    )
    db.session.add(token)
    db.session.commit()
    assert db.session.query(Token).count() == 1

    token.clean()
    db.session.commit()

    assert db.session.query(Token).count() == 0


def test_from_jwt(database_with_data, tokens):
    """
    Given a token in jwt format,
    When the from_jwt method is called,
    Then the token object should be returned.
    """
    user = db.session.get(User, 1)
    access_token, refresh_token = tokens

    token = Token.from_jwt(access_token)

    assert token.user == user
    assert token.access_token_jwt == access_token
    assert token.refresh_token == refresh_token
