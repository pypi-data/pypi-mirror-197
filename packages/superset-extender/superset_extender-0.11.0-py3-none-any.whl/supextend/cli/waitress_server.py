# -*- coding: utf-8 -*-
"""
This module runs a production server for the application using 'Waitress'
at port=5000 and host=0.0.0.0 with threads=12

Flask Documentation:
   https://flask.palletsprojects.com/en/2.2.x/

"""
from waitress import serve

from supextend.app import create_app

if __name__ == "__main__":
    serve(create_app(), host='0.0.0.0', port=5000, threads=12)
