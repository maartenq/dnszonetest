#!/usr/bin/env python
# setup.py
# -*- coding: utf-8 -*-
# vim: ai et ts=4 sw=4 sts=4 fenc=UTF-8 ft=python

import sys
from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'dnspython',
]

# Add Python 2.6-specific dependencies
if sys.version_info[:2] < (2, 7):
        requirements.append('argparse')

test_requirements = [
    'pytest>=3.3.0',
    'pytest-cov>=2.5.1',
    'tox>=2.9.1',
]

setup(
    name='dnszonetest',
    version='1.2.0',
    description='DNS Zone Test tests a DNS zone file agaist a given name '
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
    license="ISC license",
    zip_safe=False,
    keywords='dnszonetest',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
