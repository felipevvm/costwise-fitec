from datetime import date, timedelta

from src import db
from src.models import User, Project, Member, Task, Product, ProductType


def test_empty_database(app_database):
    """
    Given an empty database,
    When the database is requested,
    Then the database is empty.
    """
    users = db.session.query(User).all()
    assert len(users) == 0

    projects = db.session.query(Project).all()
    assert len(projects) == 0

    tasks = db.session.query(Task).all()
    assert len(tasks) == 0

    members = db.session.query(Member).all()
    assert len(members) == 0

    products = db.session.query(Product).all()
    assert len(products) == 0


def test_user_data(database_with_data):
    """
    Given a database with a user,
    When the user is requested,
    Then the user data is returned.
    """
    user = db.session.get(User, 1)
    assert user is not None
    assert user.email == 'test@test.com'
    assert user.username == 'test1'
    assert user.verify_password('test1')


def test_project_data(database_with_data):
    """
    Given a database with a project,
    When the project is requested,
    Then the project data is returned.
    """
    project = db.session.get(Project, 1)
    assert project is not None
    assert project.name_project == 'test_project'
    assert project.description_project == 'test_description'
    assert project.deadline == date.today() + timedelta(days=(31*6))
    assert project.owner.id == 1


def test_task_data(database_with_data):
    """
    Given a database with a task,
    When the task is requested,
    Then the task data is returned.
    """
    task = db.session.get(Task, 1)
    assert task is not None
    assert task.name_task == 'test_task'
    assert task.description_task == 'test_description'
    assert task.deadline == date.today() + timedelta(days=31*6)
    assert task.project.id == 1


def test_member_data(database_with_data):
    """
    Given a database with a member,
    When the member is requested,
    Then the member data is returned.
    """
    member = db.session.get(Member, 1)
    assert member is not None
    assert member.name_member == 'test_member'
    assert member.role == 'test_role'
    assert member.salary == 1000
    assert member.project.id == 1


def test_product_data(database_with_data):
    """
    Given a database with products,
    When the products are requested,
    Then the products data is returned.
    """
    hardware_no_license = db.session.get(Product, 1)
    assert hardware_no_license is not None
    assert hardware_no_license.name_product == 'hardware_no_license'
    assert hardware_no_license.description_product == 'test_description'
    assert hardware_no_license.type == ProductType.HARDWARE
    assert hardware_no_license.license == 0
    assert hardware_no_license.cost == 1000
    assert hardware_no_license.amount == 1
    assert hardware_no_license.project.id == 1

    hardware_license = db.session.get(Product, 2)
    assert hardware_license is not None
    assert hardware_license.name_product == 'hardware_license'
    assert hardware_license.description_product == 'test_description'
    assert hardware_license.type == ProductType.HARDWARE
    assert hardware_license.license == 1
    assert hardware_license.cost == 1000
    assert hardware_license.amount == 1
    assert hardware_license.project.id == 1

    software_no_license = db.session.get(Product, 3)
    assert software_no_license is not None
    assert software_no_license.name_product == 'software_no_license'
    assert software_no_license.description_product == 'test_description'
    assert software_no_license.type == ProductType.SOFTWARE
    assert software_no_license.license == 0
    assert software_no_license.cost == 100
    assert software_no_license.amount == 1
    assert software_no_license.project.id == 1

    software_license = db.session.get(Product, 4)
    assert software_license is not None
    assert software_license.name_product == 'software_license'
    assert software_license.description_product == 'test_description'
    assert software_license.type == ProductType.SOFTWARE
    assert software_license.license == 1
    assert software_license.cost == 100
    assert software_license.amount == 1
    assert software_license.project.id == 1

    other_no_license = db.session.get(Product, 5)
    assert other_no_license is not None
    assert other_no_license.name_product == 'other_no_license'
    assert other_no_license.description_product == 'test_description'
    assert other_no_license.type == ProductType.OTHER
    assert other_no_license.license == 0
    assert other_no_license.cost == 10
    assert other_no_license.amount == 1
    assert other_no_license.project.id == 1

    other_license = db.session.get(Product, 6)
    assert other_license is not None
    assert other_license.name_product == 'other_license'
    assert other_license.description_product == 'test_description'
    assert other_license.type == ProductType.OTHER
    assert other_license.license == 1
    assert other_license.cost == 10
    assert other_license.amount == 1
    assert other_license.project.id == 1
    