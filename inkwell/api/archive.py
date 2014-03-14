# -*- coding: utf-8 -*-
from inkwell import utils, exceptions

class Archive(utils.ApiEndpoint):
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
            raise exceptions.NotFound
        except Exception as e:
            raise exceptions.InternalServerError(e.message)

        return articles