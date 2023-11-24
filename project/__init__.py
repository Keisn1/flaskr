import os
from . import db
from flask import Flask, render_template, session, g
from project.views import auth, videos


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    if testing:
        app.config.from_prefixed_env(prefix="TEST_FLASK")
        app.config.from_mapping({"TESTING": True})
    else:
        app.config.from_prefixed_env("FLASK")

    app.config["DATABASE"] = os.path.join(app.instance_path, app.config["DATABASE"])

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_request
    def load_user():
        if "userId" in session:
            g.user = {"userId": session["userId"]}

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(videos.bp)
    app.add_url_rule("/", endpoint="videos.index")

    return app
