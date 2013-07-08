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
                fixtures.invalid_articles_path)
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
        self.assertEquals(len(articles), len(fixtures.valid_files))

    def test_list_by_year(self):
        articles = self.reader.list(by_year='1900')
        self.assertEquals(len(articles), 1)

        articles = self.reader.list(by_year='2099')
        self.assertEquals(len(articles), 0)

        articles = self.reader.list(by_year='2013')
        self.assertEquals(len(articles), 3)

        articles = self.reader.list(by_year='2014')
        self.assertEquals(len(articles), 1)

    def test_list_by_year_and_month(self):
        articles = self.reader.list(by_year='1900', by_month='07')
        self.assertEquals(len(articles), 1)

    def test_list_by_year_month_and_day(self):
        articles = self.reader.list(by_year='2013', by_month='07', by_day='01')
        self.assertEquals(len(articles), 1)

        articles = self.reader.list(by_year='2013', by_month='07', by_day='02')
        self.assertEquals(len(articles), 1)

    def test_fetch_valid_article(self):
        article = self.reader.fetch_article(fixtures.valid_files[0])

        self.assertTrue(isinstance(article, inkwell.reader.Article))

    def test_fetch_valid_article_without_filename(self):
        article = self.reader.fetch_article(year='1900', month='07', \
            day='03', title='lorem-ipsum-example-old')

        self.assertEquals('Lorem Ipsum Example Old', article.title)
        self.assertTrue(isinstance(article.date, datetime))
        self.assertTrue(isinstance(article, inkwell.reader.Article))

    def test_fetch_invalid_article(self):
        article = self.reader.fetch_article(year='2009', month='04', \
            day='01', title='ohoneos')

        self.assertFalse(article)

    def test_article_factory(self):
        test_file = fixtures.valid_files[0]
        with open(os.path.join(fixtures.valid_articles_folder, test_file))\
            as file:
            article = self.reader._article_factory(file)

            self.assertEquals(test_file, article.filename)
            self.assertTrue(isinstance(article.date, datetime))
            self.assertTrue(isinstance(article, inkwell.reader.Article))

    def test_build_filter_pattern(self):
        filter = self.reader._build_filter_pattern()
        self.assertEquals(filter, r'^\d{4}\-\d{2}\-\d{2}\-.*\.txt$')

        filter = self.reader._build_filter_pattern(year='1900')
        self.assertEquals(filter, r'^1900\-\d{2}\-\d{2}\-.*\.txt$')

        filter = self.reader._build_filter_pattern(year='1900', month='01')
        self.assertEquals(filter, r'^1900\-01\-\d{2}\-.*\.txt$')

        filter = self.reader._build_filter_pattern(year='1900', month='01', \
            day='01')
        self.assertEquals(filter, r'^1900\-01\-01\-.*\.txt$')

    def test_filter_articles(self):
        articles = self.reader._filter_articles()
        self.assertEquals(len(fixtures.valid_files), len(articles))

        articles = self.reader._filter_articles(year='2013')
        self.assertEquals(len(articles), 3)

        articles = self.reader._filter_articles(month='07')
        self.assertEquals(len(articles), len(fixtures.valid_files))

        articles = self.reader._filter_articles(year='2013', month='07')
        self.assertEquals(len(articles), 3)

    def test_article_file_pattern(self):
        valid = invalid = 0
        for filename in (fixtures.valid_files + \
            fixtures.invalid_files):
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

        self.assertEquals(valid, len(fixtures.valid_files))
        self.assertEquals(invalid, len(fixtures.invalid_files))
