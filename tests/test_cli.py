# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# tests/test_cli.py

import pytest
from dnszonetest.cli import parse_args


def test_parse_args_empty():
    '''
    Test the long command-line arguments to dnszonetest.
    '''
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args_short():
    '''
    Test the short command-line arguments to dnszonetest.
    '''
    args = parse_args(
        [
            'hva.nl',
            '/var/named/hva.nl',
            '-v',
            '-q',
            '-d', 'ns.hva.nl',
            '-r',
            '-t',
            '-n',
            '-s',
        ]
    )
    assert vars(args) == {
        'zonename': 'hva.nl',
        'zonefile': '/var/named/hva.nl',
        'verbose': True,
        'quiet': True,
        'version': False,
        'nameserver': 'ns.hva.nl',
        'norec': True,
        'ttl': True,
        'ns': True,
        'soa': True
    }


def test_parse_args_long():
    '''
    Test the long command-line arguments to dnszonetest.
    '''
    args = parse_args(
        [
            'hva.nl',
            '/var/named/hva.nl',
            '--verbose',
            '--quiet',
            '--nameserver', 'ns.hva.nl',
            '--norec',
            '--ttl',
            '--ns',
            '--soa',
        ]
    )
    assert vars(args) == {
        'zonename': 'hva.nl',
        'zonefile': '/var/named/hva.nl',
        'verbose': True,
        'quiet': True,
        'version': False,
        'nameserver': 'ns.hva.nl',
        'norec': True,
        'ttl': True,
        'ns': True,
        'soa': True
    }


def test_parse_args_pos():
    '''
    Test the long command-line arguments to dnszonetest.
    '''
    args = parse_args(
        [
            'hva.nl',
            '/var/named/hva.nl',
        ]
    )
    assert vars(args) == {
        'zonename': 'hva.nl',
        'zonefile': '/var/named/hva.nl',
        'verbose': False,
        'quiet': False,
        'version': False,
        'nameserver': None,
        'norec': False,
        'ttl': False,
        'ns': False,
        'soa': False,
    }
