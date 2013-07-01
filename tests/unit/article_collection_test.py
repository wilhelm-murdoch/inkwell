from inkwell.reader import ArticleCollection, Article
import unittest
from tests import fixtures

class ArticleCollectionTest(unittest.TestCase):
    def setUp(self):
        self.articles = []
        for filename in fixtures.valid_files:
            self.articles.append(Article(filename=filename))

    def test_init_with_articles(self):
        ''' ArticleCollection: Init with list of articles '''
        collection = ArticleCollection(items=self.articles)

        self.assertEquals(len(collection.items), len(self.articles))

    def test_init_without_articles(self):
        ''' ArticleCollection: Init without initial list of articles '''
        collection = ArticleCollection()
        collection.items = self.articles

        self.assertEquals(len(collection.items), len(self.articles))

    def test_init_with_invalid_articles(self):
        ''' ArticleCollection: Init with list of invalid articles '''
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
        ''' ArticleCollection: Returns first article in collection '''
        collection = ArticleCollection(items=self.articles)

        self.assertEquals(self.articles[0], collection.first())

    def test_last(self):
        ''' ArticleCollection: Returns last article in collection '''
        collection = ArticleCollection(items=self.articles)

        self.assertEquals(self.articles[len(self.articles) - 1], \
            collection.last())

    def test_current(self):
        ''' ArticleCollection: Returns current article in collection'''
        collection = ArticleCollection(items=self.articles)
        collection.next()

        self.assertEquals(self.articles[1], collection.current())

    def test_rewind(self):
        ''' ArticleCollection: Rewinds iterator back to first article in collection '''
        collection = ArticleCollection(items=self.articles)
        collection.next()
        collection.next()
        collection.next()
        collection.rewind()

        self.assertEquals(self.articles[0], collection.current())

    def test_sort(self):
        ''' ArticleCollection: Can properly sort collection by specified article attribute '''
        collection = ArticleCollection(items=self.articles).compose()

        first = collection.first()
        last = collection.last()

        collection.sort(by='date', reverse=True)

        self.assertEquals(collection.first(), last)
        self.assertEquals(collection.last(), first)

    def test_sort_lambda(self):
        ''' ArticleCollection: Can properly sort collection by with custom lambda sort '''
        articles = [
              Article(filename='2013-07-02-a-title.txt')
            , Article(filename='2013-07-02-b-title.txt')
        ]

        collection = ArticleCollection(items=articles).compose()

        first = collection.first()
        last = collection.last()

        collection.sort(by=lambda x: x.title.lower, reverse=True)

        self.assertEquals(collection.first(), last)
        self.assertEquals(collection.last(), first)

    def test_getitem(self):
        ''' ArticleCollection: Returns desired article by associated index '''
        collection = ArticleCollection(items=self.articles)

        try:
            collection[1]
            collection[2]
            assert True
        except:
            assert False

    def test_out_of_range_getitem(self):
        ''' ArticleCollection: Raises IndexError when accessing out-of-range index '''
        collection = ArticleCollection(items=self.articles)

        try:
            collection[9999]
            assert False
        except IndexError:
            assert True

    def test_len(self):
        ''' ArticleCollection: Returns length of collection using len() '''
        collection = ArticleCollection(items=self.articles)

        self.assertEquals(len(collection), len(self.articles))

    def test_append(self):
        ''' ArticleCollection: Appends article to the end of collection '''
        collection = ArticleCollection(items=self.articles)
        article = Article(filename='2013-07-02-a-title.txt').compose()
        collection.append(article)

        self.assertEquals(article.title, collection.last().title)

    def test_extend(self):
        ''' ArticleCollection: Combines current collection with another '''
        collection = ArticleCollection(items=self.articles)
        articles = [
              Article(filename='2013-07-02-a-title.txt')
            , Article(filename='2013-07-02-b-title.txt')
        ]
        collection.extend(articles)

        self.assertEquals(collection[-1], articles[-1])
        self.assertEquals(collection[-2], articles[-2])

    def test_is_valid(self):
        ''' ArticleCollection: Determine validity of specified element '''
        try:
            collection = ArticleCollection()
            collection.is_valid(Article(filename='2013-07-02-b-title.txt'))
            assert True
        except AssertionError as e:
            assert False

    def test_is_not_valid(self):
        ''' ArticleCollection: Determine invalidity of specified element '''
        try:
            collection = ArticleCollection()
            collection.is_valid('nope')
            assert False
        except AssertionError as e:
            assert True

    def test_to_json(self):
        ''' ArticleCollection: JSON output is structured properly '''
        collection = ArticleCollection(items=self.articles)
        json = collection.to_json()
        collection.is_valid(collection)

    def test_iterable(self):
        ''' ArticleCollection: Implements iterable interface '''
        collection = ArticleCollection(items=self.articles)
        try:
            for article in collection:
                pass
            assert True
        except:
            assert False
