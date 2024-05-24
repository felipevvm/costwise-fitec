from datetime import date

import pytest

invalid_tasks_id = [0, -1, 1.5, 99999999999999]


def test_get_tasks(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/tasks,
    When the method is GET,
    Then the user should receive a 200 status code and a list of the project's tasks.
    """
    response = database_with_data.get('api/v1/projects/1/tasks', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['project_id'] == 1


def test_new_task(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/tasks,
    When the method is POST and the user provides valid data,
    Then the user should receive a 200 status code and the new task data.
    """
    response = database_with_data.post('api/v1/projects/1/tasks', json={
        'name_task': 'test_task2',
        'description_task': 'test_description',
        'deadline': '2024-12-31',
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 201
    assert response.json['id'] == 2
    assert response.json['name_task'] == 'test_task2'
    assert response.json['description_task'] == 'test_description'
    assert response.json['deadline'] == '2024-12-31'
    assert response.json['created_at'] == date.today().isoformat()


def test_get_task(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/tasks/<task_id>,
    When the method is GET and the user provides a valid task id,
    Then the user should receive a 200 status code and the task data.
    """
    response = database_with_data.get('api/v1/projects/1/tasks/1', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name_task'] == 'test_task'
    assert response.json['description_task'] == 'test_description'
    assert response.json['deadline'] == '2024-11-26'
    assert response.json['created_at'] == date.today().isoformat()
    assert response.json['project_id'] == 1


@pytest.mark.parametrize('task_id', invalid_tasks_id)
def test_get_task_invalid_task_id(database_with_data, access_token_valid, task_id):
    """
    Given the protected endpoint /projects/<project_id>/tasks/<task_id>,
    When the method is GET and the user provides an invalid task id,
    Then the user should receive a 404 status code.
    """
    response = database_with_data.get(f'api/v1/projects/1/tasks/{task_id}', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 404


def test_update_task(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/tasks/<task_id>,
    When the method is PUT and the user provides valid data,
    Then the user should receive a 200 status code and the updated task data.
    """
    response = database_with_data.put('api/v1/projects/1/tasks/1', json={
        'name_task': 'test_task_updated',
        'description_task': 'test_description_updated',
        'deadline': '2024-12-31',
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name_task'] == 'test_task_updated'
    assert response.json['description_task'] == 'test_description_updated'
    assert response.json['deadline'] == '2024-12-31'
    assert response.json['created_at'] == date.today().isoformat()
    assert response.json['project_id'] == 1


def test_update_task_invalid_data(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/tasks/<task_id>,
    When the method is PUT and the user provides invalid data,
    Then the user should receive a 400 status code.
    """
    response = database_with_data.put('api/v1/projects/1/tasks/1', json={
        'name_task': 10.0,
        'description_task': 100,
        'deadline': '12-2400-01',
    }, headers={'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 400


def test_delete_task(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/tasks/<task_id>,
    When the method is DELETE and the user provides a valid task id,
    Then the user should receive a 204 status code.
    """
    response = database_with_data.delete('api/v1/projects/1/tasks/1', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 204


def test_assing_member(database_with_data, access_token_valid):
    """
    Given the protected endpoint /projects/<project_id>/tasks/<task_id>/<member_id>,
    When the method is PUT and the user provides valid data,
    Then the user should receive a 200 status code and the updated task data.
    """
    response = database_with_data.put('api/v1/projects/1/tasks/1/1', headers={
        'Authorization': f'Bearer {access_token_valid}'})
    assert response.status_code == 200
    assert response.json['members'][0]['id'] == 1
