#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai et ts=4 sw=4 sts=4 fenc=UTF-8 ft=python

'''
dnszonetest.cli
-------------

Main dnszonetest CLI.
'''

from __future__ import print_function
from __future__ import unicode_literals
import argparse
import logging
import logging.handlers
import sys

from dnszonetest.main import dnszonetest

logger = logging.getLogger(__name__)


def setup_logging(verbose, quiet):
    '''
    Sets up logging.

    :param bool verbose: verbose output.
    :param bool quiet: suppress output.
    '''
    # Root logger
    logger = logging.getLogger()
    # Clear all handlers
    [handler.close() for handler in logger.handlers]
    logger.handlers = []
    # Root logger logs all
    logger.setLevel(logging.DEBUG)
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter(fmt='%(levelname)-10s%(message)s',)
        # logging.Formatter(fmt='%(message)s',)
    )
    if verbose:
        log_level = logging.INFO
    elif quiet:
        log_level = logging.CRITICAL
    else:
        log_level = logging.WARNING
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)


def parse_args(args):
    '''
    Parse the command-line arguments to dnszonetest.

    :param list args: list of arguments (example: sys.argv[1:])

    :returns: argparse.Namespace
    :rtype: argparse.Namespace
    '''
    parser = argparse.ArgumentParser(
        prog='dnszonetest',
        description='DNS Zone Test',
    )
    parser.add_argument(
        'zonename',
        help='zone name',
    )
    parser.add_argument(
        'zonefile',
        help='zone file',
    )
    parser.add_argument(
        '-d',
        '--nameserver',
        help='DNS server to query.',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Show verbose info (level DEBUG).',
    )
    parser.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='No output.',
    )
    parser.add_argument(
        '-r',
        '--norec',
        action='store_true',
        help='Set No Recursion flag.',
    )
    parser.add_argument(
        '-t',
        '--ttl',
        action='store_true',
        help='Compare TTL values.',
    )
    parser.add_argument(
        '-n',
        '--ns',
        action='store_true',
        help='Compare NS records.',
    )
    parser.add_argument(
        '-s',
        '--soa',
        action='store_true',
        help='Compare SOA records.',
    )
    return parser.parse_args(args)


def main():
    '''
    Entry point for the package defined in setup.py.

    :returns: 0 when records from zone file correctly resolve against
        nameserver, 2 when not, 3 on errors.
    :rtype: int
    '''
    # Parse args
    args = parse_args(sys.argv[1:])
    # Setup basic logging
    setup_logging(args.verbose, args.quiet)
    logger.debug('Arguments: %s', args)
    return dnszonetest(
        args.zonename,
        args.zonefile,
        nameserver=args.nameserver,
        verbose=args.verbose,
        quiet=args.quiet,
        norec=args.norec,
        ttl=args.ttl,
        ns=args.ns,
        soa=args.soa,
    )
