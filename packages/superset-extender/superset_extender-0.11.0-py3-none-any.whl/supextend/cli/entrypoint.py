# -*- coding: utf-8 -*-
"""
This module registers a management script for the flask app
it is registred in the setup.cfg and changes the entrypoint from
'flask' to 'supextend'

Flask Documentation:
   https://flask.palletsprojects.com/en/2.2.x/

"""
import click
from flask.cli import FlaskGroup
from supextend.app import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the superset-extender application."""
