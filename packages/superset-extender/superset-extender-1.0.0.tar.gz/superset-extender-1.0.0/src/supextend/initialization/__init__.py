# -*- coding: utf-8 -*-
"""

This sub-package instantiates basic flask utilities :

Attributes
----------
bcrypt : Bcrypt
    Flask-Bcrypt is a Flask extension that provides bcrypt
    hashing utilities for your application.
    reference: https://pypi.org/project/Flask-Bcrypt/

db: SQLAlchemy
    Flask-SQLAlchemy is an extension for Flask that adds support
    for SQLAlchemy to your application.
    It aims to simplify using SQLAlchemy with
    Flask by providing useful defaults and extra helpers that make it easier to
    accomplish common tasks.
    reference: https://pypi.org/project/Flask-SQLAlchemy/

migrate : Migrate
    Flask-Migrate is an extension that configures Alembic in the
    proper way to work with your Flask and Flask-SQLAlchemy application.
    In terms of the actual database migrations, everything
    is handled by Alembic, so you get exactly the same functionality.
    reference: https://flask-migrate.readthedocs.io/en/latest/

db_schema  : str
    Module level variable that holds the name of
    the schema for the metastore in the project.

oidc : OpenIDConnect
    Flask-OIDC is an extension to Flask that allows you to
    add OpenID Connect based authentication to your website in a matter of
    minutes. It depends on Flask and oauth2client. You can install the
    requirements from PyPI with easy_install or pip or download them by hand.
    reference: https://flask-oidc.readthedocs.io/en/latest/

login_manager : LoginManager
    The most important part of an application that
    uses Flask-Login is the LoginManager class. You should create one for your
    application somewhere in your code, like this.
    reference: https://flask-login.readthedocs.io/en/latest/


Flask Documentation:
   https://flask.palletsprojects.com/en/2.2.x/

"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_oidc import OpenIDConnect
from flask_migrate import Migrate
from supextend.config import Config
from supextend.utils.database import schema_exists
from supextend.exceptions import (
    SecretKeyMissingError,
    DbURIMissingError,
    SupersetURLMissingError,
    SchemaDoesNotExistError,
    SupersetCredMissingError
    )

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
db_schema = Config.schema_name
oidc = OpenIDConnect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# environment variables
if not Config.secret_key:
    raise SecretKeyMissingError

if not Config.database_url:
    raise DbURIMissingError

if not Config.superset_base_url:
    raise SupersetURLMissingError

if not Config.superset_password or not Config.superset_username:
    raise SupersetCredMissingError

# schema
if not schema_exists():
    raise SchemaDoesNotExistError
