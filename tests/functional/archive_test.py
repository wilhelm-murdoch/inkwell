import inkwell
import unittest
import json
import random
from tests import fixtures
from werkzeug.test import Client

class ArchiveTest(unittest.TestCase):
    def setUp(self):
        self.client = inkwell.bootstrap('inkwell.config.TestConfig').test_client()

    def test_bad_accept_header(self):
        response = self.client.get('/inkwell/')
        self.assertEquals(response.status_code, 400)

    def test_archive_root(self):
        response = self.client.get('/inkwell/', headers=\
            {'Accept': 'application/json'})
        self.assertEquals(response.status_code, 200)
        body = json.loads(response.data)
        self.assertEquals(len(body), len(fixtures.valid_files))

    def test_archive_year(self):
        year = random.choice(fixtures.dates.keys())

        response = self.client.get("/inkwell/{}".format(year), headers=\
            {'Accept': 'application/json'})

        self.assertEquals(response.status_code, 200)
        body = json.loads(response.data)

        count = 0
        for month in fixtures.dates[year]:
            count += len(fixtures.dates[year][month])

        self.assertEquals(count, len(body))

    def test_archive_year_and_month(self):
        year  = random.choice(fixtures.dates.keys())
        month = random.choice(fixtures.dates[year].keys())

        response = self.client.get("/inkwell/{}/{}".format(year, month), \
            headers={'Accept': 'application/json'})

        self.assertEquals(response.status_code, 200)
        body = json.loads(response.data)

        self.assertEquals(len(fixtures.dates[year][month]), len(body))

    def test_archive_year_month_and_day(self):
        year  = random.choice(fixtures.dates.keys())
        month = random.choice(fixtures.dates[year].keys())
        day   = random.choice(fixtures.dates[year][month])

        response = self.client.get("/inkwell/{}/{}/{}".format(year, month, \
            day), headers={'Accept': 'application/json'})

        self.assertEquals(response.status_code, 200)
        body = json.loads(response.data)

        count = 0
        for d in fixtures.dates[year][month]:
            count += 1 if d == day else 0

        self.assertEquals(count, len(body))
