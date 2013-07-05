# -*- coding: utf-8 -*-
from inkwell import exceptions
import unittest
import inspect
import importlib

class ExceptionsTest(unittest.TestCase):
    def test_exceptions_are_json(self):
        ''' Exceptions: All JSON exceptions are subclasses of JSONHTTPException '''
        for e in exceptions.__all__:
            try:
                klass = getattr(exceptions, e)
                raise klass('foo')
            except exceptions.JSONHTTPException as e:
                assert True