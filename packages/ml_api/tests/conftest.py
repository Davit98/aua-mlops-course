import pytest
from api.app import create_app
from api.config import TestingConfig


@pytest.fixture(scope='session')
def app():
    app = create_app(config_object=TestingConfig()).app
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client  # has to be yielded to access session cookies
