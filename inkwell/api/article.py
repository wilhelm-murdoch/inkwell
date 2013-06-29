# -*- coding: utf-8 -*-
from ..utils import ApiEndpoint
from ..reader import Reader
from ..exceptions import NotFound, InternalServerError

class Article(ApiEndpoint):
    def get(self, year, month, day, title):
        reader = Reader(articles_folder=self.config.get('ARTICLES_FOLDER'))
        try:
            article = reader.fetch_article(year=year, month=month, day=day, \
                title=title)
        except Exception as e:
            raise InternalServerError, e.message

        if not article:
            raise NotFound

        return article