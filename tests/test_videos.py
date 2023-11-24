from flask import url_for, g
from pluggy import _result
import pytest
from werkzeug.datastructures import auth
from werkzeug.wrappers import response

from project.db import get_db


def test_index(test_client, auth_fixture):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"<h2>All Videos</h2>" in response.data
    assert b"test_title1" in response.data
    assert b"test_title2" in response.data

    # test section with public videos and user videos
    auth_fixture.login()
    response = test_client.get("/")
    assert b"<h2>All Videos</h2>" in response.data
    assert b"<h2>My Videos</h2>" in response.data
    assert b'<a href="/videos/create">Create a new video</a>' in response.data
    assert b"test_title1" in response.data
    assert b"test_title1" in response.data
    assert b"test_title2" in response.data


@pytest.mark.parametrize(
    "path",
    (
        "/videos/create",
        "/videos/1/update",
        "/videos/1/delete",
    ),
)
def test_login_required(test_client, path):
    response = test_client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_get_create(test_client, auth_fixture):
    auth_fixture.login()
    response = test_client.get("/videos/create")
    assert (
        response.status_code == 200
    )  # name_field, description_field, video_path_field, submit_button
    assert b"<h1>Create Video</h1>" in response.data
    assert (
        b'<label for="video_title">Enter a title for the video:<input type="text" name="video_title" value="video_title"'
        in response.data
    )
    assert (
        b'<label for="video_description"><textarea name="video_description" value="video_description"'
        in response.data
    )
    assert (
        b'<label for="video_path">Upload<input type="text" name="video_path" value="video_path">'
        in response.data
    )
    assert b'<button type="submit">Upload video</button>' in response.data


def test_create(test_client, auth_fixture, test_app):
    auth_fixture.login()
    with test_app.app_context():
        data = {
            "title": "test_create_title1",
            "description": "test_create_description1",
            "videoPath": "test_create_path1",
        }
        assert (
            get_db()
            .execute("select * from videos where title == ?", (data["title"],))
            .fetchall()
            == []
        )
        response = test_client.post("/videos/create", data=data)
        assert response.status_code == 302
        assert response.headers["Location"] == "/videos/"
        new_data = (
            get_db()
            .execute("select * from videos where title == ?", (data["title"],))
            .fetchall()
        )
        assert len(new_data) == 1
        new_data = new_data[0]
        assert new_data["title"] == data["title"]
        assert new_data["description"] == data["description"]
        assert new_data["videoPath"] == data["videoPath"]
        assert new_data["userId"] == g.user["userId"]


def test_update(test_client, auth_fixture, test_app):
    """tests that update actually happened"""
    auth_fixture.login()
    with test_app.app_context():
        response = test_client.get("/")
        user_videos = (
            get_db()
            .execute("select * from videos where userId == ?", (g.user["userId"],))
            .fetchall()
        )
        assert len(user_videos)
        video_id = user_videos[0]["videoId"]
        data = {
            "title": "new_title",
            "description": "new_description",
            "videoPath": "new_path",
        }
        response = test_client.post(f"videos/{video_id}/update", data=data)

        new_video = (
            get_db()
            .execute("select * from videos where userId == ?", (video_id,))
            .fetchone()
        )

        for key, val in data.items():
            assert new_video[key] == data[key]


@pytest.mark.parametrize(
    "path,data,message",
    (
        (
            "/videos/create",
            {
                "title": "",
                "description": "test_create_description1",
                "videoPath": "test_create_path1",
            },
            b"Video title is required",
        ),
        (
            "/videos/create",
            {
                "title": "test_create_title",
                "description": "test_create_description1",
                "videoPath": "",
            },
            b"Video path is required",
        ),
    ),
)
def test_create_update_validate(test_client, auth_fixture, path, data, message):
    """
    Validates input of create and update (title/path required)
    (login required tested earlier)
    """
    auth_fixture.login()
    response = test_client.post(
        path,
        data=data,
    )
    assert message in response.data


def test_exists_required(client, auth, path):
    """tests that video that shall be updated or deleted exists"""
    response = client.post(path)
    assert response.status_code == 404
    get_db().execute("delete from videos where videoId == 1")
    response = client.post(path)


def test_author_required(client, auth, path):
    """Requires the author of change to be author of create"""
    pass


def test_delete(client, auth, app):
    """tests that delete actually happened"""
