import base64
import os
import sqlalchemy
import urllib

def sql_connect():
    raise NotImplementedError("Must be implemented by end-user")
    # return engine, staging_schema, app_schema
