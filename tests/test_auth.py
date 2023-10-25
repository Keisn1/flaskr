from flask import session
from project.db import get_db


def test_login_logout_on_index_page(test_client, auth_fixture):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Sign Up" in response.data

    r = auth_fixture.login()
    assert r.headers["Location"] == "/"
    with test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert session["userId"] == 1


def test_login(test_client):
    response = test_client.get("/auth/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    response = test_client.post(
        "/auth/login", data={"email": "test_email1", "password": "test_pw1"}
    )
    assert response.status_code == 302  # route redirection
    assert response.headers["Location"] == "/"


def test_signup(test_app, test_client):
    response = test_client.get("/auth/signup")
    assert response.status_code == 200

    with test_app.app_context():
        row = (
            get_db()
            .execute("SELECT * FROM users WHERE email = 'test_email2'")
            .fetchone()
        )
        assert row is None

    response = test_client.post(
        "/auth/signup",
        data={"name": "test_name2", "email": "test_email2", "password": "test_pw2"},
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


def test_validate_signup_input():
    pass
