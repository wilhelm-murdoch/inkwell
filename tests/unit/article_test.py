# -*- coding: utf-8 -*-
from inkwell.reader import Article, Reader, ARTICLE_FILE_PATTERN
from dateutil import parser
from datetime import datetime
import re
import unittest
from tests import fixtures

class ArticleTest(unittest.TestCase):
    def test_without_meta(self):
        filename = fixtures.valid_files[0]
        article = Article(filename=filename, body='Lorem Ipsum')

        self.assertEquals(filename, article.filename)
        self.assertEquals(article.body, '<p>Lorem Ipsum</p>')
        self.assertFalse(article.is_composed)
        composed = article.compose()
        self.assertTrue(isinstance(composed, Article))
        self.assertTrue(article.is_composed)

        article.date = None

        matched = re.search(ARTICLE_FILE_PATTERN, filename)
        date = parser.parse("{}/{}/{}".format(
              matched.group('year')
            , matched.group('month')
            , matched.group('day')
        ))

        self.assertEquals(article.date, date)
        self.assertEquals(article.title, article._unslugify(\
            matched.group('title')))

    def test_compose_without_body_and_meta(self):
        filename = fixtures.valid_files[0]
        article = Article(filename=filename)

        self.assertEquals(filename, article.filename)
        self.assertEquals(article.body, '')
        self.assertFalse(article.is_composed)
        composed = article.compose()
        self.assertTrue(isinstance(composed, Article))
        self.assertTrue(article.is_composed)

        article.date = None

        matched = re.search(ARTICLE_FILE_PATTERN, filename)
        date = parser.parse("{}/{}/{}".format(
              matched.group('year')
            , matched.group('month')
            , matched.group('day')
        ))

        self.assertEquals(article.date, date)
        self.assertEquals(article.title, article._unslugify(\
            matched.group('title')))

    def test_compose_without_body_but_with_meta(self):
        filename = fixtures.valid_files[0]
        meta = {
              'title': 'This is a test title'
            , 'date': '2013/07/02 10:00:00'
            , 'arbitrary': 'blerp'
        }
        article = Article(filename=filename, meta=meta)

        self.assertEquals(filename, article.filename)
        self.assertEquals(article.body, '')
        self.assertFalse(article.is_composed)
        composed = article.compose()
        self.assertTrue(isinstance(composed, Article))
        self.assertTrue(article.is_composed)

        self.assertEquals(article.date, meta['date'])
        self.assertEquals(article.arbitrary, meta['arbitrary'])
        self.assertEquals(article.title, meta['title'])

    def test_to_json(self):
        filename = fixtures.valid_files[0]
        article = Article(filename=filename)

        matched = re.search(ARTICLE_FILE_PATTERN, filename)
        date = parser.parse("{}/{}/{}".format(
              matched.group('year')
            , matched.group('month')
            , matched.group('day')
        ))

        self.assertEquals(article.to_json(), {
              'meta': {
                  'title': article._unslugify(matched.group('title'))
                , 'date': date
              }
            , 'body': ''
        })

    def test_unslugify(self):
        for filename in fixtures.valid_files:
            article = Article(filename=filename).compose()
            matched = re.search(ARTICLE_FILE_PATTERN, filename)
            self.assertEquals(article.title, article._unslugify(\
                matched.group('title')))

    def test_getattr(self):
        filename = fixtures.valid_files[0]
        article = Article(filename=filename).compose()

        self.assertIsNone(article.does_not_exist_here)
        self.assertIsNone(article.does_not_exist_there)
        self.assertIsNone(article.does_not_exist_anywhere)