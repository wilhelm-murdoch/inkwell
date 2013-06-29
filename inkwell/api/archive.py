# -*- coding: utf-8 -*-
from ..utils import ApiEndpoint
from ..reader import Reader

class Archive(ApiEndpoint):
    def get(self, year=None, month=None, day=None):
        reader = Reader(articles_folder=self.config.get('ARTICLES_FOLDER'))
        articles = reader.list(by_year=year, by_month=month, by_day=day)

        return articles