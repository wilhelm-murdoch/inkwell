import inkwell
import unittest
import json
import random
import re
from tests import fixtures
from werkzeug.test import Client

class ArticleTest(unittest.TestCase):
    def setUp(self):
        self.client = inkwell.bootstrap('inkwell.config.TestConfig').test_client()

    def test_article_found(self):
        file = random.choice(fixtures.valid_files)
        matched = re.match(inkwell.reader.ARTICLE_FILE_PATTERN, file)

        response = self.client.get("/inkwell/{}/{}/{}/{}".format(
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
        self.assertTrue('title' in body['meta'])

    def test_article_not_found(self):
        response = self.client.get('/inkwell/9999/99/99/not-found', headers=\
            {'Accept': 'application/json'})
        self.assertEquals(response.status_code, 404)