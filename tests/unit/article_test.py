# -*- coding: utf-8 -*-
from inkwell.reader import Article, Reader, ARTICLE_FILE_PATTERN
from dateutil import parser
from datetime import datetime
import re
import unittest
from tests import fixtures

class ArticleTest(unittest.TestCase):
    def test_raise_on_invalid_filename(self):
        try:
            Article(filename='invalidfilename.txt')
            assert False
        except ValueError:
            assert True

    def test_without_meta(self):
        filename = fixtures.valid_files[0]
        article = Article(filename=filename, body='Lorem Ipsum')

        self.assertEquals(filename, article.filename)
        self.assertEquals(article.body, 'Lorem Ipsum')
        self.assertTrue(isinstance(article, Article))

        matched = re.search(ARTICLE_FILE_PATTERN, filename)
        date = parser.parse("{}/{}/{}".format(
              matched.group('year')
            , matched.group('month')
            , matched.group('day')
        ))

        self.assertEquals(article.date, date)
        self.assertEquals(article.title, article._unslugify(\
            matched.group('title')))

    def test_without_body_and_meta(self):
        filename = fixtures.valid_files[0]
        article = Article(filename=filename)

        self.assertEquals(filename, article.filename)
        self.assertEquals(article.body, '')
        self.assertTrue(isinstance(article, Article))

        matched = re.search(ARTICLE_FILE_PATTERN, filename)
        date = parser.parse("{}/{}/{}".format(
              matched.group('year')
            , matched.group('month')
            , matched.group('day')
        ))

        self.assertEquals(article.date, date)
        self.assertEquals(article.title, article._unslugify(\
            matched.group('title')))

    def test_without_body_but_with_meta(self):
        filename = fixtures.valid_files[0]
        meta = {
              'title': 'This is a test title'
            , 'arbitrary': 'blerp'
        }
        article = Article(filename=filename, meta=meta)

        self.assertEquals(filename, article.filename)
        self.assertEquals(article.body, '')
        self.assertTrue(isinstance(article, Article))

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
                'title': article._unslugify(matched.group('title'))
              , 'meta': {
                  'date': date
                , 'slug': matched.group('title')
                , 'year': matched.group('year')
                , 'month': matched.group('month')
                , 'day': matched.group('day')
                , 'path': "{}/{}/{}/{}".format(
                      matched.group('year')
                    , matched.group('month')
                    , matched.group('day')
                    , matched.group('title')
                )
              }
            , 'body': False
            , 'summary': False
        })

    def test_article_has_summary(self):
        filename = '2013-07-28-summary-test.txt'
        meta = {
              'title': 'I should have a summary!'
            , 'summary': True
        }
        body = """This is a summary.\n\nThis is a body."""

        article = Article(filename=filename, meta=meta, body=body).to_json()

        self.assertEquals(article['summary'], '<p>This is a summary.</p>')
        self.assertEquals(article['body'], '<p>This is a body.</p>')

    def test_article_has_no_summary(self):
        filename = '2013-07-28-summary-test.txt'
        meta = {
            'title': 'I should have a summary!'
        }

        article = Article(filename=filename, meta=meta).to_json()

        self.assertFalse(article['summary'])

    def test_unslugify(self):
        for filename in fixtures.valid_files:
            article = Article(filename=filename)
            matched = re.search(ARTICLE_FILE_PATTERN, filename)
            self.assertEquals(article.title, article._unslugify(\
                matched.group('title')))

    def test_getattr(self):
        filename = fixtures.valid_files[0]
        article = Article(filename=filename)

        self.assertIsNone(article.does_not_exist_here)
        self.assertIsNone(article.does_not_exist_there)
        self.assertIsNone(article.does_not_exist_anywhere)
