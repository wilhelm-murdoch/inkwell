# -*- coding: utf-8 -*-

import os
import inkwell
import unittest
import re
from datetime import datetime
from tests import fixtures

class ReaderTest(unittest.TestCase):
    def setUp(self):
        self.reader = inkwell.reader.Reader(articles_folder=\
            fixtures.valid_articles_folder)

    def test_invalid_article_path(self):
        try:
            inkwell.reader.Reader(articles_folder=\
                fixtures.invalid_articles_folder)
            assert False
        except IOError:
            assert True

    def test_valid_article_path(self):
        try:
            reader = inkwell.reader.Reader(articles_folder=\
                fixtures.valid_articles_folder)
        except IOError:
            assert False

        self.assertEquals(reader.articles_folder, fixtures.valid_articles_folder)

    def test_list(self):
        articles = self.reader.list()

        self.assertTrue(isinstance(articles, inkwell.reader.ArticleCollection))
        self.assertEquals(len(articles), fixtures.number_of_test_articles)

    def test_list_by_year(self):
        articles = self.reader.list(by_year=1900)
        self.assertEquals(len(articles), 1)

        articles = self.reader.list(by_year=2009)
        self.assertEquals(len(articles), 4)

        articles = self.reader.list(by_year=2001)
        self.assertEquals(len(articles), 1)

    def test_list_by_year_and_month(self):
        articles = self.reader.list(by_year=2009, by_month=12)
        self.assertEquals(len(articles), 3)

    def test_list_by_year_month_and_day(self):
        articles = self.reader.list(by_year=2009, by_month=12, by_day=11)
        self.assertEquals(len(articles), 1)

        articles = self.reader.list(by_year=2009, by_month=12, by_day=14)
        self.assertEquals(len(articles), 1)

    def test_fetch_valid_article(self):
        article = self.reader.fetch_article('2009-04-01-tilt-factor.txt')

        self.assertTrue(isinstance(article, inkwell.reader.Article))

    def test_fetch_valid_article_without_filename(self):
        article = self.reader.fetch_article(year='2009', month='04', \
            day='01', title='tilt-factor')

        self.assertEquals('the wizard of oz', article.title)
        self.assertTrue(isinstance(article.date, datetime))
        self.assertTrue(isinstance(article, inkwell.reader.Article))

    def test_fetch_invalid_article(self):
        article = self.reader.fetch_article(year='2009', month='04', \
            day='01', title='ohoneos')

        self.assertFalse(article)

    def test_article_factory(self):
        with open(os.path.join(fixtures.valid_articles_folder, '2009-12-20-invalid.xtx')) as file:
            self.reader._article_factory(file)

    def test_build_filter_pattern(self):
        pass

    def test_filter_articles(self):
        pass

    def test_article_file_pattern(self):
        valid = invalid = 0
        for filename in (fixtures.valid_filenames + \
            fixtures.invalid_filenames):
            matched = re.search(inkwell.reader.ARTICLE_FILE_PATTERN, filename)
            if matched and filename == "{}-{}-{}-{}.{}".format(
                  matched.group('year')
                , matched.group('month')
                , matched.group('day')
                , matched.group('title')
                , inkwell.reader.ARTICLE_FILE_EXTENSION
            ):
                valid += 1
            else:
                invalid += 1

        self.assertEquals(valid, len(fixtures.valid_filenames))
        self.assertEquals(invalid, len(fixtures.invalid_filenames))

class ArticleTest(unittest.TestCase):
    pass

class ArticleCollectionTest(unittest.TestCase):
    pass
