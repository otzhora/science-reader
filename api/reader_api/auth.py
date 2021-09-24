from functools import wraps
from flask import Blueprint, session, request, g
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm.exc import NoResultFound

from reader_api.db import connect_to_db
from reader_api.models import User


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
@connect_to_db
def register(db_session):
    username = request.form['username']
    password = request.form['password']

    if not username:
        return 'Username is required', 400
    if not password:
        return 'Password is required', 400

    if username_exist(db_session, username):
        return f"Username {username} is taken", 400

    db_session.add(User(username=username,
                        password=generate_password_hash(password)))
    return "Registration is successfuly"


def username_exist(db_session, username):
    return db_session.\
        query(User.username).\
        filter(User.username == username).exists()


@bp.route("/login", methods=["POST"])
@connect_to_db
def login(db_session):
    username = request.form['username']
    password = request.form['password']

    try:
        user = db_session.query(User).filter(User.username == username).one()
    except NoResultFound:
        return f"User with username {username} is not registered", 400

    if not check_password_hash(user.password, password):
        return "Invalid password", 400

    session.clear()
    session["user_id"] = user.id

    return f"Logged in successfuly with username: {user.username}", 200


@bp.before_app_request
@connect_to_db
def load_user(db_session):
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        try:
            g.user = db_session.query(User) \
                .filter(User.id == user_id) \
                .one().serialize
        except NoResultFound:
            return f"User with id {id} wasn't found in database", 500


@bp.route("logout")
def logout():
    session.clear()
    return "Logged out successfuly"


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if g.user is None:
            return "You are not logged in", 400
        return f(*args, **kwargs)
    return inner
