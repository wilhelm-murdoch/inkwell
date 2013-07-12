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

        return Article(filename=filename, meta=meta, body=body)

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
    """ Class `inkwell.reader.Article` is an abstract representation of a
    single article entry. This class is not responsible for parsing file and
    creating attributes, that's the job of `inkwell.reader.Reader`. You
    must, at the very least, specify a filename. If no other attributes are
    specified, upon composition, this class will attempt to derive a date and
    title from the specified filename itself. Title, date and body properties
    are completely optional, but the specified filename must match the
    `inkwell.reader.ARTICLE_FILE_PATTERN` pattern or a ValueError will be
    raised.

    Usage::

        article = Article(filename='2013-07-12-example.txt')

        print article.title
        >>> 'Example'

        print article.date
        >>> datetime.datetime(2013, 7, 12, 0, 0)

        print article.body
        >>> ''

        try:
            Article(filename='aninvalidfilename.txt')
        except ValueError as e:
            print e.message

        article = Article(
              filename='2013-07-12-example.txt'
            , title='Another Example'
            , meta={'tags': ['foo', 'bar'], 'time': '12:34:00'}
            , body='This is a body'
        )

        print article.title
        >>> 'Another Example'

        print article.date
        >>> datetime.datetime(2013, 7, 12, 0, 0)

        print article.body
        >>> 'This is a body'

        print article.tags
        >>> ['foo', 'bar']
    """

    """ This is a list containing reserved metadata keywords. """
    IGNORED_META_TAGS = ['date']

    def __init__(self, filename, **kwargs):
        """ Creates class instance and assigns properties.

        Arguments::
            filename        str  the name of article's file.
            kwargs['title'] str  official article title
            kwargs['body']  str  the main body of the article
            kwargs['meta']  dict containing additional metadata properties

        Raises::
            ValueError for invalid filename values
        """
        self.matched = re.search(ARTICLE_FILE_PATTERN, filename)
        if not self.matched:
            raise ValueError, 'filename must match ARTICLE_FILE_PATTERN.'

        self.filename = filename
        self.meta = kwargs.get('meta', {})
        self.body = kwargs.get('body', '')
        self.title = kwargs.get('title', '')

        self.date = parser.parse("{}/{}/{}".format(
              self.matched.group('year')
            , self.matched.group('month')
            , self.matched.group('day')
        ))

        if self.meta:
            for key, value in self.meta.iteritems():
                if key.lower() not in self.IGNORED_META_TAGS:
                    setattr(self, key, value)

        self.meta['title'] = self.title
        self.meta['date']  = self.date

    @property
    def title(self):
        """Returns the current article's title."""
        return self._title

    @title.setter
    def title(self, title=None):
        """Sets the current article's title. If one is not specified, this method
        will fall back upon the <title> portion of the ARTICLE_FILE_PATTERN and
        attempt to unslugify it.

        Arguments::
            title str,None the title of the article
        """
        if title:
            self._title = title
        else:
            self._title = self._unslugify(self.matched.group('title'))

    @property
    def date(self):
        """Returns the current article's date."""
        return self._date

    @date.setter
    def date(self, date):
        """Sets the current article's date. This is derived from the article's
        specified filename.

        Arguments::
            date datetime the current article's date
        """
        assert isinstance(date, datetime)
        self._date = date

    def to_json(self):
        """ Returns a JSON representation of the current article.

        Usage::

            article = Article(
                  filename='2013-07-12-example.txt'
                , title='Another Example'
                , meta={'tags': ['foo', 'bar'], 'time': '12:34:00'}
                , body='This is a body'
            )

            print article.to_json()
            >>> {
                'meta': {
                      'title': 'Another Example'
                    , 'tags': ['foo', 'bar']
                    , 'date': '2013-07-12T00:00:00Z'
                    , 'time': '12:34:00'
                }
                , 'body': 'This is a body'
            }

        Returns::
            dictionary containing the JSON output for the article.
        """
        return {
              'meta': self.meta
            , 'body': self.body
        }

    def _unslugify(self, string):
        """Takes the provided string and converts it into a human-readable
        article title. This is primarily used as a fallback when no official
        title is provided, where the filename itself is used instead.

        Usage::

            print article._unslugify('this-is-a-title')
            >>> 'This Is A Title'

        Arguments::
            string str the string to unslugify

        Returns::
            an unslugified string
        """
        return string.replace('-', ' ').replace('_', ' ').title()

    def __getattr__(self, attr):
        """ Prevents raising of KeyError when accessing a non-existent
        attribute.

        Returns::
            None
        """
        return None

class ArticleCollection(object):
    """ Class `inkwell.reader.ArticleCollection` is an iterable collection of
    `inkwell.reader.Article` instances. This class is useful to people who
    wish to use Inkwell as an internal module rather than a server or
    blueprint.

    Usage::
        articles = [
              Article(filename='2013-07-02-a-title.txt')
            , Article(filename='2013-07-02-b-title.txt')
        ]

        collection = ArticleCollection(articles=articles)

        for article in collection:
            print article.title

        >>> A Title
        >>> B Title
    """
    def __init__(self, **kwargs):
        """ Creates class instance and assigns properties.

        Arguments::
            kwargs['articles'] list a list of `inkwell.reader.Article` instances
        """
        self.articles = kwargs.get('articles', [])
        self._current_index = 0

    @property
    def articles(self):
        """Returns the current collection of articles."""
        return self._articles

    @articles.setter
    def articles(self, articles):
        """Sets the current collection of articles. If there are already
        articles assocaited with the current ArticleCollection instance, they
        will be replaced by the specified list.

        Raises:
            AssertionError if not a valid list of Article instances.
        """
        assert isinstance(articles, list)
        assert self.is_valid(articles), 'articles must be a list of class Article instances.'
        self._articles = articles

    def first(self):
        """Returns the first article in the collection, or None if the current
        collection is empty.

        Returns::
            `inkwell.reader.Article` instance or None
        """
        if not self.articles:
            return None
        return self.articles[0]

    def last(self):
        """Returns the last article in the collection, or None if the current
        collection is empty.

        Returns::
            `inkwell.reader.Article` instance or None
        """
        if not self.articles:
            return None
        return self.articles[len(self.articles) - 1]

    def current(self):
        """Returns the article at the current position within the iterator, or
        None if the collection is empty.

        Returns::
            `inkwell.reader.Article` instance or None
        """
        if not self.articles:
            return None
        return self.articles[self._current_index]

    def rewind(self):
        """Rewinds the current position of the iterator to the first article in
        the collection.
        """
        self._current_index = 0

    def next(self):
        """Returns the article immediately after the iterators current position
        in the collection. If the end of the collection has been reached, this
        method will raise an IndexError.

        Returns::
            `inkwell.reader.Article` instance

        Raises::
            IndexError if attempting to move past the end of the collection.
        """
        try:
            next = self.articles[self._current_index + 1]
            self._current_index += 1
            return next
        except IndexError:
            raise

    def sort(self, by, reverse=False):
        """A custom sorting implementation that allows the current collection
        to be sorted by arbitrary article properties. These properties can be
        any metadata set on the article level. This method also supports the
        use of a custom sort via lambda function. Take a look at the unit tests
        to get a good idea of how to make use of this.

        Arguments::
            by      property|lambda the property to sort by
            reverse boolean         determines the direction of the sort

        Returns::
            A sorted collection of articles.
        """
        if isinstance(by, type(lambda: None)) and by.__name__ == '<lambda>':
            self.articles.sort(key=by, reverse=reverse)
        else:
            self.articles.sort(key=lambda x: getattr(x, by), reverse=reverse)
        return self.articles

    def __getitem__(self, i):
        """Implements collection access by index.

        Arguments::
            i int index pointing to the desired article in the current
            collection

        Returns::
            The desired article.

        Raises::
            IndexError if the specified index is out of range.
        """
        return self.articles[i]

    def __len__(self):
        """Implements len() functionality for the collection.

        Returns::
            Integer representing the size of the current collection.
        """
        return len(self.articles)

    def __iter__(self):
        """Returns a generator to iterate through the current collection.

        Returns::
            generator yielding articles
        """
        for article in self.articles:
            yield article

    def extend(self, articles):
        """Merges a list of articles with the current collection.

        Arguments::
            articles list A collection of `inkwell.reader.Article` instances.

        Raises::
            AssertionError if the specified list of articles is invalid.
        """
        assert isinstance(articles, list)
        assert self.is_valid(articles), 'articles must be a list of class Article instances.'
        self.articles.extend(articles)

    def append(self, article):
        """Adds an article instance to the end of the collection.

        Arguments::
            article object instance of `inkwell.reader.Article

        Raises::
            AssertionError if the specified article is invalid.
        """
        assert isinstance(article, Article), 'article must be an instance of class Article.'
        self.articles.append(article)

    def is_valid(self, articles):
        """ Validates an article, or list of articles, and ensures they are all
        instances of `inkwell.reader.Article`.

        Arguments::
            articles list a single article or list of articles.

        Returns::
            Boolean depending on the validity of the list.
        """
        if not isinstance(articles, list):
            articles = [articles]
        for index, article in enumerate(articles):
            if not isinstance(article, Article):
                return False
        return True

    def to_json(self):
        """ Returns a JSON representation of the current article collection.

        Returns::
            A list of `inkwell.reader.Article` instances.
        """
        return self.articles