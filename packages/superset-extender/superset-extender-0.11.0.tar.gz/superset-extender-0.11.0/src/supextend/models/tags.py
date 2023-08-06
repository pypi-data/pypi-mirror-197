# -*- coding: utf-8 -*-
"""
This module holds the modules that deal with storing all tag related data
coming from Superset.

Flask Documentation:
   https://flask.palletsprojects.com/en/2.2.x/

"""
from supextend.initialization import db, db_schema


class Tag(db.Model):
    __tablename__ = 'tag'

    __table_args__ = (
            {'schema': db_schema}
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(260), nullable=False)
    color = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Tag - Title[{self.title}] - Color[{self.color}]"
