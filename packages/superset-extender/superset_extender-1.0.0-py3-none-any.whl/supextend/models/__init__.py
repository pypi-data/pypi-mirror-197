# -*- coding: utf-8 -*-
"""

This sub-package is a design construct that presents an entrypoint to import
all the modules (representation of database tables as classes).

"""
from supextend.models.airflow_task_instances import AirflowTaskInstance
from supextend.models.charts import Chart
from supextend.models.dashboards import Dashboard
from supextend.models.tags import Tag
from supextend.models.workspaces import Workspace
from supextend.models.owners import Owner

__all__ = [
        'AirflowTaskInstance',
        'Chart',
        'Dashboard',
        'Tag',
        'Workspace',
        'Owner'
        ]
