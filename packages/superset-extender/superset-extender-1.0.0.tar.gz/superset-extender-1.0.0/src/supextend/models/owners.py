# -*- coding: utf-8 -*-
"""
This module holds the modules that deal with storing all owner related data
coming from Superset.

Flask Documentation:
   https://flask.palletsprojects.com/en/2.2.x/

"""
from flask_login import UserMixin
from supextend.initialization import db, login_manager, db_schema


@login_manager.user_loader
def load_owner(owner_id):
    return Owner.query.get(int(owner_id))


class Owner(db.Model, UserMixin):
    __tablename__ = 'owner'

    __table_args__ = (
        {'schema': db_schema}
    )

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(260), nullable=False)
    last_name = db.Column(db.String(260), nullable=False)
    username = db.Column(db.String(260), unique=True, nullable=False)
    color = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        return f"Owner - Name[{self.first_name} {self.last_name}]" \
               f" - Username[{self.username}]"
