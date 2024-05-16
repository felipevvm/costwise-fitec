from datetime import date

import pytest

from src import create_app, db
from src.models import User, Project, Member, Task, Product


@pytest.fixture(scope='session')
def app():
    """ Instance of Main flask app"""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
    })

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope='session')
def app_database(app):
    """ Initialize the database for the tests."""
    db.create_all()

    yield app

    db.session.commit()
    db.drop_all()


@pytest.fixture
def database_with_data(app_database):
    """ Populate the database with some data. """

    # Create a User
    user = User(
        email='test@test.com',
        username='test1',
        password='test1'
    )

    # Create a Project
    project = Project(
        name_project='test_project',
        description_project='test_description',
        deadline=date(3000, 12, 30),
        owner=user
    )

    # Create a Task
    task = Task(
        name_task='test_task',
        description_task='test_description',
        deadline=date(3000, 12, 30),
        project=project
    )

    # Create a Member
    member = Member(
        name_member='test_member',
        role='test_role',
        salary=1000,
        project=project
    )

    # Create a Product(Hardware)
    product_hardware_no_license = Product(
        name_product='hardware_no_license',
        description_product='test_description',
        license=0,
        type='HARDWARE',
        cost=1000,
        amount=1,
        project=project
    )

    product_hardware_license = Product(
        name_product='hardware_license',
        description_product='test_description',
        license=1,
        type='HARDWARE',
        cost=1000,
        amount=1,
        project=project
    )

    # Create a Product(Software)
    product_software_no_license = Product(
        name_product='software_no_license',
        description_product='test_description',
        license=0,
        type='SOFTWARE',
        cost=100,
        amount=1,
        project=project
    )

    product_software_license = Product(
        name_product='software_license',
        description_product='test_description',
        license=1,
        type='SOFTWARE',
        cost=100,
        amount=1,
        project=project
    )

    # Create a Product(Other)
    product_other_no_license = Product(
        name_product='other_no_license',
        description_product='test_description',
        license=0,
        type='OTHER',
        cost=10,
        amount=1,
        project=project
    )

    product_other_license = Product(
        name_product='other_license',
        description_product='test_description',
        license=1,
        type='OTHER',
        cost=10,
        amount=1,
        project=project
    )

    db.session.add_all([user, project, task, member, product_hardware_no_license, product_hardware_license,
                        product_software_no_license, product_software_license, product_other_no_license,
                        product_other_license])
    db.session.commit()

    yield app_database

    db.session.delete(user)
    db.session.delete(project)
    db.session.delete(task)
    db.session.delete(member)
    db.session.delete(product_hardware_no_license)
    db.session.delete(product_hardware_license)
    db.session.delete(product_software_no_license)
    db.session.delete(product_software_license)
    db.session.delete(product_other_no_license)
    db.session.delete(product_other_license)
    db.session.commit()
