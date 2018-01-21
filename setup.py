#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path) as f:
        return f.read()


setup(
    name='pytest-pspec',
    version='0.0.1',
    description='A rspec format reporter for Python ptest',
    long_description=read('README.rst'),
    author='Gowtham Sai',
    author_email='hello@gowtham-sai.com',
    url='https://github.com/gowtham-sai/pytest-pspec',
    keywords='pytest pspec test report bdd rspec',
    install_requires=[
        'pytest>=3.0.0',
        'six>=1.11.0',
    ],
    packages=['pytest_pspec'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'pspec = pytest_pspec.plugin',
        ],
    },
)
