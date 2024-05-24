from src import db
from src.models import Task, Member


def test_task_members(database_with_data):
    """
    Given a task with members,
    When I call the members property of the task object,
    Then the members property should return a list of the task's members.
    """
    task = db.session.get(Task, 1)
    assert task is not None
    assert task.members == []

    # assign a member to a task
    member = db.session.get(Member, 1)
    task.members.append(member)

    assert len(task.members) == 1
    assert task.members[0].name_member == 'test_member'
    assert task.members[0].id == 1


def test_task_repr(database_with_data):
    """
    Given a task,
    When I call the repr method of the task object,
    Then the method should return a string with the task id, name and deadline.
    """
    task = db.session.get(Task, 1)
    assert task is not None
    assert repr(task) == f'<Task {task.id}-{task.name_task}-{task.deadline}>'


def test_url(database_with_data):
    """
    Given a task,
    When I call the url property of the task object,
    Then the URL should be '/api/v1/project/<project_id>/tasks/<id>'.
    """
    task = db.session.get(Task, 1)
    assert task is not None
    assert task.url == f'/api/v1/projects/{task.project.id}/tasks/{task.id}'


def test_assign_member(database_with_data):
    """
    Given a task and a member,
    When I call the assign_member method of the task object,
    Then the member should be added to the task's members list.
    """
    task = db.session.get(Task, 1)
    assert task is not None
    assert task.members == []

    member = db.session.get(Member, 1)
    task.assign_member(member)

    assert len(task.members) == 1
    assert task.members[0].name_member == 'test_member'
    assert task.members[0].id == 1


def test_has_member(database_with_data):
    """
    Given a task with a member,
    When I call the has_member method of the task object with the member,
    Then the method should return True.
    """
    task = db.session.get(Task, 1)
    assert task is not None
    assert task.members == []

    member = db.session.get(Member, 1)
    task.assign_member(member)

    assert task.has_member(member) is True


def test_total_months(database_with_data):
    """
    Given a task with a duration of 6 months,
    When I call the total_months property of the task object,
    Then the total_months property should return 6.
    """
    task = db.session.get(Task, 1)
    assert task is not None
    assert task.total_months() == 6
