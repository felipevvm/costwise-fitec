from src import db
from src.models import Project


def test_project_members(database_with_data):
    """
    Given a project with members,
    When I call the members property of the project object,
    Then the property should return a list of the project's members.
    """
    project = db.session.get(Project, 1)
    assert project is not None
    assert project.members is not None
    assert len(project.members) == 1
    assert project.members[0].name_member == 'test_member'


def test_project_tasks(database_with_data):
    """
    Given a project with tasks,
    When I call the tasks property of the project object,
    Then the property should return a list of the project's tasks.
    """
    project = db.session.get(Project, 1)
    assert project is not None
    assert project.tasks is not None
    assert len(project.tasks) == 1
    assert project.tasks[0].name_task == 'test_task'


def test_project_products(database_with_data):
    """
    Given a project with products,
    When I call the products property of the project object,
    Then the property should return a list of the project's products.
    """
    project = db.session.get(Project, 1)
    assert project is not None
    assert project.products is not None
    assert len(project.products) == 6
    assert project.products[0].name_product == 'hardware_no_license'
    assert project.products[1].name_product == 'hardware_license'
    assert project.products[2].name_product == 'software_no_license'
    assert project.products[3].name_product == 'software_license'
    assert project.products[4].name_product == 'other_no_license'
    assert project.products[5].name_product == 'other_license'


def test_project_repr(database_with_data):
    """
    Given a project,
    When I call the repr method of the project object,
    Then the method should return a string with the project id, name and user id.
    """
    project = db.session.get(Project, 1)
    assert project is not None
    assert repr(project) == f'<Project {project.id}-{project.name_project}-{project.user_id}>'


def test_url(database_with_data):
    """
    Given a project,
    When I call the url property of the project object,
    Then the URL should be '/api/v1/projects/<id>'.
    """
    project = db.session.get(Project, 1)
    assert project is not None
    assert project.url == '/api/v1/projects/' + str(project.id)


def test_total_months(database_with_data):
    """
    Given a project with tasks,
    When I call the total_months property of the project object,
    Then the property should return the difference in months between the start and end dates of the project.
    """
    project = db.session.get(Project, 1)
    assert project is not None
    assert project.total_months() == 6


def test_calc_cost_total_member(database_with_data):
    """
    Given a project with members,
    When I call the calc_cost_total_member method of the project object,
    Then the cost_total_member property should be set to the sum of the costs of the project's members.
    """
    project = db.session.get(Project, 1)
    assert project is not None

    # assign a task to a member
    project.members[0].tasks.append(project.tasks[0])

    project.calc_cost_total_member()
    assert project.total_cost_members == 6000


def test_calc_cost_total_product(database_with_data):
    """
    Given a project with products,
    When I call the calc_cost_total_product method of the project object,
    Then the cost_total_product property should be set to the sum of the costs of the project's products.
    """
    project = db.session.get(Project, 1)
    assert project is not None

    project.calc_cost_total_products()
    assert project.total_cost_products == 7770


def test_calc_budget(database_with_data):
    """
    Given a project with members and products,
    When I call the calc_budget method of the project object,
    Then the budget property should be set sum of the costs of the project's members and products.
    """
    project = db.session.get(Project, 1)
    assert project is not None

    # assign a task to a member
    project.members[0].tasks.append(project.tasks[0])
    project.calc_cost_total_member()
    project.calc_cost_total_products()

    project.calc_budget()
    assert project.budget == 13770


def test_update_budget(database_with_data):
    """
    Given a project with members and products,
    When I call the update_budget method of the project object,
    Then the total_cost_members, total_cost_products and budget properties should be updated.
    """
    project = db.session.get(Project, 1)
    assert project is not None

    # assign a task to a member
    project.members[0].tasks.append(project.tasks[0])

    project.update_budget()
    assert project.total_cost_members == 6000
    assert project.total_cost_products == 7770
    assert project.budget == 13770
