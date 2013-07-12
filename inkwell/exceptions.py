# -*- coding: utf-8 -*-
from werkzeug import exceptions
from werkzeug.debug import tbtools
from flask import json, current_app
import inspect

class JSONHTTPException(exceptions.HTTPException):
    """ Implements `exceptions.HTTPException` and adds support for JSON output
    as a Flask request.
    """
    def get_body(self, environ):
        if self.code == 500:
            traceback = tbtools.get_current_traceback()
            current_app.logger.error(traceback.plaintext)

        return json.dumps({
            'code': self.code,
            'name': self.name,
            'description': self.description
        })

    def get_headers(self, environ):
        return [('Content-Type', 'application/json')]

""" Using Werkzeug's built-in list of HTTP exceptions, dynamically create a
new set of exceptions, implementing JSONHTTPException.
"""
base_http_exceptions = [m for m in inspect.getmembers(exceptions)\
    if inspect.isclass(m[1]) and issubclass(m[1], exceptions.HTTPException)]

__all__ = []
for exception in base_http_exceptions:
    json_http_exception = type(exception[0], (JSONHTTPException,\
        exception[1]), {})
    locals()[exception[0]] = json_http_exception
    __all__.append(exception[0])