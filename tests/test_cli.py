# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# tests/test_cli.py

from __future__ import print_function
from __future__ import unicode_literals
import pytest
import logging
from dnszonetest import cli


def test_parse_args_empty():
    '''
    Test the long command-line arguments to dnszonetest.
    '''
    with pytest.raises(SystemExit):
        cli.parse_args([])


def test_parse_args_short():
    '''
    Test the short command-line arguments to dnszonetest.
    '''
    args = cli.parse_args(
        [
            'example.com',
            '/var/named/zone/example.com',
            '-v',
            '-q',
            '-d', 'ns.example.com',
            '-r',
            '-t',
            '-n',
            '-s',
        ]
    )
    assert vars(args) == {
        'zonename': 'example.com',
        'zonefile': '/var/named/zone/example.com',
        'verbose': True,
        'quiet': True,
        'nameserver': 'ns.example.com',
        'no_recursion': True,
        'compare_ttl': True,
        'compare_ns': True,
        'compare_soa': True
    }


def test_parse_args_long():
    '''
    Test the long command-line arguments to dnszonetest.
    '''
    args = cli.parse_args(
        [
            'example.com',
            '/var/named/example.com',
            '--verbose',
            '--quiet',
            '--nameserver', 'ns.example.com',
            '--norec',
            '--ttl',
            '--ns',
            '--soa',
        ]
    )
    assert vars(args) == {
        'zonename': 'example.com',
        'zonefile': '/var/named/example.com',
        'verbose': True,
        'quiet': True,
        'nameserver': 'ns.example.com',
        'no_recursion': True,
        'compare_ttl': True,
        'compare_ns': True,
        'compare_soa': True
    }


def test_parse_args_pos():
    '''
    Test the long command-line arguments to dnszonetest.
    '''
    args = cli.parse_args(
        [
            'example.com',
            '/var/named/zone/example.com',
        ]
    )
    assert vars(args) == {
        'zonename': 'example.com',
        'zonefile': '/var/named/zone/example.com',
        'verbose': False,
        'quiet': False,
        'nameserver': None,
        'no_recursion': False,
        'compare_ttl': False,
        'compare_ns': False,
        'compare_soa': False,
    }


@pytest.mark.parametrize(
    ('verbose', 'quiet', 'log_level'),
    [
        (True, True, logging.DEBUG),
        (True, False, logging.DEBUG),
        (False, False, logging.INFO),
        (False, True, logging.CRITICAL),

    ]
)
def test_setup_logging_level(verbose, quiet, log_level):
    cli.setup_logging(verbose, quiet)
    logger = logging.getLogger()
    print(logger.handlers)
    assert logger.handlers[0].level == log_level
