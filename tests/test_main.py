# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# tests/test_cli.py

from __future__ import print_function
from __future__ import unicode_literals
import io
import pytest
import dns.name
import dns.rdataset
import dns.resolver
import dns.zone
import sys
from dnszonetest.main import DnsZoneTest
from dnszonetest.main import Record
from dnszonetest.exceptions import (
    NoZoneFileException,
    UnableToResolveNameServerException
)


if sys.version_info < (3,):
    ip_192_0_2_1 = b'192.0.2.1'
    ip_192_0_2_2 = b'192.0.2.2'
else:
    ip_192_0_2_1 = '192.0.2.1'
    ip_192_0_2_2 = '192.0.2.2'


@pytest.mark.parametrize(
    ('rdataset_file', 'rdataset_query', 'rdataset_match', 'ttl_match'),
    [
        (
            (1, 1, 28800, ip_192_0_2_1),
            (1, 1, 28800, ip_192_0_2_1),
            True,
            True,
        ),
        (
            (1, 1, 28800, ip_192_0_2_1),
            (1, 1, 28800, ip_192_0_2_2),
            False,
            True,
        ),
        (
            (1, 1, 28800, ip_192_0_2_1),
            (1, 1, 100, ip_192_0_2_1),
            True,
            False,
        ),
        (
            (1, 1, 28800, ip_192_0_2_1),
            (1, 1, 100, ip_192_0_2_2),
            False,
            False,
        ),
    ]
)
def test_record(rdataset_file, rdataset_query, rdataset_match, ttl_match):
    record = Record('www.example.com', dns.rdataset.from_text(*rdataset_file))
    record.rdataset_query = dns.rdataset.from_text(*rdataset_query)
    assert record.rdataset_match is rdataset_match
    assert record.ttl_match is ttl_match


@pytest.fixture(scope='module')
def zonefile(tmpdir_factory):
    zonefile = tmpdir_factory.mktemp('data').join('example.com')
    with io.open(str(zonefile), 'w', encoding='utf-8') as fh:
        fh.write('''$ORIGIN example.com.
$TTL 8h
example.com.  IN  SOA   ns.example.com. username.example.com. (
    2001052542
    1d
    2h
    4w
    1h
    )
example.com.  IN  NS    ns
example.com.  IN  NS    ns.somewhere.example.
example.com.  IN  MX    10 mail.example.com.
@             IN  MX    20 mail2.example.com.
@             IN  MX    50 mail3
example.com.  IN  A     192.0.2.1
IN  AAAA  2001:db8:10::1
ns            IN  A     192.0.2.2
IN  AAAA  2001:db8:10::2
www           IN  CNAME example.com.
wwwtest       IN  CNAME www
mail          IN  A     192.0.2.3
mail2         IN  A     192.0.2.4
mail3         IN  A     192.0.2.5''')
    return str(zonefile)


@pytest.fixture(scope='module')
def dzt(zonefile):
    '''
    DnsZoneTest instance with no given nameserver.
    '''
    return DnsZoneTest('example.com', zonefile)


@pytest.fixture(scope='module')
def dzt_ns(zonefile):
    '''
    DnsZoneTest instance with given nameserver.
    '''
    return DnsZoneTest('example.com', zonefile,
                       'google-public-dns-a.google.com')


def test_dzt_get_resolver_return_resolver_with_no_given_nameserver(dzt):
    dzt.get_resolver()
    assert isinstance(dzt.resolver, dns.resolver.Resolver)
    assert dzt.resolver.nameservers ==  \
        dns.resolver.get_default_resolver().nameservers


def test_dzt_get_resolver_return_resolver_with_given_nameserver(dzt_ns):
    dzt_ns.get_resolver()
    assert isinstance(dzt_ns.resolver, dns.resolver.Resolver)
    assert dzt_ns.resolver.nameservers == ['8.8.8.8']


def test_get_resolver_raises_UnableToResolveNameServerException():
    '''
    test if get_resolver('non.existing.nameserver') raises
    UnableToResolveNameServerException
    '''
    dzt = DnsZoneTest('example.com', 'example.com', 'non.existing.nameserver')
    with pytest.raises(UnableToResolveNameServerException):
        dzt.get_resolver()


def test_dzt_get_zone_from_file(dzt):
    dzt.get_zone_from_file()
    assert isinstance(dzt.zone_from_file, dns.zone.Zone)


def test_dzt_get_zone_from_file_raises_NoZoneFileException():
    dzt = DnsZoneTest('example.com', '/path/to/non/existing/zone/file')
    with pytest.raises(NoZoneFileException):
        dzt.get_zone_from_file()


def test_dzt_query(dzt, monkeypatch):
    class Rrset(object):
        def __init__(self, answer):
            self.answer = answer

        def to_rdataset(self):
            return dns.rdataset.from_text(*self.answer)

    class Answer(object):
        def __init__(self, answer):
            self.rrset = Rrset(answer)

    class Resolver(object):
        def __init__(self, answer):
            self.answer = answer

        def query(self, name, rdtype, rdclass):
            return Answer(self.answer)

    rdataset = (1, 1, 28800, ip_192_0_2_1)
    record = Record('example.com', dns.rdataset.from_text(*rdataset))
    monkeypatch.setattr(dzt, 'resolver', Resolver(rdataset))
    dzt.query(record)
    assert record.rdataset_query == dns.rdataset.from_text(*rdataset)


def test_dzt_query_raise_NXDOMAIN(dzt, monkeypatch):
    class Resolver(object):
        def query(self, name, rdtype, rdclass):
            raise dns.resolver.NXDOMAIN

    rdataset = (1, 1, 28800, ip_192_0_2_1)
    record = Record('example.com', dns.rdataset.from_text(*rdataset))
    monkeypatch.setattr(dzt, 'resolver', Resolver())
    dzt.query(record)
    assert record.rdataset_query is None
