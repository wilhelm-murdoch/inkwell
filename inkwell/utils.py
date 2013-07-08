# -*- coding: utf-8 -*-
from flask import request, current_app, json, make_response
from flask.views import MethodView
from reader import Article, ArticleCollection
from datetime import date, datetime

def json_presenter(f):
    """ A method view decorator used to transform view response bodies into
    JSON-based Flask response objects with appropriate headers.
    """
    def decorator(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            raise

        response = make_response(json.dumps(result, cls=Encoder))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'

        return response
    return decorator

class Encoder(json.JSONEncoder):
    """ Custom JSON encoder used to parse dicts which may contain instances of
    `inkwell.reader.Article` or `inkwell.reader.ArticleCollection`.

    Usage::

        response = {
            articles: [
                  Article(filename='2012-02-01-foo.txt', body='foo')
                , Article(filename='2012-02-01-bar.txt', body='bar')
                , Article(filename='2012-02-01-baz.txt', body='baz')
            ]
        }

        parsed = json.dumps(response, cls=Encoder)
    """
    def default(self, obj):
        if isinstance(obj, Article):
            return obj.to_json()
        if isinstance(obj, ArticleCollection):
            return obj.to_json()
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat() + 'Z'
        elif hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


# http://flask.pocoo.org/snippets/45/
def request_wants_json():
    """ Attempts a best-guess, using request headers, at whether the current
    request has been properly configured to recieve JSON.

    Returns::
        Boolean True|False depending on best guess
    """
    best = request.accept_mimetypes.best_match(['application/json', \
        'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


class ApiEndpoint(MethodView):
    """ Base abstract class which implements `flask.view.MethodView` and
    provides Inkwell's endpoints with some convenience methods and decorators.
    """

    decorators = [json_presenter]

    @property
    def config(self):
        """ Returns the current app instance's loaded configuration. """
        return current_app.config

    @property
    def request(self):
        """ Returns the current request. """
        return request

    @property
    def app(self):
        """ Returns the current instance of the Inkwell server. """
        return current_app

    @property
    def logger(self):
        """ Returns Inkwell's logger. """
        return current_app.logger