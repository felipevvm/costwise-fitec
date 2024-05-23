from datetime import date, timedelta

import pytest

from src import create_app, db
from src.models import User, Project, Member, Task, Product, Token


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


@pytest.fixture
def app_database(app):
    """ Initialize the database for the tests."""
    db.create_all()

    yield app

    db.drop_all()
    db.session.commit()


@pytest.fixture
def database_with_data(app_database):
    """ Populate the database with some data. """

    # Create a User
    user = User(
        id=1,
        email='test@test.com',
        username='test1',
        password='test1'
    )

    # Create a Project
    project = Project(
        id=1,
        name_project='test_project',
        description_project='test_description',
        deadline=date.today() + timedelta(days=(31*6)),
        owner=user
    )

    # Create a Task
    task = Task(
        id=1,
        name_task='test_task',
        description_task='test_description',
        deadline=date.today() + timedelta(days=31*6),
        project=project
    )

    # Create Members
    member1 = Member(
        id=1,
        name_member='test_member',
        role='test_role',
        salary=1000,
        project=project
    )

    member2 = Member(
        id=2,
        name_member='test_member2',
        role='test_role',
        salary=100,
        project=project
    )

    # Create a Product(Hardware)
    product_hardware_no_license = Product(
        id=1,
        name_product='hardware_no_license',
        description_product='test_description',
        license=0,
        type='HARDWARE',
        cost=1000,
        amount=1,
        project=project
    )

    product_hardware_license = Product(
        id=2,
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
        id=3,
        name_product='software_no_license',
        description_product='test_description',
        license=0,
        type='SOFTWARE',
        cost=100,
        amount=1,
        project=project
    )

    product_software_license = Product(
        id=4,
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
        id=5,
        name_product='other_no_license',
        description_product='test_description',
        license=0,
        type='OTHER',
        cost=10,
        amount=1,
        project=project
    )

    product_other_license = Product(
        id=6,
        name_product='other_license',
        description_product='test_description',
        license=1,
        type='OTHER',
        cost=10,
        amount=1,
        project=project
    )

    db.session.add_all([user, project, task, member1, member2, product_hardware_no_license, product_hardware_license,
                        product_software_no_license, product_software_license, product_other_no_license,
                        product_other_license])
    db.session.commit()

    yield app_database

    db.session.query(User).delete()
    db.session.query(Project).delete()
    db.session.query(Task).delete()
    db.session.query(Member).delete()
    db.session.query(Product).delete()
    db.session.commit()


@pytest.fixture
def tokens(database_with_data):
    """ Create a token for the user test1 """
    response = database_with_data.post('api/v1/tokens', auth=('test1', 'test1'))
    assert response.status_code == 200

    return response.json['access_token'], response.json['refresh_token']
