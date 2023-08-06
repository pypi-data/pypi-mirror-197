# -*- coding: utf-8 -*-
"""
This module holds the modules that deal with storing all workspace related data
in the metastore.

Attributes
----------
workspace_owner: Table
    An intermediate class module representing the table in the chart-owner
    many-to-many relationship.

Flask Documentation:
   https://flask.palletsprojects.com/en/2.2.x/

"""
from datetime import datetime
from supextend.initialization import db, db_schema

workspace_owner = db.Table('workspace_owner',
                           db.Column(
                                   'workspace_id',
                                   db.Integer,
                                   db.ForeignKey(f'{db_schema}.workspace.id')),
                           db.Column(
                                   'owner_id',
                                   db.Integer,
                                   db.ForeignKey(f'{db_schema}.owner.id')),
                           schema=db_schema
                           )


class Workspace(db.Model):
    __tablename__ = 'workspace'

    __table_args__ = (
        {'schema': db_schema}
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(260), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    created_by = db.Column(db.String(260), nullable=False)
    description = db.Column(db.String(260), nullable=False)
    created_on = db.Column(
            db.DateTime,
            nullable=False,
            default=datetime.utcnow)
    charts = db.relationship(
            'Chart',
            cascade="all,delete",
            backref='workspace',
            lazy=True)
    dashboards = db.relationship(
            'Dashboard',
            cascade="all,delete",
            backref='workspace',
            lazy=True)
    owners = db.relationship(
            'Owner',
            secondary=workspace_owner,
            backref='workspaces')

    def __repr__(self):
        return f"Workspace - Title[{self.title}] - " \
               f"Desc[{self.description}] - Owners[{self.owners}]"
