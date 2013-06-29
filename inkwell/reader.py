# -*- coding: utf-8 -*-
import os
import re
import yaml
import time
from dateutil import parser
from datetime import datetime
import markdown

ARTICLE_FILE_PATTERN = r'^(?P<year>\d{4})\-(?P<month>\d{2})\-(?P<day>\d{2})\-(?P<title>.*)\.txt$'
ARTICLE_FILE_SEARCH_PATTERN = r'^%s\-%s\-%s\-.*\.txt$'
ARTICLE_FILE_EXTENSION = 'txt'

class Reader(object):
    def __init__(self, **kwargs):
        self.articles_folder = kwargs.get('articles_folder', None)
        self._cache = []

    @property
    def articles_folder(self):
        return self._articles_folder

    @articles_folder.setter
    def articles_folder(self, path):
        path = os.path.join(os.getcwd(), path)
        if not os.path.exists(path):
            raise IOError, "article path {} is invalid".format(path)
        self._articles_folder = path

    def list(self, by_year=None, by_month=None, by_day=None):
        articles = ArticleCollection()
        for filename in self._filter_articles(by_year, by_month, by_day):
            article = self.article(filename=filename)
            if article:
                articles.append(article)
        return articles

    def fetch_article(self, filename=None, **kwargs):
        if not filename:
            filename = "{}.{}".format('-'.join([
                  str(kwargs.get('year', ''))
                , str(kwargs.get('month', ''))
                , str(kwargs.get('day', ''))
                , str(kwargs.get('title', ''))
            ]), ARTICLE_FILE_EXTENSION)

        path_to_file = os.path.join(self._articles_folder, filename)
        if os.path.isfile(path_to_file):
            try:
                with open(path_to_file) as file:
                    return self._article_factory(file)
            except:
                raise
        return False

    def _article_factory(self, file):
        file_contents = file.read()
        filename = os.path.basename(file.name)
        file.close()

        try:
            header, body = file_contents.split('\n\n', 1)
        except:
            raise InvalidArticle, "{} may be malformed.".format(filename)

        try:
            meta = yaml.load(header)
        except:
            raise InvalidArticleHeader, "{} has an invalid header.".format(\
                filename)

        return Article(filename=filename, meta=meta, body=body).compose()

    def _build_filter_pattern(self, year, month, day):
        return ARTICLE_FILE_SEARCH_PATTERN % (
              year  or '\d{4}'
            , month or '\d{2}'
            , day   or '\d{2}'
        )

    def _filter_articles(self, year=None, month=None, day=None):
        return [file for file in os.listdir(self.articles_folder) if \
            re.match(self._build_filter_pattern(year, month, day), file)]


class Article(object):
    def __init__(self, filename, **kwargs):
        self.filename = filename
        self.meta = kwargs.get('meta', {})
        self.body = kwargs.get('body', '')
        self.title = kwargs.get('title', '')
        self.date = None
        self.is_composed = False

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, meta):
        self._meta = meta

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = markdown.markdown(body)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title=None):
        if not title:
            matched = re.search(ARTICLE_FILE_PATTERN, self.filename)
            title = self._unslugify(matched.group('title'))
        self._title = title

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if isinstance(date, datetime):
            return
        if not date:
            matched = re.search(ARTICLE_FILE_PATTERN, self.filename)
            self._date = parser.parse("{}/{}/{}".format(
                  matched.group('year')
                , matched.group('month')
                , matched.group('day')
            ))
        else:
            self._date = parser.parse(date)

        self._meta['date'] = self.date

    def compose(self, body=None, meta=None):
        if self.is_composed:
            return True

        if body and not self.body:
            assert isinstance(body, str)
            self.body = body

        if meta and not self.meta:
            assert isinstance(meta, dict)
            self.meta = meta

        for key, value in self.meta.iteritems():
            setattr(self, key, value)

        self.is_composed = True

        return self

    def to_json(self):
        if not self.is_composed:
            self.compose()

        return {
              'meta': self.meta
            , 'body': self.body
        }

    def _unslugify(self, string):
        return string.replace('-', ' ').replace('_', ' ').title()

    def __getattr__(self, attr):
        return None

class ArticleCollection(object):
    def __init__(self, **kwargs):
        self.items = kwargs.get('items', [])
        self._current_index = 0

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        assert isinstance(items, list)
        assert self.is_valid(items), "items must be a list of class Article instances."
        self._items = items

    def first(self):
        return self.items[0]

    def last(self):
        return self.items[len(self.items) - 1]

    def current(self):
        return self.items[self._current_index]

    def rewind(self):
        self._current_index = 0

    def next(self):
        try:
            next = self.items[self._current_index + 1]
            self._current_index += 1
            return next
        except IndexError:
            raise

    def sort(self, by, reverse=False):
        if isinstance(by, type(lambda: None)) and by.__name__ == '<lambda>':
            self.items.sort(key = by, reverse=reverse)
        else:
            self.items.sort(key = lambda x: getattr(x, by), reverse=reverse)
        return self.items

    def __getitem__(self, i):
        return self.items[i]

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        for item in self.items:
            yield item

    def extend(self, items):
        assert isinstance(items, list)
        assert self.is_valid(items), "items must be a list of class Article instances."
        self.items.extend(items)

    def append(self, item):
        assert isinstance(item, Article), "item must be an instance of class Article."
        self.items.append(item)

    def is_valid(self, items):
        if not isinstance(items, list):
            items = [items]
        for index, item in enumerate(items):
            if not isinstance(item, Article):
                return False
        return True

    def to_json(self):
        return self.items

class InvalidArticle(Exception): pass
class InvalidArticleHeader(Exception): pass