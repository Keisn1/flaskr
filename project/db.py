import click
import sqlite3

from flask import current_app, g


def connect_db():
    db = sqlite3.connect(
        current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    return db


def get_db():
    if not hasattr(g, "db"):
        g.db = connect_db()
    return g.db


def init_db():
    # execute sql script
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


# add init_db_command to the app.cli
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo("Initialized Database")


def init_app(app):
    # app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
