import pytest

from src import db
from src.models import User

invalid_users_id = [0, -1, 1.5, 99999999999999]


def test_get_users(database_with_data):
    """
    Given the endpoint /users,
    When the method is GET,
    Then the user should receive a 200 status code and a list of users.
    """
    response = database_with_data.get('api/v1/users')

    assert response.status_code == 200
    assert len(response.json) == 1


def test_new_user(database_with_data):
    """
    Given the endpoint /users,
    When the method is POST and the user provides valid data,
    Then the user should receive a 201 status code and the new user data.
    """
    response = database_with_data.post('api/v1/users', json={
        'username': 'test2',
        'email': 'test2@test2.com',
        'password': 'test2'
    })
    assert response.status_code == 201
    assert response.json['id'] == 2
    assert response.json['email'] == 'test2@test2.com'
    assert response.json['username'] == 'test2'
    assert db.session.get(User, 2).verify_password('test2')


def test_get_user(database_with_data, access_token_valid):
    """
    Given the protected endpoint /users/<user_id>,
    When the method is GET and the user provides a valid user id,
    Then the user should receive a 200 status code and the user data.
    """
    response = database_with_data.get('api/v1/users/1', headers={'Authorization': f'Bearer {access_token_valid}'})

    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['username'] == 'test1'


@pytest.mark.parametrize('user_id', invalid_users_id)
def test_get_user_invalid_id(database_with_data, access_token_valid, user_id):
    """
    Given the protected endpoint /users/<user_id>,
    When the method is GET and the user provides an invalid user id,
    Then the user should receive a 404 status code.
    """
    response = database_with_data.get(f'api/v1/users/{user_id}', headers={
        'Authorization': f'Bearer {access_token_valid}'})

    assert response.status_code == 404


def test_update_user(database_with_data, access_token_valid):
    """
    Given the protected endpoint /users,
    When the method is PUT and the user provides valid data,
    Then the user should receive a 200 status code and the updated user data.
    """
    response = database_with_data.put('api/v1/users', json={
        'username': 'test2',
        'email': 'test2@test2.com',
        'password': 'test2'
    }, headers={'Authorization': f'Bearer {access_token_valid}'})

    assert response.status_code == 200
    assert response.json['email'] == 'test2@test2.com'
    assert response.json['username'] == 'test2'
    assert db.session.get(User, 1).verify_password('test2')


def test_update_user_invalid_data(database_with_data, access_token_valid):
    """
    Given the protected endpoint /users,
    When the method is PUT and the user provides invalid data,
    Then the user should receive a 400 status code.
    """
    response = database_with_data.put('api/v1/users', json={
        'username': 100,
        'email': 'abc',
        'password': False
    }, headers={'Authorization': f'Bearer {access_token_valid}'})

    assert response.status_code == 400


def test_delete_user(database_with_data, access_token_valid):
    """
    Given the protected endpoint /users,
    When the method is DELETE,
    Then the user should receive a 204 status code and the user should be deleted.
    """
    response = database_with_data.delete('api/v1/users', headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 204
    assert db.session.query(User).count() == 0
