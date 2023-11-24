from flask import Blueprint, render_template, request, url_for, redirect, flash, g
from project.db import get_db

from project.views.auth import login_required

bp = Blueprint("videos", __name__, url_prefix="/videos")


@bp.route("/")
def index():
    videos = get_db().execute("select * from videos").fetchall()

    return render_template(
        "videos/index.html",
        videos=videos,
    )


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        video_path = request.form["videoPath"]

        error = None
        if not title:
            error = "Video title is required"

        if not video_path:
            error = "Video path is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "insert into videos (title, description, videoPath, userId) values (?, ?, ?, ?)",
                (title, description, video_path, g.user["userId"]),
            )
            db.commit()
            return redirect(url_for("videos.index"))

    return render_template("videos/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(video_id: int):
    # if request.method == "POST":
    return render_template("videos/create.html")


@bp.route("/<int:id>/delete", methods=("GET", "POST"))
@login_required
def delete(video_id: int):
    # if request.method == "POST":
    return render_template("videos/create.html")


# @bp.route("/")
# def index():
#     return render_template("videos/index.html")


# @bp.route("/")
# def index():
#     return render_template("videos/index.html")
