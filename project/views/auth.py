import functools
from flask import (
    Blueprint,
    flash,
    g,
    current_app,
    render_template,
    redirect,
    session,
    url_for,
    request,
)
from werkzeug.security import generate_password_hash, check_password_hash
from project.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        error = None

        if not name:
            error = "Name is required"
        elif not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"

        if error is None:
            db = get_db()
            pw_hash = generate_password_hash(password)
            try:
                db.execute(
                    "insert into users (name, email, password) values (?,?,?)",
                    (
                        name,
                        email,
                        pw_hash,
                    ),
                )
                db.commit()
            except db.IntegrityError:
                error = f"user with {email} is already registered"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/signup.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        error = None
        db = get_db()
        user = db.execute(
            "SELECT userId, name, email, password FROM users WHERE email = (?)",
            (email,),
        ).fetchone()

        if user is None:
            error = "Incorrect user email"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"
        if error is None:
            session.clear()
            session["userId"] = user["userId"]
            return redirect(url_for("videos.index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("videos.index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_client():
    # bp.before_app_request registers a function that is called before every
    # viewfunction no matter the URL is
    user_id = session.get("userId")
    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute(
                "select userId, name, email from users where userId == ?",
                (user_id,),
            )
        ).fetchone()


#
# @bp.before_request
# def load_logged_in_client():
#     # bp.before_app_request registers a function that is called before every
#     # viewfunction no matter the URL is
#     user_id = session.get("userId")

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = (
#             get_db().execute(
#                 "SELECT userId, name, email FROM users WHERE userId = ?",
#                 (user_id,),
#             )
#         ).fetchone()
