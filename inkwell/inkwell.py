# -*- coding: utf-8 -*-
from werkzeug.debug import tbtools
from flask import Blueprint, Flask, render_template, current_app
from api import archive, article
from utils import request_wants_json
from exceptions import BadRequest, NotFound, InternalServerError

rules = [
      ('/', archive.Archive, 'api_archive')
    , ('/<year>', archive.Archive, 'api_archive_year')
    , ('/<year>/<month>', archive.Archive, 'api_archive_year_month')
    , ('/<year>/<month>/<day>', archive.Archive, 'api_archive_year_month_day')
    , ('/<year>/<month>/<day>/<title>', article.Article, 'api_article')
]

api = Blueprint('inkwell_api', __name__, url_prefix='/inkwell')

for rule in rules:
    api.add_url_rule(rule[0], view_func=rule[1].as_view(rule[2]), \
        methods=['GET'])

@api.before_request
def before_request(*args, **kwargs):
    if not request_wants_json():
        raise BadRequest, '`Accept: application/json` is required.'

@api.errorhandler(404)
@api.errorhandler(Exception)
def errorhandler(error):
    if not hasattr(error, 'code'):
        traceback = tbtools.get_current_traceback()
        current_app.logger.error(traceback.plaintext)
        error.code = 500

    try:
        if error.code == 404:
            raise NotFound
        elif error.code == 500:
            raise InternalServerError
    except Exception as e:
        return e, e.code

def bootstrap(configuration=None):
    app = Flask(__name__)

    app.config.from_object(configuration or 'inkwell.config.LocalConfig')
    app.register_blueprint(api)

    return app