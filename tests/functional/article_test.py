# -*- coding: utf-8 -*-
import inkwell
import unittest
import json
import random
import re
from tests import fixtures
from werkzeug.test import Client

class ArticleTest(unittest.TestCase):
    def test_article_found(self):
        file = random.choice(fixtures.valid_files)
        matched = re.match(inkwell.reader.ARTICLE_FILE_PATTERN, file)

        response = fixtures.client.get("/inkwell/{}/{}/{}/{}".format(
              matched.group('year')
            , matched.group('month')
            , matched.group('day')
            , matched.group('title')
        ), headers={'Accept': 'application/json'})

        self.assertEquals(response.status_code, 200)
        body = json.loads(response.data)

        self.assertTrue('meta' in body)
        self.assertTrue('body' in body)
        self.assertTrue('date' in body['meta'])
        self.assertTrue('title' in body)

    def test_article_not_found(self):
        response = fixtures.client.get('/inkwell/2011/01/01/not-found', 
            headers={'Accept': 'application/json'})

        self.assertEquals(response.status_code, 404)

    def test_article_year_badrequest(self):
        response = fixtures.client.get('/inkwell/9999/01/01/not-found', 
            headers={'Accept': 'application/json'})