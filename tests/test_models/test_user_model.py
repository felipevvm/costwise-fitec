import pytest

from src import db
from src.models import User


def test_user_repr(database_with_data):
    """
    Given a user,
    When I call the repr method of the user object,
    Then the method should return a string with the user id and username.
    """
    user = db.session.get(User, 1)
    assert user is not None
    assert repr(user) == f'<User {user.id}-{user.username}>'


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
    Then the property should be set to the hashed password.
    """
    user = db.session.get(User, 1)
    assert user is not None
    user.password = 'test0'
    assert user.verify_password('test0')
    assert not user.verify_password('test1')


def test_url(database_with_data):
    """
    Given a user,
    When I call the url property of the user object,
    Then the URL should be '/api/v1/users/<id>'.
    """
    user = db.session.get(User, 1)
    assert user is not None
    assert user.url == '/api/v1/users/' + str(user.id)
