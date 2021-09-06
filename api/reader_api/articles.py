from flask import Blueprint, g, request
from flask.json import jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from reader_api.db import connect_to_db
from reader_api.auth import login_required
from reader_api.models import Article


bp = Blueprint("articles", __name__, url_prefix="/articles")


@bp.route("/", methods=["GET", "POST"])
def get_articles():
    if request.method == "GET":
        return get_all_articles()
    return add_new_article()


@connect_to_db
def get_all_articles(db_session):
    try:
        articles = db_session.query(Article).all()
    except SQLAlchemyError as e:
        print(f"Error has occured: {e}")
        return e, 500
    return jsonify([article.serialize for article in articles])


@connect_to_db
def add_new_article(db_session):
    article_data = get_article_data()
    try:
        db_session.add(Article(**article_data))
    except SQLAlchemyError as e:
        print(f"Error has occured: {e}")
        return e, 500
    return "Successful", 200


@login_required
def get_article_data():
    return {
        "author_id": g.user["id"],
        "content": request.form["content"],
        "section_id": int(request.form["section_id"])
    }


@bp.route("/<int:article_id>")
@connect_to_db
def get_article_by_id(article_id, db_session):
    try:
        article = db_session.query(Article).filter(Article.id == article_id).one()
    except NoResultFound:
        return f"Article with {article_id} does not exist", 400
    except SQLAlchemyError as e:
        print(f"Error has occured: {e}")
        return e, 500
    return jsonify(article.serialize)
