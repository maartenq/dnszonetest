#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
   'dnspython',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='dnszonetest',
    version='0.1.0',
    description="Dnszonetest tests a DNS zone file agaist a given name server.",
    long_description=readme + '\n\n' + history,
    author="Maarten",
    author_email='@twaarten',
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
    license="ISCL",
    zip_safe=False,
    keywords='dnszonetest',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
