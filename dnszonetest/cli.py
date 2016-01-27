#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai et ts=4 sw=4 sts=4 fenc=UTF-8 ft=python

'''
dnszonetest.cli
-------------

Main dnszonetest CLI.
'''

import argparse
import logging
import logging.handlers
import sys
from . import __version__


logger = logging.getLogger(__name__)


def setup_logging(verbose):
    if verbose:
        log_level = logging.DEBUG
        log_format = logging.Formatter(fmt='%(levelname)-8s %(message)s',)
    else:
        log_level = logging.INFO
        log_format = logging.Formatter(fmt='%(message)s',)

    # Console Handler
    handler = logging.StreamHandler()
    handler.setFormatter(log_format)
    handler.setLevel(log_level)

    # Add to root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)


def parse_pcrunner_args(args):
    '''
    Parse the command-line arguments to dnszonetest.
    '''
    parser = argparse.ArgumentParser(
        prog='dnszonetest',
        description='DNS Zone Test',
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
        '--version',
        action='store_true',
        help='Show version',
    )
    parser.add_argument(
        '-d',
        '--nameserver',
        help='DNS server to query.',
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
    '''
    # Parse args
    args = parse_pcrunner_args(sys.argv[1:])

    # Version info
    if args.version:
        print(__version__)
        sys.exit(0)

    # Setup basic logging
    setup_logging(args.verbose)

    logger.debug('Arguments: %s', args)

if __name__ == '__main__':
    main()
