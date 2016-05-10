#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai et ts=4 sw=4 sts=4 fenc=UTF-8 ft=python

'''
dnszonetest.main
-------------

Main dnszonetest
'''

from __future__ import print_function
from __future__ import unicode_literals

import logging
import socket

import dns.resolver
import dns.zone
import dns.rdatatype
import dns.flags
from dnszonetest.exceptions import (
    UnableToResolveNameServerException,
    NoZoneFileException,
)

logger = logging.getLogger(__name__)


class Record(object):
    def __init__(self, name, rdataset_file):
        self.name = name
        self.rdataset_file = rdataset_file
        self.rdataset_query = None

    @property
    def rdataset_match(self):
        return self.rdataset_file == self.rdataset_query

    @property
    def ttl_match(self):
        try:
            res = self.rdataset_file.ttl == self.rdataset_query.ttl
        except AttributeError as err:
            logger.info(err)
            res = None
        return res


class DnsZoneTest(object):
    '''
    API equivalent to using dnszonetest at the command line.

    :returns: 0 when records from zone file correctly resolve against
        nameserver, 2 when not, 3 on errors.
    '''
    def __init__(self, zonename, zonefile, nameserver=None, verbose=False,
                 quiet=False, no_recursion=False, compare_ttl=False,
                 compare_ns=False, compare_soa=False):
        '''
        :param str zonename: Zone name.
        :param str zonefile: Zone file name.
        :param bool nameserver: name server to use.
        :param bool verbose: verbose output.
        :param bool quiet: suppress output.
        :param bool no_recursion: do not use recursion.
        :param bool compare_ttl: include TTL field in comparison.
        :param bool compare_ns: include NS records in comparison.
        :param bool compare_soa: include SOA records in comparison.
        '''
        self.zonename = zonename
        self.zonefile = zonefile
        self.nameserver = nameserver
        self.verbose = verbose
        self.quiet = quiet
        self.no_recursion = no_recursion
        self.compare_ttl = compare_ttl
        self.compare_ns = compare_ns
        self.compare_soa = compare_soa
        self.resolver = None
        self.zone_from_file = None
        self.mismatch_ttl = 0
        self.mismatch_rdataset = 0
        self.errno = 3

    def get_resolver(self):
        '''
        Get Resolver object depending on self.nameserver
        '''
        if self.nameserver is None:
            logger.info('Get IP number(s) of system resolvers')
            self.resolver = dns.resolver.get_default_resolver()
        else:
            logger.info(
                'Get IP number(s) of name server %s',
                self.nameserver
            )
            self.resolver = dns.resolver.Resolver(configure=False)
            try:
                nameserver_ips = socket.gethostbyname_ex(
                    self.nameserver)[2]
            except socket.gaierror as err:
                raise UnableToResolveNameServerException(
                    'Unable to resolve nameserver "{0}". {1}'.format(
                        self.nameserver,
                        err
                    )
                )
            else:
                self.resolver = dns.resolver.Resolver(configure=False)
                self.resolver.nameservers = nameserver_ips
                if self.no_recursion:
                    self.resolver.set_flags(dns.flags.RD)
        logger.info('name server IP(s): {0}'.format(self.resolver.nameservers))

    def get_zone_from_file(self):
        '''
        Read records from zone file. Sets self.zone_from_file
        '''
        try:
            self.zone_from_file = dns.zone.from_file(
                self.zonefile,
                origin=self.zonename,
                relativize=False
            )
        except IOError as err:
            raise NoZoneFileException(
                'Unable to read zone file: {0}'.format(err)
            )

    def query(self, record):
        try:
            answer = self.resolver.query(
                record.name,
                record.rdataset_file.rdtype,
                record.rdataset_file.rdclass
            )
        except dns.resolver.NXDOMAIN:
            logger.info('NXDOMAIN')
        else:
            record.rdataset_query = answer.rrset.to_rdataset()
            logger.info('query result: {0}'.format(record.rdataset_query))

    def compare_rdatasets(self):
        for name, rdataset_file in self.zone_from_file.iterate_rdatasets():
            if not self.compare_ns and \
                    rdataset_file.rdtype == dns.rdatatype.NS:
                continue
            if not self.compare_soa and \
                    rdataset_file.rdtype == dns.rdatatype.SOA:
                continue
            record = Record(name, rdataset_file)
            self.query(record)
            if self.compare_ttl and record.rdataset_query is not None:
                if not record.ttl_match:
                    self.mismatch_ttl += 1
                    logger.warning(
                        '%s TTL: %s',
                        record.name,
                        record.rdataset_file.ttl
                    )
                    logger.warning(
                        '%s TTL : %s',
                        record.name,
                        record.rdataset_query.ttl
                    )
            if not record.rdataset_match:
                self.mismatch_rdataset += 1
                logger.warning(
                    '%s in zonefile: %s',
                    record.name,
                    record.rdataset_file
                )
                logger.warning(
                    '%s from query : %s',
                    record.name,
                    record.rdataset_query
                )
        if self.mismatch_ttl > 0 or self.mismatch_rdataset > 0:
            self.errno = 1
        else:
            self.errno = 0

    def compare(self):
        self.get_resolver()
        self.get_zone_from_file()
        self.compare_rdatasets()
