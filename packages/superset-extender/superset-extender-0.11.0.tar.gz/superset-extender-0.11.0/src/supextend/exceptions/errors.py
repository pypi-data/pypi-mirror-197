# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from supextend.loggers.config import LoggingConfig
from supextend.config import Config


class SupextendException(Exception):
    """Top class for exceptions

    Attributes:
    -----------
    msg: str
        The debug message for the Error raised
    extra: str|None
        Additional information about the exception.
        For example the traceback or embedded exception message

    """

    def __init__(self, msg, extra=None):
        self.msg = msg
        self.extra = extra
        super().__init__(self.msg)
        LoggingConfig.logger.critical(self.msg)

    def __str__(self):
        if self.extra:
            return f"{self.msg} | {self.extra}"
        return f"{self.msg}"


class UnexpectatedDbError(SupextendException):
    """Raised if the exception case is not specific enough.

    """

    def __init__(self, extra=None):
        super().__init__(
                "The database returned an unexpected error.",
                extra
                )


class HostNotFoundError(SupextendException):
    """Raised if the superset host is missing or unspecified.

    """

    def __init__(self, extra=None):
        super().__init__(
                "The host might be down, and can't be reached.",
                extra
                )


class CommandError(SupextendException):
    """Raised if a supextend command raised any unhandled exception.

    """

    def __init__(self, extra=None):
        super().__init__(
                "The command encountered an error while running.",
                extra
                )


class GeneralError(SupextendException):
    """Raised if any generale and unforeseen exception is raised during
    Runtime.

    """

    def __init__(self, extra=None):
        super().__init__(
                "The SupExtender encountered an unexpected error.",
                extra
                )


class SchemaDoesNotExistError(SupextendException):
    """Raised if a schema is none existent in the metastore

    """

    def __init__(self, extra=None):
        super().__init__(
                f"The schema `{Config.schema_name}` does not exist in the "
                f"database.",
                extra
                )


class UnexpectedSupersetError(SupextendException):
    """Raised if the superset host returned any unexpected errors.

    """

    def __init__(self, extra=None):
        super().__init__(
                "Superset API return an unexpected error.",
                extra
                )


class SupersetPayloadFormatError(SupextendException):
    """Raised if the payload for the superset API request is incorrectly
    formatted.

    """

    def __init__(self, extra=None):
        super().__init__(
                "The submitted payload has the incorrect format.",
                extra
                )


class SupersetConnectionError(SupextendException):
    """Raised if the application is unable to reach a superset API enpoint.

    """

    def __init__(self, extra=None):
        super().__init__(
                "The connection to superset failed.",
                extra
                )


class SupersetPayloadSchemaError(SupextendException):
    """Raised if the payload for the superset API request has an
     incorrect schema.

    """

    def __init__(self, extra=None):
        super().__init__(
                "The submitted payload has an incorrect schema.",
                extra
                )


class SecretKeyMissingError(SupextendException):
    """Raised if the secret key configs are missing.

    """

    def __init__(self, extra=None):
        super().__init__(
                "There is a missing `SECRET_KEY` environment variable.",
                extra
                )


class DbURIMissingError(SupextendException):
    """Raised if the connection string to the metastore is missing from the
    environment variables.

    """

    def __init__(self, extra=None):
        super().__init__(
                "There is a missing `SQLALCHEMY_DATABASE_URI` environment "
                "variable.",
                extra
                )


class DbConnectionFailedError(SupextendException):
    """Raised if the connection to the metastore was unsuccessful.

    """

    def __init__(self, extra=None):
        super().__init__(
                "The connection to the database failed",
                extra
                )


class SupersetURLMissingError(SupextendException):
    """Raised if the url to superset is missing from the environment variables.

    """

    def __init__(self, extra=None):
        super().__init__(
                "There is a missing `SUPERSET_BASE_URL` environment variable.",
                extra
                )


class SupersetCredMissingError(SupextendException):
    """Raised if the url to superset is missing from the environment variables.

    """

    def __init__(self, extra=None):
        super().__init__(
                "There is a missing `SUPERSET_ADMIN_PASSWORD` or "
                "`SUPERSET_USERNAME` environment variable.",
                extra
                )


class TableDoesNotExistError(SupextendException):
    """Raised if there is a query to access a none existent table from
    the metastore.

    """

    def __init__(self, extra=None):
        super().__init__(
                "The table was deleted or renamed in the database.",
                extra
                )
