# -*- coding: utf-8 -*-
import inkwell
import unittest
import json
import random
from flask import json
from tests import fixtures
from werkzeug.test import Client

class ArchiveTest(unittest.TestCase):
    def test_bad_accept_header(self):
        response = fixtures.client.get('/inkwell/')
        self.assertEquals(response.status_code, 400)

    def test_root(self):
        response = fixtures.client.get('/inkwell/', 
            headers={'Accept': 'application/json'})
        self.assertEquals(response.status_code, 200)
        body = json.loads(response.data)
        self.assertEquals(len(body), len(fixtures.valid_files))

    def test_valid_year(self):
        year = random.choice(fixtures.dates.keys())

        response = fixtures.client.get("/inkwell/{}".format(year), 
            headers={'Accept': 'application/json'})

        self.assertEquals(response.status_code, 200)
        body = json.loads(response.data)

        count = 0
        for month in fixtures.dates[year]:
            count += len(fixtures.dates[year][month])

        self.assertEquals(count, len(body))

    def test_valid_year_and_month(self):
        year  = random.choice(fixtures.dates.keys())
        month = random.choice(fixtures.dates[year].keys())

        response = fixtures.client.get("/inkwell/{}/{}".format(year, month), 
            headers={'Accept': 'application/json'})

        self.assertEquals(response.status_code, 200)
        body = json.loads(response.data)

        self.assertEquals(len(fixtures.dates[year][month]), len(body))

    def test_valid_year_month_and_day(self):
        year  = random.choice(fixtures.dates.keys())
        month = random.choice(fixtures.dates[year].keys())
        day   = random.choice(fixtures.dates[year][month])

        response = fixtures.client.get("/inkwell/{}/{}/{}".format(
            year, month, day), headers={'Accept': 'application/json'})

        self.assertEquals(response.status_code, 200)
        body = json.loads(response.data)

        count = 0
        for d in fixtures.dates[year][month]:
            count += 1 if d == day else 0

        self.assertEquals(count, len(body))

    def test_invalid_year(self):
        response = fixtures.client.get('/inkwell/9999', 
            headers={'Accept': 'application/json'})

        body = json.loads(response.data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(len(body['description']['year']), 1)
        self.assertEquals(body['description']['year'][0], '9999 is not a valid year')

    def test_invalid_year_and_month(self):
        response = fixtures.client.get('/inkwell/9999/99', 
            headers={'Accept': 'application/json'})

        body = json.loads(response.data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(len(body['description']['year']), 1)
        self.assertEquals(body['description']['year'][0], '9999 is not a valid year')

        self.assertEquals(len(body['description']['month']), 1)
        self.assertEquals(body['description']['month'][0], '99 is not a valid month')

    def test_invalid_year_month_and_day(self):
        response = fixtures.client.get('/inkwell/9999/99/99', 
            headers={'Accept': 'application/json'})

        body = json.loads(response.data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(len(body['description']['year']), 1)
        self.assertEquals(body['description']['year'][0], '9999 is not a valid year')

        self.assertEquals(len(body['description']['month']), 1)
        self.assertEquals(body['description']['month'][0], '99 is not a valid month')

        self.assertEquals(len(body['description']['day']), 1)
        self.assertEquals(body['description']['day'][0], '99 is not a valid day')
