# -*- coding: utf-8 -*-

import inkwell
import unittest
import os
import re

valid_articles_folder = os.path.abspath(os.path.join(os.path.realpath(\
    __file__), os.pardir, 'articles'))

invalid_articles_folder = 'play/more/awesome/nauts'

number_of_test_articles = len([f for f in os.listdir(valid_articles_folder) \
    if re.match(r'^\d{4}\-\d{2}\-\d{2}\-.*\.txt$', f)])

valid_filenames = [
      '2010-09-01-this-is-a-test.txt'
    , '2023-09-01-this-is-also-a-test.txt'
    , '2013-09-11-this-is-another-test.txt'
    , '2030-09-01-this-is-yet-another-test.txt'
    , '2040-09-02-this-is-one-more-test.txt'
]

invalid_filenames = [
      '20400-09-02-this-is-one-more-test.txt'
    , '2040-09-02-this-is-one-more-test.log'
    , '2040-a-023-this-is-one-more-test.txt'
]