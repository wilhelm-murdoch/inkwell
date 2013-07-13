# -*- coding: utf-8 -*-
from ..utils import ApiEndpoint
from ..exceptions import NotFound, InternalServerError

class Article(ApiEndpoint):
    def get(self, year, month, day, title):
        try:
            article = self.reader.fetch_article(
                  year=year
                , month=month
                , day=day
                , title=title
            )
        except Exception as e:
            raise InternalServerError, e.message

        if not article:
            raise NotFound

        return article