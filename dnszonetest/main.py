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
from dnszonetest.exceptions import (
    UnableToResolveNameServerException,
    NoZoneFileException,
)

logger = logging.getLogger(__name__)


def get_resolver(nameserver):
    '''
    Return a resolver
    :param str nameserver: FQDN or IP nummer of name server.
    '''
    if nameserver is None:
        # system configured nameservers
        resolver = dns.resolver.get_default_resolver()
    else:
        # user defined nameserver
        resolver = dns.resolver.Resolver(configure=False)
        try:
            nameserver_ips = socket.gethostbyname_ex(nameserver)[2]
        except socket.gaierror as err:
            raise UnableToResolveNameServerException(
                'Unable to resolve nameserver "{0}". {1}'.format(
                    nameserver,
                    err
                )
            )
        else:
            resolver = dns.resolver.Resolver(configure=False)
            resolver.nameservers = nameserver_ips
    return resolver


def get_name_rdatasets(zonename, zonefile):
    '''
    Reads records from zone file.

    :param str zonename: Zone name.
    :param str zonefile: Zone file name.
    :returns: generator which yields (name, rdataset) tuples for all rdatasets
    :rtype: generator
    '''
    try:
        zone = dns.zone.from_file(zonefile, origin=zonename, relativize=False)
    except IOError as err:
        raise NoZoneFileException('Unable to read zone file: {0}'.format(err))
    return zone.iterate_rdatasets()


def chkrecord(resolver, name, rdataset):
    '''
    Compares resolved rdataset from name with given resolver and given
    rdataset.

    :param instance Resolver: Zone name.
    :param str name: DNS name
    :returns: tuple of booleans
    :rtype: tuple
    '''
    ttl_match = False
    rdataset_match = False
    logger.info(
        'name: {0}\tradataset: {1}'.format(name, rdataset)
    )
    try:
        answer = resolver.query(name, rdataset.rdtype, rdataset.rdclass)
    except dns.resolver.NXDOMAIN:
        logger.info('NXDOMAIN')
    else:
        result = answer.rrset.to_rdataset()
        logger.info('query result: {0}'.format(result))
        rdataset_match = rdataset == result
        ttl_match = rdataset.ttl == result.ttl
    return rdataset_match, ttl_match


def dnszonetest(zonename, zonefile, nameserver=None, verbose=False,
                quiet=False, norec=False, ttl=False, ns=False, soa=False):
    '''
    API equivalent to using dnszonetest at the command line.

    :param str zonename: Zone name.
    :param str zonefile: Zone file name.
    :param bool nameserver: name server to use.
    :param bool verbose: verbose output.
    :param bool quiet: suppress output.
    :param bool norec: do not use recursion.
    :param bool ttl: include TTL field in comparison.
    :param bool ns: include NS records in comparison.
    :param bool soa: include SOA records in comparison.
    :returns: 0 when records from zone file correctly resolve against
        nameserver, 2 when not, 3 on errors.
    :rtype: int
    '''
    # Get name server's IP
    try:
        if nameserver is None:
            logger.info('Get IP number(s) of system resolvers')
        else:
            logger.info(
                'Get IP number(s) of name server {0}'.format(nameserver)
            )
        resolver = get_resolver(nameserver)
    except UnableToResolveNameServerException as err:
        logger.error(err)
        return 3
    logger.info('name server IP(s): {0}'.format(resolver.nameservers))
    # Get name, rdatasets from zone file
    try:
        name_rdatasets = get_name_rdatasets(zonename, zonefile)
    except NoZoneFileException as err:
        logger.error(err)
        return 3
    for name, rdataset in name_rdatasets:
        rdataset_match, ttl_match = chkrecord(resolver, name, rdataset)
        logger.info('Record matches: {0}'.format(rdataset_match))
        logger.info('TTL matches: {0}'.format(ttl_match))
    return 0
