#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from version import __version__

setup(
    name='inkwell',
    version=__version__,
    description='A tiny Git-powered blogging API.',
    author='Wilhelm Murdoch',
    author_email='wilhelm.murdoch@gmail.com',
    url='http://www.devilmayco.de/',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
          'Flask==0.10'
        , 'PyYaml==3.10'
        , 'Markdown==2.3.1'
        , 'python-dateutil==2.1'
    ],
    setup_requires=[
          'nose==1.1.2'
        , 'yanc==0.2.3'
        , 'mock==1.0.1'
    ]
)