# -*- coding: utf-8 -*-
from inkwell.reader import ArticleCollection, Article
import unittest
from tests import fixtures
from random import shuffle

class ArticleCollectionTest(unittest.TestCase):
    def setUp(self):
        self.articles = []
        for filename in fixtures.valid_files:
            self.articles.append(Article(filename=filename))

    def test_init_with_articles(self):
        collection = ArticleCollection(articles=self.articles)

        self.assertEquals(len(collection.articles), len(self.articles))

    def test_init_without_articles(self):
        collection = ArticleCollection()
        collection.articles = self.articles

        self.assertEquals(len(collection.articles), len(self.articles))

    def test_init_with_invalid_articles(self):
        try:
            collection = ArticleCollection(articles=[1, 2, 3, 4])
            assert False
        except AssertionError as e:
            assert True

        try:
            collection = ArticleCollection(articles='merpflakes')
            assert False
        except AssertionError as e:
            assert True

    def test_first(self):
        collection = ArticleCollection(articles=self.articles)
        self.assertEquals(self.articles[0], collection.first())

    def test_last(self):
        collection = ArticleCollection(articles=self.articles)
        self.assertEquals(self.articles[len(self.articles) - 1], \
            collection.last())

    def test_current(self):
        collection = ArticleCollection(articles=self.articles)
        collection.next()
        self.assertEquals(self.articles[1], collection.current())

    def test_rewind(self):
        collection = ArticleCollection(articles=self.articles)
        collection.next()
        collection.next()
        collection.next()
        collection.rewind()
        self.assertEquals(self.articles[0], collection.current())

    def test_sort(self):
        filenames_to_titles = {
              '2013-07-02-a-title.txt': 'A Title'
            , '2013-07-02-b-title.txt': 'B Title'
            , '2013-07-02-d-title.txt': 'D Title'
            , '2013-07-02-q-title.txt': 'Q Title'
            , '2013-07-02-t-title.txt': 'T Title'
        }

        articles = [
            Article(filename=k)
            for k in filenames_to_titles.keys()
        ]

        shuffle(articles)

        collection = ArticleCollection(articles=articles).sort(by='title', reverse=True)

        titles = filenames_to_titles.values()
        titles.sort(reverse=True)

        for i, _ in enumerate(titles):
            self.assertEquals(collection[i].title, titles[i])

    def test_sort_lambda(self):
        articles = [
              Article(filename='2013-07-02-a-title.txt')
            , Article(filename='2013-07-02-b-title.txt')
        ]

        collection = ArticleCollection(articles=articles)

        first = collection.first()
        last  = collection.last()

        collection.sort(by=lambda a: a.title, reverse=True)

        self.assertEquals(collection.first(), last)
        self.assertEquals(collection.last(), first)

    def test_getarticle(self):
        collection = ArticleCollection(articles=self.articles)

        try:
            collection[1]
            collection[2]
            assert True
        except:
            assert False

    def test_out_of_range_getarticle(self):
        collection = ArticleCollection(articles=self.articles)

        try:
            collection[9999]
            assert False
        except IndexError:
            assert True

    def test_len(self):
        collection = ArticleCollection(articles=self.articles)

        self.assertEquals(len(collection), len(self.articles))

    def test_append(self):
        collection = ArticleCollection(articles=self.articles)
        article = Article(filename='2013-07-02-a-title.txt')
        collection.append(article)

        self.assertEquals(article.title, collection.last().title)

    def test_extend(self):
        collection = ArticleCollection(articles=self.articles)
        articles = [
              Article(filename='2013-07-02-a-title.txt')
            , Article(filename='2013-07-02-b-title.txt')
        ]
        collection.extend(articles)

        self.assertEquals(collection[-1], articles[-1])
        self.assertEquals(collection[-2], articles[-2])

    def test_is_valid(self):
        try:
            collection = ArticleCollection()
            collection.is_valid(Article(filename='2013-07-02-b-title.txt'))
            assert True
        except AssertionError as e:
            assert False

    def test_is_not_valid(self):
        try:
            collection = ArticleCollection()
            collection.is_valid('nope')
            assert False
        except AssertionError as e:
            assert True

    def test_to_json(self):
        collection = ArticleCollection(articles=self.articles)
        json = collection.to_json()
        collection.is_valid(collection)

    def test_iterable(self):
        collection = ArticleCollection(articles=self.articles)
        try:
            for article in collection:
                pass
            assert True
        except:
            assert False
