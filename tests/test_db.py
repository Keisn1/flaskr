# Description: Test the database functions


# tests if script is executed
import project.db
from pathlib import Path
from project.db import get_db, connect_db, init_db


def test_init_db(test_app, mocker):
    mocker.patch("project.db.get_db")
    with test_app.app_context():
        init_db()
        project.db.get_db.assert_called_once()


def test_get_db(test_app, mocker):
    mocker.patch("project.db.connect_db")
    with test_app.app_context():
        get_db()
        project.db.connect_db.assert_called_once()


def test_connect_db(test_app):
    with test_app.app_context():
        connect_db()
        assert Path(test_app.config["DATABASE"]).is_file()


def test_app_registers_cli_command(test_runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("project.db.init_db", fake_init_db)
    result = test_runner.invoke(args=["init-db"])
    assert "Initialized Database" in result.output
    assert Recorder.called
