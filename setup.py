#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai et ts=4 sw=4 sts=4 fenc=UTF-8 ft=python

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

version = '0.2.1'


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
   'dnspython',
]

test_requirements = [
    'pytest',
    'tox',
]

setup(
    name='dnszonetest',
    version=version,
    description='Dnszonetest tests a DNS zone file agaist a given name '
    'server.',
    long_description=readme + '\n\n' + history,
    author='Maarten Diemel',
    author_email='maarten@maartendiemel.nl',
    url='https://github.com/maartenq/dnszonetest',
    packages=[
        'dnszonetest',
    ],
    package_dir={'dnszonetest':
                 'dnszonetest'},
    entry_points={
        'console_scripts': [
            'dnszonetest = dnszonetest.cli:main',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license='ISCL',
    zip_safe=False,
    keywords='dnszonetest',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    cmdclass={'test': PyTest},
    tests_require=test_requirements
)
