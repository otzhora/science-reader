from flask import Blueprint, g, request
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound

from reader_api.db import connect_to_db
from reader_api.auth import login_required
from reader_api.models import Comment


bp = Blueprint("comments", __name__, url_prefix="/comments")


@bp.route("/<int:article_id>", methods=["GET", "POST"])
def get_articles(article_id):
    if request.method == "GET":
        return get_all_comments(article_id)
    return add_new_comment(article_id)


@connect_to_db
def get_all_comments(article_id, db_session):
    articles = (
        db_session.query(Comment)
        .filter((Comment.article_id == article_id)
                & (Comment.response_id.is_(None)))
        .all()
    )
    return jsonify([article.serialize for article in articles])


@connect_to_db
def add_new_comment(article_id, db_session):
    comment_data = get_comment_data(article_id)
    db_session.add(Comment(**comment_data))
    return "Successful", 200


@login_required
def get_comment_data(article_id):
    return {
        "author_id": g.user["id"],
        "content": request.form["content"],
        "article_id": article_id,
        "response_id": request.form.get("response_id"),
    }


@bp.route("/<int:article_id>/<int:comment_id>")
@connect_to_db
def get_article_by_id(article_id, comment_id, db_session):
    try:
        comment = (
            db_session.query(Comment)
            .filter((Comment.article_id == article_id) & (Comment.id == comment_id))
            .one()
        )
    except NoResultFound:
        return f"Article with {article_id} does not exist", 400
    return jsonify(comment.serialize)
