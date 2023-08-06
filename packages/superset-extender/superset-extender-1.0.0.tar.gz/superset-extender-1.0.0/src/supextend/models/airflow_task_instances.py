# -*- coding: utf-8 -*-
"""
This module holds the modules that deal with storing data coming from Airflow

Flask Documentation:
   https://flask.palletsprojects.com/en/2.2.x/

"""
from supextend.initialization import db, db_schema


class AirflowTaskInstance(db.Model):

    __tablename__ = 'airflow_task_instance'

    __table_args__ = (
        {'schema': db_schema}
    )

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(260), nullable=False)
    dag_name = db.Column(db.String(260), nullable=False)
    run_id = db.Column(db.String(260), nullable=False)
    removed_charts = db.relationship('Chart', backref='task', lazy=True)
    removed_dashboards = db.relationship('Dashboard', backref='task', lazy=True)

    def __repr__(self):
        return f"Task - Title[{self.task_name}] - Run ID[{self.run_id}]"
