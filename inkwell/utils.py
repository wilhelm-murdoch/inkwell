# -*- coding: utf-8 -*-
from flask import request, current_app, json, make_response
from flask.views import MethodView
from reader import Article, ArticleCollection
from datetime import date, datetime

def json_presenter(f):
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
    best = request.accept_mimetypes.best_match(['application/json', \
        'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


class ApiEndpoint(MethodView):
    decorators = [json_presenter]

    @property
    def config(self):
        return current_app.config

    @property
    def request(self):
        return request

    @property
    def app(self):
        return current_app

    @property
    def logger(self):
        return current_app.logger