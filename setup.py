from __future__ import unicode_literals

from setuptools import setup, find_packages

setup(
    name='django-reuse',
    version='.'.join(map(str, __import__('reuse').__version__)),
    description='Yet another collection of components commonly used for Django sites',
    author='Markus Kaiserswerth',
    author_email='github@sensun.org',
    url='https://github.com/mkai/django-reuse',
    packages=find_packages(),
    install_requires=['django'],
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    license="MIT",
)
