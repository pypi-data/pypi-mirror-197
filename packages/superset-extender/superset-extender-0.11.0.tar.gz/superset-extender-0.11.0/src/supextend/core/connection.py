# -*- coding: utf-8 -*-
"""
This module provides basic session management from external and internal
resources.

"""
import requests
from urllib.parse import urljoin
from supextend.initialization import db
from supextend.exceptions import SupersetConnectionError


class Connection:
    """Top class to represent a connection to any
    resource (External or Internal)

    Attributes:
    -----------
    _session: None
        Internal attribute that denotes the session in use
    """

    def __init__(self, **kwargs):
        """
        Parameters:
        -----------
        kwargs: dict
            Extra connection details to establish the new session
        """

        self._session = None
        self.__dict__.update(kwargs)


class SupersetConnManager(Connection):
    """A context manager class that creates/drops
    a connection to the superset RESTApi.

    Attributes:
    -----------
    _auth_headers: dict
        The headers used in the request to the superset api.


    Methods:
    --------
    _get_access_token()
        (Weak internal use only) Retrieves the access token
        from the superset api endpoint
        `/api/v1/security/login` whilst using the credentials
        provided to the `Connection` instance of the parent class

    __set_session()
        (Weak internal use only) Retrieves the session and
        updates the _auth_headers
        with the `X-CSRFToken` token for security.
    """

    def __init__(self, base_url, username, password):
        """
        Parameters:
        -----------
        base_url: str
            The superset endpoint in a local deploy
            it is `http://localhost:8088`
        username: str
            The right credentials to access superset API,
            in a fresh deploy it is `admin`
        password: str
            The right credentials to access superset API,
            in a fresh deploy it is `admin`
        """

        super().__init__(
                _base_url=base_url,
                _username=username,
                _password=password
                )
        self._auth_headers = None

    def _get_access_token(self):
        login_endpoint = urljoin(self._base_url, '/api/v1/security/login')
        try:
            response = requests.post(
                    login_endpoint,
                    json={
                            "username": self._username,
                            "password": self._password,
                            "refresh": "true",
                            "provider": "db",
                            },
                    )
        except requests.exceptions.ConnectionError as e:
            raise SupersetConnectionError(extra=e)
        return response.json().get("access_token")

    def _set_session(self):
        auth_headers = {
                'Authorization': 'Bearer ' + self._get_access_token()
                }

        csrf_token_endpoint = urljoin(
                self._base_url,
                '/api/v1/security/csrf_token'
                )
        session = requests.Session()
        response = session.get(
                url=csrf_token_endpoint,
                headers=auth_headers,
                )
        auth_headers["X-CSRFToken"] = response.json().get("result")
        auth_headers['Content-Type'] = "application/json"
        auth_headers['Referer'] = self._base_url
        self._auth_headers = auth_headers
        self._session = session

    def __enter__(self):
        self._set_session()
        return self._auth_headers, self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
        self._session = None


class MetastoreConnManager(Connection):
    """A context manager class that creates/drops
    a connection to the superset extension app database."""

    def __enter__(self):
        self._session = db.session()
        self._session.expire_on_commit = False
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.expire_on_commit = True
        self._session = None
