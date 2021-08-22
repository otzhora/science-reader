import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from models import Base, Section


engine = create_engine(os.environ['DATABASE_URL'])
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()


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


for section in initialSections:
    # sectionObject = Section(name=section["name"], moderated=section["moderated"], premium=section["premium"])
    oSection = Section(**section)
    session.add(oSection)

session.commit()

for subsection in subsections:
    try:
        parent = session.query(Section).filter(Section.name.like(subsection["parent"])).one()
        child = session.query(Section).filter(Section.name.like(subsection["child"])).one()

        parent.subsections.append(child)
    except (MultipleResultsFound, NoResultFound) as e:
        print(e)
        print("Erorr: database initiated incorrectly. Clear it and start again")
        exit()

session.commit()
