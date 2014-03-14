# -*- coding: utf-8 -*-
from werkzeug import exceptions
from flask import json

__all__ = [
    'JSONHTTPException', 
    'BadRequest', 
    'NotFound', 
    'InternalServerError'
]

class JSONHTTPException(exceptions.HTTPException):   
    """ Implements `exceptions.HTTPException` and adds support for JSON output
    as a Flask request.
    """
    def get_body(self):
        return json.dumps({
            'code': self.code,
            'name': self.name,
            'description': self.description
        })

    def get_headers(self):
        return [('Content-Type', 'application/json')]


class BadRequest(JSONHTTPException):
    code = 400
    description = (
        'The browser (or proxy) sent a request that this server could '
        'not understand.'
    )


class NotFound(JSONHTTPException):
    code = 404
    description = (
        'The requested URL was not found on the server.  '
        'If you entered the URL manually please check your spelling and '
        'try again.'
    )


class InternalServerError(JSONHTTPException):
    code = 500
    description = (
        'The server encountered an internal error and was unable to '
        'complete your request.  Either the server is overloaded or there '
        'is an error in the application.'
    )