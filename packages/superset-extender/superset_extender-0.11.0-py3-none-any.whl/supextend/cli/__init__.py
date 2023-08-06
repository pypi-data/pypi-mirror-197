# -*- coding: utf-8 -*-
"""

This sub-package provides the basic modules to interact with the
internal cli wrapped around the flask cli. The first module
entrypoint.py gives an entrypoint to the package supextend command
defined in the setup.cfg.
The second module waitress_server.py is used when running publicly rather
than in development, you should not use the built-in development server
(supextend run). The development server is provided by Werkzeug for
convenience, but is not designed to be particularly
efficient, stable, or secure. Instead, use a production WSGI server. This is
why we currently use waitress

Example
-------
For example, to use Waitress, first start the virtual environment:
literal blocks::

    $ pipenv shell

To use the cli You need to tell Waitress about your application, but it doesn’t
use --app like supextend run does. You need to tell it to import and call the
application factory to get an application object.

literal blocks::

    $ waitress-serve --threads=12 --port 8080 --call "app:create_app"

    Serving on http://0.0.0.0:8080

But if you need to use the module directly run the following:

literal blocks::

    $ python superset_extender/cli/waitress_server.py


Flask Documentation:
   https://flask.palletsprojects.com/en/2.2.x/

"""
