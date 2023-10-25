import pytest
import tempfile
import os
from project import create_app
from project.db import get_db, init_db

# load sql script
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def test_app():
    # create a temporary file and store the path in DATABASE
    app = create_app(testing=True)

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)  # load test data

    yield app


@pytest.fixture
def test_runner(test_app):
    return test_app.test_cli_runner()


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


class AuthActions(object):
    def __init__(self, test_client):
        self._test_client = test_client

    def login(self, email="test_email1", password="test_pw1"):
        return self._test_client.post(
            "/auth/login", data={"email": email, "password": password}
        )

    def logout(self):
        return self._test_client.get("/auth/logout")


@pytest.fixture
def auth_fixture(test_client):
    return AuthActions(test_client)
