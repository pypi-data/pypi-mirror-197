# -*- coding: utf-8 -*-
"""
This module draws a clear separation in terms of design and make basic
abstract classes from which you can inherit to define either an external or
internal resource.

"""
from abc import ABC


class APPClient(ABC):
    """Top class to represent the application"""

    pass


class ExternResource(APPClient, ABC):
    """External Resources are defined as everything
    not originating from the superset extension metastore"""

    pass


class InternResource(APPClient, ABC):
    """Internal Resources are defined as everything
    originating from the superset extension metastore"""

    pass
