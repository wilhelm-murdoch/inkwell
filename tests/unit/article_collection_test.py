import inkwell
import unittest
from tests import fixtures

class ArticleCollectionTest(unittest.TestCase):
    def setUp(self):
        reader = inkwell.reader.Reader(articles_folder=\
            fixtures.valid_articles_folder)
        self.articles = reader.list()

    def test_init_with_articles(self):
        ''' ArticleCollection: Init with list of articles '''
        pass

    def test_init_without_articles(self):
        ''' ArticleCollection: Init without initial list of articles '''
        pass

    def test_init_with_invalid_articles(self):
        ''' ArticleCollection: Init with list of invalid articles '''
        pass

    def test_first(self):
        ''' ArticleCollection: Returns first article in collection '''
        pass

    def test_last(self):
        ''' ArticleCollection: Returns last article in collection '''
        pass

    def test_current(self):
        ''' ArticleCollection: Returns current article in collection'''
        pass

    def test_rewind(self):
        ''' ArticleCollection: Rewinds iterator back to first article in collection '''
        pass

    def test_sort(self):
        ''' ArticleCollection: Can properly sort collection by specified article attribute '''
        pass

    def test_sort_reverse(self):
        ''' ArticleCollection: Can properly sort collection by specified article attribute in reverse'''
        pass

    def test_sort_lambda(self):
        ''' ArticleCollection: Can properly sort collection by with custom lambda sort '''
        pass

    def test_getitem(self):
        ''' ArticleCollection: Returns desired article by associated index '''
        pass

    def test_len(self):
        ''' ArticleCollection: Returns length of collection using len() '''
        pass

    def test_append(self):
        ''' ArticleCollection: Appends article to the end of collection '''
        pass

    def test_extend(self):
        ''' ArticleCollection: Combines current collection with another '''
        pass

    def test_is_valid(self):
        ''' Determine validity of specified element '''
        pass

    def test_to_json(self):
        ''' ArticleCollection: JSON output is structured properly '''
        pass

    def test_iterable(self):
        ''' ArticleCollection: Implements iterable interface '''
        pass
