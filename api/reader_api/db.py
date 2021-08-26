import os
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.environ["DATABASE_URL"])
Session = sessionmaker(bind=engine)


def connect_to_db(f):
    @wraps(f)
    def inner(*args, **kwargs):
        db_session = Session()
        try:
            rv = f(*args, db_session, **kwargs)
            db_session.commit()
        except Exception as e:
            print(f"Exception has occured: {e}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

        return rv

    return inner
