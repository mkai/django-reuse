#!/usr/bin/env python

from __future__ import unicode_literals
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-reuse',
    version='.'.join(map(str, __import__('reuse').__version__)),
    description='Yet another collection of components commonly used for Django sites',
    author='Markus Kaiserswerth',
    author_email='github@sensun.org',
    url='https://github.com/mkai/django-reuse',
    packages=find_packages(exclude=['tests*']),
    install_requires=['Django'],
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
