# -*- coding: utf-8 -*-
from inkwell import utils, exceptions
from validator import field, rules, collection

class Archive(utils.ApiEndpoint):
    def get(self, year=None, month=None, day=None):
        check = collection.Collection()

        if year:
            check.append(field.Field('year', year).append(rules.Regex(utils.REGEX_YEAR, error='{} is not a valid year')))

        if month: 
            check.append(field.Field('month', month).append(rules.Regex(utils.REGEX_MONTH, error='{} is not a valid month')))

        if day:
            check.append(field.Field('day', day).append(rules.Regex(utils.REGEX_DAY, error='{} is not a valid day')))

        if not check.run():
            raise exceptions.BadRequest(check.errors())

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
            raise exceptions.NotFound
        except Exception as e:
            raise exceptions.InternalServerError(e.message)

        return articles