import logging
import os
import pathlib
import sys

import api

# logging format
FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —" "%(funcName)s:%(lineno)d — %(message)s"
)

# Project Directories
ROOT = pathlib.Path(api.__file__).resolve().parent.parent


class Config:
    DEBUG = False
    TESTING = False
    ENV = os.getenv("FLASK_ENV", "production")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 5000))
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)

    # DB config matches docker container
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "example")
    DB_PORT = os.getenv("DB_PORT", 7619)
    DB_HOST = os.getenv("DB_HOST", "0.0.0.0")
    DB_NAME = os.getenv("DB_NAME", "ml_api_dev")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:"  # dialect = postgresql, driver = psycopg2
        f"{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )  # more on the URI here: https://docs.sqlalchemy.org/en/20/core/engines.html


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"  # do not use in production!
    LOGGING_LEVEL = logging.DEBUG


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = logging.DEBUG

    DB_USER = os.getenv("DB_USER", "test_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "example")
    DB_PORT = os.getenv("DB_PORT", 7618)
    DB_HOST = os.getenv("DB_HOST", "0.0.0.0")
    DB_NAME = os.getenv("DB_NAME", "ml_api_test")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:"
        f"{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class ProductionConfig(Config):
    pass


def get_console_handler():
    """Setup console logging handler."""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def setup_app_logging(config: Config) -> None:
    """Prepare custom logging for our application."""
    _disable_irrelevant_loggers()
    root = logging.getLogger()
    root.setLevel(config.LOGGING_LEVEL)
    root.addHandler(get_console_handler())
    root.propagate = False


def _disable_irrelevant_loggers() -> None:
    """Disable loggers created by packages which create a lot of noise."""
    for logger_name in (
        "connexion.apis.flask_api",
        "connexion.apis.abstract",
        "connexion.decorators",
        "connexion.operation",
        "connexion.operations",
        "connexion.app",
        "openapi_spec_validator",
    ):
        logging.getLogger(logger_name).level = logging.WARNING
