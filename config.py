"""
Configuration file
"""

DATA_BASE_PATH = ""

""" FLASK CONFIG """
FLASK_PORT = "5000"
FLASK_HOST_ADDRESS = "0.0.0.0"
ENV = 'development'
TESTING = True
DEBUG = True
SECRET_KEY = 'XB#"L))I`m(?>X#\ts.[wr#v\''

""" GUNICORN CONFIG """
bind = "0.0.0.0:5000"
workers=2
limit_request_line=0