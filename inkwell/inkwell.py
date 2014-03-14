# -*- coding: utf-8 -*-
from flask import Blueprint, Flask, render_template, current_app
from api import archive, article
from . import utils, exceptions

rules = [
      ('/', archive.Archive, 'api_archive')
    , ('/<year>', archive.Archive, 'api_archive_year')
    , ('/<year>/<month>', archive.Archive, 'api_archive_year_month')
    , ('/<year>/<month>/<day>', archive.Archive, 'api_archive_year_month_day')
    , ('/<year>/<month>/<day>/<title>', article.Article, 'api_article')
]

api = Blueprint('inkwell_api', __name__, url_prefix='/inkwell')

for rule in rules:
    api.add_url_rule(rule[0], view_func=rule[1].as_view(rule[2]),
        methods=['GET'])

@api.before_request
def before_request():
    """ Decorator applied to all incoming requests determines whether the
    request contains a valid `Accept` header with the value of
    `application/json`. Raises `BadRequest` if evaluated to False.

    Returns::
        inkwell.exceptions.BadRequest
    """
    if not utils.request_wants_json():
        raise exceptions.BadRequest

@api.errorhandler(404)
@api.errorhandler(Exception)
def errorhandler(error):
    """ An Inkwell-specific error handler that handles 404 and 500 server
    errors. All Inkwell internal exceptions are derived from
    `inkwell.exceptions.JSONHTTPException`, which returns a JSON body that
    Flask can recognize and use as a response.

    Arguments::
        error `object` Exception derived from JSONHTTPException.

    Returns::
        Flask response
    """
    if not hasattr(error, 'code'):
        error.code = 500

    try:
        if error.code == 404:
            raise exceptions.NotFound
        elif error.code == 500:
            raise exceptions.InternalServerError
    except Exception as e:
        return e, e.code

def bootstrap(configuration=None):
    """ A factory that creates an instance of the Inkwell server. This allows
    one create multiple instances running different configurations
    simultaneously.

    Arguments::
        configuration `object or None` A configuration object for the resulting
        instance of Inkwell.

    Returns::
        An instance of an Inkwell server.
    """
    app = Flask(__name__)

    app.config.from_object(configuration or 'inkwell.config.LocalConfig')
    app.register_blueprint(api)

    return app