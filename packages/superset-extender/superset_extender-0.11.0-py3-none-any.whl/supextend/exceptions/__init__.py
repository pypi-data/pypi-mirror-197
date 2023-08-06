# -*- coding: utf-8 -*-
"""

This sub-package provides the basic modules to that implement custom errors.

"""
from .errors import (
    UnexpectatedDbError,
    HostNotFoundError,
    CommandError,
    GeneralError,
    SchemaDoesNotExistError,
    UnexpectedSupersetError,
    SupersetPayloadFormatError,
    SupersetPayloadSchemaError,
    SecretKeyMissingError,
    DbURIMissingError,
    SupersetURLMissingError,
    TableDoesNotExistError,
    DbConnectionFailedError,
    SupersetConnectionError,
    SupersetCredMissingError
    )

__all__ = [
        "UnexpectatedDbError",
        "HostNotFoundError",
        "CommandError",
        "GeneralError",
        "SchemaDoesNotExistError",
        "UnexpectedSupersetError",
        "SupersetPayloadFormatError",
        "SupersetPayloadSchemaError",
        "SecretKeyMissingError",
        "DbURIMissingError",
        "SupersetURLMissingError",
        "TableDoesNotExistError",
        "DbConnectionFailedError",
        "SupersetConnectionError",
        "SupersetCredMissingError"
        ]
