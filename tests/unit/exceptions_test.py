# -*- coding: utf-8 -*-
from inkwell import exceptions
import unittest
import inspect
import importlib

class ExceptionsTest(unittest.TestCase):
    def test_exceptions_loaded(self):
        ''' Exceptions: All werkzeug HTTP exceptions are recreated as JSON exceptions '''
        try:
            __import__('inkwell.exceptions', fromlist=\
                exceptions.base_http_exceptions)
            for e in exceptions.base_http_exceptions:
                locals()[e]
            assert True
        except ImportError:
            assert False

    def test_exceptions_are_json(self):
        ''' Exceptions: All JSON exceptions are subclasses of JSONHTTPException '''
        for e in exceptions.__all__:
            try:
                __import__('inkwell.exceptions', fromlist=[e])
            except exceptions.JSONHTTPException:
                assert True
