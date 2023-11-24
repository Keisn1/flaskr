from flask import session
import pytest
from project.db import get_db


def test_login_logout_on_index_page(test_client, auth_fixture):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Sign Up" in response.data

    r = auth_fixture.login()
    assert r.headers["Location"] == "/videos/"
    assert r.status_code == 302
    with test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert session["userId"] == 1
        assert b"Login" not in response.data
        assert b"Sign Up" not in response.data
        assert b"Logout" in response.data
        response = test_client.get("/auth/logout")
        assert response.headers["Location"] == "/videos/"
        assert "user_id" not in session
        response = test_client.get("/")
        assert b"Login" in response.data
        assert b"Sign Up" in response.data
        assert b"Logout" not in response.data


def test_logout(test_client, auth_fixture):
    auth_fixture.login()

    with test_client:
        auth_fixture.logout()
        assert "user_id" not in session


def test_login(test_client):
    response = test_client.get("/auth/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    response = test_client.post(
        "/auth/login", data={"email": "test_email1", "password": "test_pw1"}
    )
    assert response.status_code == 302  # route redirection
    assert response.headers["Location"] == "/videos/"


def test_signup(test_app, test_client):
    response = test_client.get("/auth/signup")
    assert response.status_code == 200

    with test_app.app_context():
        row = (
            get_db()
            .execute("SELECT * FROM users WHERE email = 'none_existing_email'")
            .fetchone()
        )
        assert row is None

    response = test_client.post(
        "/auth/signup",
        data={
            "name": "non_existing_name",
            "email": "non_existing_email",
            "password": "non_existing_password",
        },
    )
    assert response.status_code == 302  # route redirection
    assert response.headers["Location"] == "/auth/login"
    with test_app.app_context():
        row = (
            get_db()
            .execute("SELECT * FROM users WHERE email = 'test_email2'")
            .fetchone()
        )
        assert row is not None


# parametrize
@pytest.mark.parametrize(
    ("name", "email", "password", "message"),
    (
        ("", "a", "a", b"Name is required"),
        ("a", "", "a", b"Email is required"),
        ("a", "a", "", b"Password is required"),
        (
            "test_name1",
            "test_email1",
            "test_pw",
            b"user with test_email1 is already registered",
        ),
    ),
)
def test_validate_signup_input(test_client, name, email, password, message):
    data = {"name": name, "email": email, "password": password}
    r = test_client.post("/auth/signup", data=data)
    assert message in r.data


# parametrize
@pytest.mark.parametrize(
    ("email", "password", "message"),
    (
        ("a", "test_pw1", b"Incorrect user email"),
        ("test_email1", "a", b"Incorrect password"),
    ),
)
def test_login_validate_input(test_client, email, password, message):
    data = {"email": email, "password": password}
    r = test_client.post("/auth/login", data=data)
    assert message in r.data
