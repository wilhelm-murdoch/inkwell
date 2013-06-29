# -*- coding: utf-8 -*-
from werkzeug import exceptions
from flask import json
import inspect

class JSONHTTPException(exceptions.HTTPException):
    def get_body(self, environ):
        return json.dumps({
            'code': self.code,
            'name': self.name,
            'description': self.description
        })

    def get_headers(self, environ):
        return [('Content-Type', 'application/json')]

base_http_exceptions = [m for m in inspect.getmembers(exceptions)\
    if inspect.isclass(m[1]) and issubclass(m[1], exceptions.HTTPException)]

__all__ = []
for exception in base_http_exceptions:
    json_http_exception = type(exception[0], (JSONHTTPException,\
        exception[1]), {})
    locals()[exception[0]] = json_http_exception
    __all__.append(exception[0])