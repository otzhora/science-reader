from functools import wraps

from sqlalchemy.exc import SQLAlchemyError


def handle_db_exception(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            rv = f(*args, **kwargs)
        except SQLAlchemyError as e:
            return e, 500
        return rv
    return inner
