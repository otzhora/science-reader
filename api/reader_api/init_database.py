import click
from sqlalchemy.exc import SQLAlchemyError

from reader_api.models import Section
from reader_api.db import connect_to_db


initialSections = [
    {
        "name": "Physics",
        "moderated": False,
        "premium": False,
    },
    {
        "name": "Math",
        "moderated": False,
        "premium": False,
    },
    {
        "name": "Algebra",
        "moderated": False,
        "premium": False,
    },
    {
        "name": "Calculus",
        "moderated": False,
        "premium": False,
    },
    {
        "name": "Computer science",
        "moderated": False,
        "premium": False,
    },
    {
        "name": "Algorithms",
        "moderated": False,
        "premium": False,
    },
    {
        "name": "P == NP?",
        "moderated": False,
        "premium": False,
    },
    {
        "name": "Data science",
        "moderated": False,
        "premium": False,
    },
]

subsections = [
    {
        "parent": "Computer science",
        "child": "Algorithms"
    },
    {
        "parent": "Algorithms",
        "child": "P == NP?"
    },
    {
        "parent": "Math",
        "child": "Algebra"
    },
    {
        "parent": "Math",
        "child": "Calculus"
    },
]


@click.command('init-db')
@connect_to_db
def init_db(db_session):
    click.echo("Initializing db")
    oSections = {section["name"]: Section(**section)
                 for section in initialSections}

    for oSection in oSections.values():
        db_session.add(oSection)
    db_session.flush()

    for subsection in subsections:
        try:
            child = oSections[subsection["child"]]
            parent = oSections[subsection["parent"]]
            db_session.refresh(child)
            db_session.refresh(parent)
            parent.subsections.append(child)
        except SQLAlchemyError:
            click.echo("Erorr: database initiated incorrectly. Clear it and start again")
            exit()
