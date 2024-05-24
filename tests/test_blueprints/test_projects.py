from datetime import date

import pytest

invalid_projects_id = [0, -1, 1.5, 99999999999999]


def test_get_projects(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects,
    When the method is GET,
    Then the user should receive a 200 status code and a list of the user's projects.
    """
    response = database_with_data.get('api/v1/projects', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['user_id'] == 1


def test_new_project(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects,
    When the method is POST and the user provides valid data,
    Then the user should receive a 200 status code and the new project data.
    """
    response = database_with_data.post('api/v1/projects', json={
        'name_project': 'test_project',
        'description_project': 'test_description',
        'deadline': '2024-12-31',
        'expected_budget': 10000,
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['name_project'] == 'test_project'
    assert response.json['description_project'] == 'test_description'
    assert response.json['deadline'] == '2024-12-31'
    assert response.json['created_at'] == date.today().isoformat()
    assert float(response.json['expected_budget']) == 10000


def test_get_project(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>,
    When the method is GET and the user provides a valid project id,
    Then the user should receive a 200 status code and the project data.
    """
    response = database_with_data.get('api/v1/projects/1', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name_project'] == 'test_project'
    assert response.json['description_project'] == 'test_description'
    assert response.json['deadline'] == '2024-11-26'
    assert response.json['created_at'] == date.today().isoformat()
    assert float(response.json['expected_budget']) == 10000


@pytest.mark.parametrize('project_id', invalid_projects_id)
def test_get_project_invalid_id(database_with_data, access_token_valid, project_id):
    """
    Given the protected endpoint /projects/<project_id>,
    When the method is GET and the user provides an invalid project id,
    Then the user should receive a 404 status code.
    """
    response = database_with_data.get(f'api/v1/projects/{project_id}', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 404


def test_update_project(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>,
    When the method is PUT and the user provides valid data,
    Then the user should receive a 200 status code and the updated project data.
    """
    response = database_with_data.put('api/v1/projects/1', json={
        'name_project': 'test_project2',
        'description_project': 'test_description2',
        'deadline': '2024-12-31',
        'expected_budget': 20000,
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['name_project'] == 'test_project2'
    assert response.json['description_project'] == 'test_description2'
    assert response.json['deadline'] == '2024-12-31'
    assert response.json['created_at'] == date.today().isoformat()
    assert float(response.json['expected_budget']) == 20000


def test_update_project_invalid_data(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>,
    When the method is PUT and the user provides invalid data,
    Then the user should receive a 400 status code.
    """
    response = database_with_data.put('api/v1/projects/1', json={
        'name_project': 10.0,
        'description_project': 2,
        'deadline': '31-2024-12',
        'expected_budget': '20000',
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 400


def test_delete_project(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>,
    When the method is DELETE and the user provides a valid project id,
    Then the user should receive a 204 status code and the project should be deleted.
    """
    response = database_with_data.delete('api/v1/projects/1', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 204


def test_get_cost_of_all_members(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/members_costs,
    When the method is GET and the user provides a valid project id,
    Then the user should receive a 200 status code and the total cost of all members.
    """
    response = database_with_data.get('api/v1/projects/1/members_costs', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert len(response.json['Members']) == 2
    assert response.json['Members'][0]['member'] == 'test_member'
    assert response.json['Members'][0]['total_cost'] == 0


def test_get_cost_of_all_products_by_license(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/products_by_license,
    When the method is GET and the user provides a valid project id,
    Then the user should receive a 200 status code and the total cost of all products by license.
    """
    response = database_with_data.get('api/v1/projects/1/products_by_license', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['no_license_cost'] == 1110
    assert response.json['license_cost'] == 6660


def test_get_cost_of_all_products_by_type(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/products_by_type,
    When the method is GET and the user provides a valid project id,
    Then the user should receive a 200 status code and the total cost of all products by type.
    """
    response = database_with_data.get('api/v1/projects/1/products_by_type', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['HARDWARE'] == 7000
    assert response.json['SOFTWARE'] == 700
    assert response.json['OTHER'] == 70
