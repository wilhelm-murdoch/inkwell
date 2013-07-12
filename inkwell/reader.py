# -*- coding: utf-8 -*-
import os
import re
import yaml
from dateutil import parser
from datetime import datetime

ARTICLE_FILE_PATTERN = r'^(?P<year>\d{4})\-(?P<month>\d{2})\-(?P<day>\d{2})\-(?P<title>.*)\.txt$'
ARTICLE_FILE_SEARCH_PATTERN = r'^%s\-%s\-%s\-.*\.txt$'
ARTICLE_FILE_EXTENSION = 'txt'

class Reader(object):
    """ Class `inkwell.reader.Reader` is responsible for finding articles within
    the specified `articles_folder`. If any are found, it will produce an
    instance of `inkwell.reader.ArticleCollection`, which contains a list of
    parsed articles in the form of `inkwell.reader.Article`.

    Usage::

        reader = Reader(articles_folder='/path/to/articles')

        try:
            # Fetch all relevant articles ...
            result = reader.list()

            # Or, fetch them by year ...
            result = reader.list(by_year='2013')

            # Or, fetch them by year and month ...
            result = reader.list(by_year='2013', by_month='12')

            # Or, fetch them by year, month and day ...
            result = reader.list(by_year='2013', by_month='12', by_day='01')
        except Exception as e:
            print "Doh! {}".format(e.message)

        for article in result:
            print article.title
    """

    def __init__(self, **kwargs):
        """ Creates class instance and assigns properties.

        Arguments::
            kwargs['articles_folder'] str absolute path to the articles folder.
        """
        self.articles_folder = kwargs.get('articles_folder', None)

    @property
    def articles_folder(self):
        """ Provides access to `Reader._articles_folder`

        Returns::
            str absolute path to the articles folder.
        """
        return self._articles_folder

    @articles_folder.setter
    def articles_folder(self, path):
        """ Sets and validates the specified path to the articles folder. If
        the specified path is not valid, this method will raise IOError.
        """
        path = os.path.join(os.getcwd(), path)
        if not os.path.exists(path):
            raise IOError, "article path {} is invalid".format(path)
        self._articles_folder = path

    def list(self, by_year=None, by_month=None, by_day=None):
        """ Responsible for searching the specified articles folder for files
        that match ARTICLE_FILE_SEARCH_PATTERN. Returns an instance of
        `inkwell.reader.ArticleCollection` if any articles are found.

        Optional arguments can be used to filter articles by date.

        Arguments::
            by_year  str Four-digit number representing the article year
            by_month str Two-digit number representing the article month
            by_day   str Two-digit number representing the article day

        Returns::
            instance of `inkwell.reader.ArticleCollection`
        """
        articles = ArticleCollection()
        for filename in self._filter_articles(by_year, by_month, by_day):
            article = self.fetch_article(filename=filename)
            if article:
                articles.append(article)
        return articles

    def fetch_article(self, filename=None, **kwargs):
        """ Attempts to locate and open the specified file. If a filename is
        not specified, a filename can be constructed using optional arguments.

        Arguments::
            filename str Filename matching ARTICLE_FILE_SEARCH_PATTERN
            year     str Four-digit number representing the article year
            month    str Two-digit number representing the article month
            day      str Two-digit number representing the article day
            title    str Slugified title of article

        Return::
            instance of `inkwell.reader.Article`

        Note::
            If filename is not specified, all other optional arguments must be
            specified or there will be nothing to fetch. If this is the case,
            this method will raise ValueError.
        """
        if not filename:
            year  = kwargs.get('year', None)
            month = kwargs.get('month', None)
            day   = kwargs.get('day', None)
            title = kwargs.get('title', None)

            if not year and not month and not day and not title:
                raise ValueError, 'Year, month, day and title not specified.'

            filename = "{}.{}".format('-'.join([
                  str(year)
                , str(month)
                , str(day)
                , str(title)
            ]), ARTICLE_FILE_EXTENSION)

        path_to_file = os.path.join(self._articles_folder, filename)

        if os.path.isfile(path_to_file):
            try:
                with open(path_to_file) as file:
                    article = self._article_factory(file.read(), filename)
                    file.close()
                return article
            except:
                raise
        return False

    def _article_factory(self, content, filename):
        """ Attempts to parse the given file stream for article header and body
        blocks. If all goes well, this method will return a single instance of
        `inkwell.reader.Article` with all associated metadata.

        Arguments::
            content  str The content of the current file.
            filename str The name of the current file.

        Return::
            instance of `inkwell.reader.Article`

        Note::
            The body of the file must meet certain requirements in order to be
            properly parsed. The header block is contained before the first two
            consecutive newline `\n` entries. The header must be formatted in
            YAML. Everything after the first `\n\n` is considered the body.

            Will raise ValueError if the file or header block are invalid.
        """
        try:
            header, body = content.split('\n\n', 1)
        except:
            raise ValueError, "{} may be malformed.".format(filename)

        try:
            meta = yaml.load(header)

            if isinstance(meta, str):
                body = meta
                meta = {}
        except:
            raise ValueError, "{} has an invalid header.".format(filename)

        return Article(filename=filename, meta=meta, body=body).compose()

    def _build_filter_pattern(self, year=None, month=None, day=None):
        """This method will attempt to dynamically construct the REGEX used to
        filter files by date elements.

        Arguments::
            year  str Four-digit number representing the article year
            month str Two-digit number representing the article month
            day   str Two-digit number representing the article day

        Returns::
            A string containing the appropriate regular expression to filter
            all files in the given directory, or to filter them by date.
        """
        return ARTICLE_FILE_SEARCH_PATTERN % (
              year  or '\d{4}'
            , month or '\d{2}'
            , day   or '\d{2}'
        )

    def _filter_articles(self, year=None, month=None, day=None):
        """Applies the configured filter pattern to the specified articles
        folder and returns a list containing the resulting filenames.

        Arguments::
            year  str Four-digit number representing the article year
            month str Two-digit number representing the article month
            day   str Two-digit number representing the article day

        Returns::
            A list containing any matched filenames.
        """
        return [file for file in os.listdir(self.articles_folder) if \
            re.match(self._build_filter_pattern(year, month, day), file)]


class Article(object):
    IGNORED_META_TAGS = ['date']

    def __init__(self, filename, **kwargs):
        self.filename = filename
        self.meta = kwargs.get('meta', {})
        self.body = kwargs.get('body', '')
        self.title = kwargs.get('title', '')
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
        self._body = body

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title=None):
        if title:
            self._title = title
        else:
            matched = re.search(ARTICLE_FILE_PATTERN, self.filename)
            self._title = self._unslugify(matched.group('title'))

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        assert isinstance(date, datetime)
        self._date = date

    def compose(self):
        if self.is_composed:
            return self

        matched = re.search(ARTICLE_FILE_PATTERN, self.filename)
        self.date = parser.parse("{}/{}/{}".format(
              matched.group('year')
            , matched.group('month')
            , matched.group('day')
        ))

        if self.meta:
            for key, value in self.meta.iteritems():
                if key.lower() not in self.IGNORED_META_TAGS:
                    setattr(self, key, value)

        self.meta['title'] = self.title
        self.meta['date']  = self.date

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

    def compose(self):
        for article in self:
            article.compose()
        return self

    def next(self):
        try:
            next = self.items[self._current_index + 1]
            self._current_index += 1
            return next
        except IndexError:
            raise

    def sort(self, by, reverse=False):
        if isinstance(by, type(lambda: None)) and by.__name__ == '<lambda>':
            self.items.sort(key=by, reverse=reverse)
        else:
            self.items.sort(key=lambda x: getattr(x, by), reverse=reverse)
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