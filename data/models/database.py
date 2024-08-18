import psycopg2
from psycopg2 import pool
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import DATABASE_URL

Base = declarative_base()


class DatabaseConnection:
    _instance = None

    def __new__(cls, ):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.engine = create_engine(DATABASE_URL)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            Base.metadata.create_all(bind=self.engine)
            self._initialized = True

    def get_session(self):
        return self.SessionLocal()
