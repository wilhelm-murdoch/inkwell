# -*- coding: utf-8 -*-
from ..utils import ApiEndpoint
from ..exceptions import InternalServerError

class Archive(ApiEndpoint):
    def get(self, year=None, month=None, day=None):
        try:
            articles = self.app.reader.list(
                  by_year=year
                , by_month=month
                , by_day=day
            )
        except Exception as e:
            raise InternalServerError, e.message

        return articles