import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Sale

logger = logging.getLogger(__name__)
logfile = "coffee_shop_log.log"

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


@contextmanager
def db_session(db_url):
    """
    Creates a context with an open SQLAlchemy session.
    """
    engine = create_engine(db_url, convert_unicode=True)
    connection = engine.connect()
    session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False))
    try:
        yield session
    finally:
        session.commit()
        session.expunge_all()
        session.close()
        connection.close()


class DatabaseHandler(object):
    def __init__(self, database_url):
        self.database_url = database_url

    def get_all(self, entity_type):
        with db_session(self.database_url) as db:
            all_values = db.query(entity_type.value).all()
            logger.info("Getting all {} objects from database {}".format(entity_type.name, self.database_url))
        return all_values

    def get_by_name(self, entity_type, name):
        with db_session(self.database_url) as db:
            value = db.query(entity_type.value).filter_by(name=name).first()
            logger.info("Getting {} object from database {}".format(entity_type.name, self.database_url))
        return value

    def add(self, entity):
        with db_session(self.database_url) as db:
            db.add(entity)
            logger.info("Adding {} object to database {}".format(entity.__class__.__name__, self.database_url))

    def get_sales_by_salesman(self, salesman):
        with db_session(self.database_url) as db:
            values = db.query(Sale).filter_by(name_salesman=salesman.name).all()
            logger.info("Getting all Sales from database {} which was done by salesman {} ".format(self.database_url,
                                                                                                   salesman.name))
        return values
