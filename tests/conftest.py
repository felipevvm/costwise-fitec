import pytest

from src import create_app


@pytest.fixture(scope='module')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()
