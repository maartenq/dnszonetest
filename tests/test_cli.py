# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# tests/test_cli.py

from __future__ import print_function
from __future__ import unicode_literals
import pytest
from dnszonetest.cli import parse_args
from dnszonetest.cli import main


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
        'norec': False,
        'ttl': False,
        'ns': False,
        'soa': False,
    }


def test_main(monkeypatch):
    monkeypatch.setattr(
        'sys.argv',
        ['dnszonetest', 'example.com', '/var/named/zone/example.com'],
    )
    assert main() == 0
