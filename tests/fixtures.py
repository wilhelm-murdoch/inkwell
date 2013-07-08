# -*- coding: utf-8 -*-
import inkwell
import unittest
import os
import re

valid_articles_folder = os.path.abspath(os.path.join(os.path.realpath(\
    __file__), os.pardir, 'articles/valid'))

invalid_articles_folder = os.path.abspath(os.path.join(os.path.realpath(\
    __file__), os.pardir, 'articles/invalid'))

invalid_articles_path = 'play/more/awesome/nauts'

valid_files = [f for f in os.listdir(valid_articles_folder) if \
    re.match(r'^\d{4}\-\d{2}\-\d{2}\-.*\.txt$', f)]

invalid_files = os.listdir(invalid_articles_folder)


dates = {}
for f in valid_files:
    matched = re.match(inkwell.reader.ARTICLE_FILE_PATTERN, f)
    if matched:
        year  = matched.group('year')
        month = matched.group('month')
        day   = matched.group('day')

        if year not in dates:
            dates.update({year: {}})

        if month not in dates[year]:
            dates[year].update({month: []})

        if day not in dates[year][month]:
            dates[year][month].append(day)

client = inkwell.bootstrap('inkwell.config.TestConfig').test_client()