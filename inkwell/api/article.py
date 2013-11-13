# -*- coding: utf-8 -*-
from inkwell import utils, exceptions

class Article(utils.ApiEndpoint):
    def get(self, year, month, day, title):
        try:
            article = self.reader.fetch_article(
                  year=year
                , month=month
                , day=day
                , title=title
            )
        except ValueError:
            raise exceptions.NotFound
        except Exception as e:
            raise exceptions.InternalServerError, e.message

        if not article:
            raise exceptions.NotFound

        return article