from src import db
from src.models import Member, Task, Project


def test_member_tasks(database_with_data):
    """
    Given a member with tasks,
    When I call the tasks property of the member object,
    Then the property should return a list of the member's tasks.
    """
    member = db.session.get(Member, 1)
    assert member is not None
    assert member.tasks == []

    # assign a task to a member
    task = db.session.get(Task, 1)
    member.tasks.append(task)

    assert len(member.tasks) == 1
    assert member.tasks[0].name_task == 'test_task'


def test_member_repr(database_with_data):
    """
    Given a member,
    When I call the repr method of the member object,
    Then the method should return a string with the member id, name and role.
    """
    member = db.session.get(Member, 1)
    assert member is not None
    assert repr(member) == f'<Member {member.id}-{member.name_member}-{member.role}>'


def test_url(database_with_data):
    """
    Given a member,
    When I call the url property of the member object,
    Then the URL should be '/api/v1/project/<project_id>/members/<id>'.
    """
    member = db.session.get(Member, 1)
    assert member is not None
    assert member.url == f'/api/v1/projects/{member.project.id}/members/{member.id}'


def test_assign_task(database_with_data):
    """
    Given a member and a task,
    When I call the assign_task method of the member object,
    Then the task should be added to the member's tasks list.
    """
    member = db.session.get(Member, 1)
    assert member is not None
    assert member.tasks == []

    task = db.session.get(Task, 1)
    member.assign_task(task)

    assert len(member.tasks) == 1
    assert member.tasks[0].name_task == 'test_task'


def test_has_task(database_with_data):
    """
    Given a member with a task,
    When I call the has_task method of the member object,
    Then the method should return True.
    """
    member = db.session.get(Member, 1)
    assert member is not None
    assert member.tasks == []

    task = db.session.get(Task, 1)
    member.assign_task(task)

    assert member.has_task(task) is True


def test_calc_total_cost(database_with_data):
    """
    Given a member with tasks,
    When I call the total_cost property of the member object,
    Then the property should return the total cost of the member.
    """
    member = db.session.get(Member, 1)
    assert member is not None
    assert member.tasks == []

    # assign a task to a member
    task = db.session.get(Task, 1)
    member.assign_task(task)

    assert member.calc_total_cost() == 6000


def test_calc_costs_for_all_members(database_with_data):
    """
    Given a project with members and tasks,
    When I call the calc_cost_for_all_members method of the Member model,
    Then the total cost of all members should be calculated.
    """
    project = db.session.get(Project, 1)
    assert project is not None

    # assign task 0 to all members
    project.members[0].assign_task(project.tasks[0])
    project.members[1].assign_task(project.tasks[0])

    cost_for_all_member = [
        {
            'member': 'test_member',
            'total_cost': 6000
        },
        {
            'member': 'test_member2',
            'total_cost': 600
        }
    ]

    assert Member.calc_costs_for_all_members(project.id) == cost_for_all_member
