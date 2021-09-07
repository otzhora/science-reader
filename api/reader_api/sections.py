from flask import Blueprint, jsonify
from sqlalchemy.orm.exc import NoResultFound

from reader_api.models import Section
from reader_api.db import connect_to_db


bp = Blueprint("sections", __name__, url_prefix="/sections")


@bp.route("/", methods=["GET"])
@connect_to_db
def index(db_session):
    sections = db_session.query(Section).filter(Section.parent_section_id.is_(None))
    return jsonify([section.serialize for section in sections])


@bp.route("/<int:section_id>", methods=["GET"])
@connect_to_db
def get_section_info(section_id, db_session):
    try:
        section = db_session.query(Section).filter(Section.id == section_id).one()
    except NoResultFound:
        return f"Sections with id: {section_id} does not exist", 400
    return jsonify(section.serialize)
