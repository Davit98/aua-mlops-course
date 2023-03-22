import logging

from api.config import Config
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from .models import Base

_logger = logging.getLogger(__name__)


def create_db_engine_from_config(*, config: Config) -> Engine:
    """The Engine is the starting point for any SQLAlchemy application.

    It’s “home base” for the actual database and its DBAPI, delivered to the SQLAlchemy
    application through a connection pool and a Dialect, which describes how to talk to
    a specific kind of database / DBAPI combination.
    """
    db_uri = config.SQLALCHEMY_DATABASE_URI
    if not database_exists(db_uri):
        create_database(db_uri)
    engine = create_engine(db_uri)

    _logger.info(f"creating DB conn with URI: {db_uri}")
    return engine


def create_db_session(*, engine: Engine) -> scoped_session:
    """Broadly speaking, the Session establishes all conversations with the database.

     It represents a “holding zone” for all the objects which you’ve loaded or
     associated with it during its lifespan.
     """
    return scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine,),
    )


def init_database(app: Flask, config: Config, db_session=None) -> None:
    """Connect to the database and attach DB session to the app."""

    if not db_session:
        engine = create_db_engine_from_config(config=config)
        db_session = create_db_session(engine=engine)

        Base.metadata.create_all(bind=engine, checkfirst=True)

    app.db_session = db_session  # attaching to Flask object's instance

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
