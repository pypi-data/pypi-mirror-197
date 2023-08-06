# -*- coding: utf-8 -*-
"""

This sub-package provides the basic modules to interact with resources (
Database, Superset Api) in the app. The first module
connection.py defines managers for the connections to both superset and the
internal metastore.
The second module resource.py is used to define the design separation
between external and internal resources which are defined follows:
1. Internal resource: everything from the metastore (Database)
2. External resource: everything out of the metastore. For example,
the Superset RestAPI.

"""
from .resource import ExternResource, InternResource
from .connection import SupersetConnManager, MetastoreConnManager

__all__ = [
        'ExternResource',
        'InternResource',
        'SupersetConnManager',
        'MetastoreConnManager'
        ]
