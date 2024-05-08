from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from database_connect import engine
import logging


class DatabaseManager:
    def __init__(self, db_uri):
        
        self.engine = engine

     
        session_factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(session_factory)

        logging.info("DatabaseManager initialized")

    def begin_transaction(self):
        
        self.session.begin()
        logging.info("Transaction begun")

    def commit_transaction(self):
        
        self.session.commit()
        logging.info("Transaction committed")

    def rollback_transaction(self):
        self.session.rollback()
        logging.info("Transaction rolled back")

    def execute_query(self, query, params=None):
        
        result = self.session.execute(text(query), params)
        return result.fetchall()

    def execute_non_query(self, query, params=None):
       
        self.session.execute(text(query), params)
        logging.info(f"Executed query: {query}")

    def close(self):
        
        self.session.remove()
        logging.info("Session closed")

    def set_isolation_level(self, isolation_level):
       
        self.session.get_bind().execution_options(isolation_level=isolation_level)
        logging.info(f"Isolation level set to {isolation_level}")
