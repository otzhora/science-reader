from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from reader_api.config import Config
from reader_api.validation import handle_db_exception


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)


def connect_to_db(f):
    @wraps(f)
    @handle_db_exception
    def inner(*args, **kwargs):
        db_session = Session()
        try:
            rv = f(*args, db_session=db_session, **kwargs)
            db_session.commit()
        except Exception as e:
            print(f"Exception has occured: {e}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

        return rv

    return inner
