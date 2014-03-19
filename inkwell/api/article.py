# -*- coding: utf-8 -*-
from inkwell import utils, exceptions
from validator import field, rules, collection

class Article(utils.ApiEndpoint):
    def get(self, year, month, day, title):
        check = collection.Collection().append([
              field.Field('year',  year).append(rules.Regex(utils.REGEX_YEAR,   error='{} is not a valid year'))
            , field.Field('month', month).append(rules.Regex(utils.REGEX_MONTH, error='{} is not a valid month'))
            , field.Field('day',   day).append(rules.Regex(utils.REGEX_DAY,     error='{} is not a valid day'))
        ])

        if not check.run():
            raise exceptions.BadRequest(check.errors())

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
            raise exceptions.InternalServerError(e.message)

        if not article:
            raise exceptions.NotFound

        return article