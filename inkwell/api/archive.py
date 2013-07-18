# -*- coding: utf-8 -*-
from ..utils import ApiEndpoint
from ..exceptions import InternalServerError, NotFound
from datetime import datetime

class Archive(ApiEndpoint):
    def get(self, year=None, month=None, day=None):
        limit  = self.request.args.get('limit',  0, type=int)
        offset = self.request.args.get('offset', 0, type=int)

        try:
            articles = self.reader.list(
                  by_year=year
                , by_month=month
                , by_day=day
                , limit=limit
                , offset=offset
            )
        except ValueError:
            raise NotFound
        except Exception as e:
            raise InternalServerError, e.message

        return articles