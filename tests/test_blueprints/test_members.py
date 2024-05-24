from datetime import date

import pytest

invalid_members_id = [0, -1, 1.5, 99999999999999]


def test_get_members(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/members,
    When the method is GET and the user provides a valid project id,
    Then the user should receive a 200 status code and the members' data.
    """
    response = database_with_data.get('api/v1/projects/1/members', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['id'] == 1
    assert response.json[0]['name_member'] == 'test_member'
    assert response.json[0]['role'] == 'test_role'
    assert response.json[0]['salary'] == 1000
    assert response.json[0]['project_id'] == 1


def test_new_member(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/members,
    When the method is POST and the user provides valid data,
    Then the user should receive a 201 status code and the new member data.
    """
    response = database_with_data.post('api/v1/projects/1/members', json={
        'name_member': 'test_member3',
        'role': 'test_role',
        'salary': 1000,
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 201
    assert response.json['id'] == 3
    assert response.json['name_member'] == 'test_member3'
    assert response.json['role'] == 'test_role'
    assert response.json['salary'] == 1000
    assert response.json['project_id'] == 1


def test_get_member(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/members/<member_id>,
    When the method is GET and the user provides a valid member id,
    Then the user should receive a 200 status code and the member data.
    """
    response = database_with_data.get('api/v1/projects/1/members/1', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name_member'] == 'test_member'
    assert response.json['role'] == 'test_role'
    assert response.json['salary'] == 1000
    assert response.json['project_id'] == 1


@pytest.mark.parametrize('member_id', invalid_members_id)
def test_get_member_invalid_member_id(database_with_data, access_token_valid, member_id):
    """
    Given the protected endpoint /projects/<project_id>/members/<member_id>,
    When the method is GET and the user provides an invalid member id,
    Then the user should receive a 404 status code.
    """
    response = database_with_data.get(f'api/v1/projects/1/members/{member_id}', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 404


def test_update_member(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/members/<member_id>,
    When the method is PUT and the user provides valid data,
    Then the user should receive a 200 status code and the updated member data.
    """
    response = database_with_data.put('api/v1/projects/1/members/1', json={
        'name_member': 'test_member_updated',
        'role': 'test_role_updated',
        'salary': 2000,
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name_member'] == 'test_member_updated'
    assert response.json['role'] == 'test_role_updated'
    assert response.json['salary'] == 2000
    assert response.json['project_id'] == 1


def test_update_member_invalid_data(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/members/<member_id>,
    When the method is PUT and the user provides invalid data,
    Then the user should receive a 400 status code.
    """
    response = database_with_data.put('api/v1/projects/1/members/1', json={
        'name_member': 10.0,
        'role': True,
        'salary': '12-2400-01',
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 400


def test_delete_member(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/members/<member_id>,
    When the method is DELETE and the user provides a valid member id,
    Then the user should receive a 204 status code.
    """
    response = database_with_data.delete('api/v1/projects/1/members/1', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 204


def test_assign_task(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/members/<member_id>/<task_id>,
    When the method is PUT and the user provides valid data,
    Then the user should receive a 200 status code and the updated member data.
    """
    response = database_with_data.put('api/v1/projects/1/members/1/1', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name_member'] == 'test_member'
    assert response.json['role'] == 'test_role'
    assert response.json['salary'] == 1000
    assert response.json['project_id'] == 1
    assert response.json['tasks'][0]['id'] == 1
