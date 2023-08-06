# -*- coding: utf-8 -*-
"""
This module holds the modules that deal with storing all chart related data
coming from Superset.

Attributes
----------
chart_tag : Table
    An intermediate class module representing the table in the chart-tag
    many-to-many
    relationship.

chart_owner: Table
    An intermediate class module representing the table in the chart-owner
    many-to-many relationship.

Flask Documentation:
   https://flask.palletsprojects.com/en/2.2.x/

"""
from urllib.parse import urljoin
import json
from supextend.initialization import db, db_schema
from supextend.config import Config

chart_tag = db.Table('chart_tag',
                     db.Column(
                             'chart_id',
                             db.Integer,
                             db.ForeignKey(f'{db_schema}.chart.id')),
                     db.Column(
                             'tag_id',
                             db.Integer,
                             db.ForeignKey(f'{db_schema}.tag.id')),
                     schema=db_schema
                     )

chart_owner = db.Table('chart_owner',
                       db.Column(
                               'chart_id',
                               db.Integer,
                               db.ForeignKey(f'{db_schema}.chart.id')),
                       db.Column(
                               'owner_id',
                               db.Integer,
                               db.ForeignKey(f'{db_schema}.owner.id')),
                       schema=db_schema
                       )


class Chart(db.Model):
    __tablename__ = 'chart'

    __table_args__ = (
        {'schema': db_schema}
    )

    id = db.Column(db.Integer, primary_key=True)
    descriptive_id = db.Column(db.String(4), nullable=False)
    superset_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(260), nullable=False)
    type = db.Column(db.String(260), nullable=False)
    created_by = db.Column(db.String(260), nullable=False)
    datasource = db.Column(db.String(260), nullable=False)
    datasource_type = db.Column(db.String(260), nullable=False)
    last_modified_on = db.Column(db.DateTime, nullable=False)
    last_saved_by = db.Column(db.String(260), nullable=False)
    status = db.Column(db.String(60), nullable=False)
    delete_on = db.Column(db.DateTime, nullable=True)
    img = db.Column(db.Text, nullable=True)
    extra = db.Column(db.Text, nullable=True)
    task_id = db.Column(
            db.Integer,
            db.ForeignKey(f'{db_schema}.airflow_task_instance.id'))
    workspace_id = db.Column(
            db.Integer,
            db.ForeignKey(f'{db_schema}.workspace.id'), nullable=False)
    tags = db.relationship('Tag', secondary=chart_tag, backref='charts')
    owners = db.relationship('Owner', secondary=chart_owner, backref='charts')

    def __repr__(self):
        return f"Chart - Title[{self.title}] - ID[{self.descriptive_id}] " \
               f"- Tags[{self.tags}] - Owners[{self.owners}]"

    def airflow_url(self):
        url = urljoin(
            Config.airflow_base_url,
            f"/taskinstance/list/?flt1_dag_id_equals={self.task.dag_name}"
            f"&_flt_3_task_id={self.task.task_name}") if self.task else "#"
        return url

    def superset_url(self):
        return urljoin(Config.superset_base_url, json.loads(self.extra)["url"])
