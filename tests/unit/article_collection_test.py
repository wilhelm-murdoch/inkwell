# -*- coding: utf-8 -*-
from inkwell.reader import ArticleCollection, Article
import unittest
from tests import fixtures

class ArticleCollectionTest(unittest.TestCase):
    def setUp(self):
        self.articles = []
        for filename in fixtures.valid_files:
            self.articles.append(Article(filename=filename))

    def test_init_with_articles(self):
        collection = ArticleCollection(items=self.articles)

        self.assertEquals(len(collection.items), len(self.articles))

    def test_init_without_articles(self):
        collection = ArticleCollection()
        collection.items = self.articles

        self.assertEquals(len(collection.items), len(self.articles))

    def test_init_with_invalid_articles(self):
        try:
            collection = ArticleCollection(items=[1, 2, 3, 4])
            assert False
        except AssertionError as e:
            assert True

        try:
            collection = ArticleCollection(items='merpflakes')
            assert False
        except AssertionError as e:
            assert True

    def test_first(self):
        collection = ArticleCollection(items=self.articles)
        self.assertEquals(self.articles[0], collection.first())

    def test_last(self):
        collection = ArticleCollection(items=self.articles)
        self.assertEquals(self.articles[len(self.articles) - 1], \
            collection.last())

    def test_current(self):
        collection = ArticleCollection(items=self.articles)
        collection.next()
        self.assertEquals(self.articles[1], collection.current())

    def test_rewind(self):
        collection = ArticleCollection(items=self.articles)
        collection.next()
        collection.next()
        collection.next()
        collection.rewind()
        self.assertEquals(self.articles[0], collection.current())

    def test_sort(self):
        collection = ArticleCollection(items=self.articles).compose()

        first = collection.first()
        last  = collection.last()

        collection.sort(by='date', reverse=True)

        self.assertEquals(collection.first(), last)
        self.assertEquals(collection.last(), first)

    def test_sort_lambda(self):
        articles = [
              Article(filename='2013-07-02-a-title.txt')
            , Article(filename='2013-07-02-b-title.txt')
        ]

        collection = ArticleCollection(items=articles).compose()

        first = collection.first()
        last  = collection.last()

        collection.sort(by=lambda a: a.title, reverse=True)

        self.assertEquals(collection.first(), last)
        self.assertEquals(collection.last(), first)

    def test_getitem(self):
        collection = ArticleCollection(items=self.articles)

        try:
            collection[1]
            collection[2]
            assert True
        except:
            assert False

    def test_out_of_range_getitem(self):
        collection = ArticleCollection(items=self.articles)

        try:
            collection[9999]
            assert False
        except IndexError:
            assert True

    def test_len(self):
        collection = ArticleCollection(items=self.articles)

        self.assertEquals(len(collection), len(self.articles))

    def test_append(self):
        collection = ArticleCollection(items=self.articles)
        article = Article(filename='2013-07-02-a-title.txt').compose()
        collection.append(article)

        self.assertEquals(article.title, collection.last().title)

    def test_extend(self):
        collection = ArticleCollection(items=self.articles)
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
        collection = ArticleCollection(items=self.articles)
        json = collection.to_json()
        collection.is_valid(collection)

    def test_iterable(self):
        collection = ArticleCollection(items=self.articles)
        try:
            for article in collection:
                pass
            assert True
        except:
            assert False
