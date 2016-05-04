# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# tests/test_cli.py

from __future__ import print_function
from __future__ import unicode_literals
import io
import pytest
import six
import dns.name
import dns.rdataset
import dns.resolver

from dnszonetest.main import get_resolver
from dnszonetest.main import get_name_rdatasets
from dnszonetest.main import chkrecord
from dnszonetest.exceptions import (
    NoZoneFileException,
    UnableToResolveNameServerException
)

if six.PY2:
    ip_192_0_2_1 = b'192.0.2.1'
    ip_192_0_2_2 = b'192.0.2.2'
else:
    ip_192_0_2_1 = '192.0.2.1'
    ip_192_0_2_2 = '192.0.2.2'


def test_get_resolver_return_resolver_with_given_nameserver():
    resolver = get_resolver('google-public-dns-a.google.com')
    assert isinstance(resolver, dns.resolver.Resolver)
    assert resolver.nameservers == ['8.8.8.8']


def test_get_resolver_return_resolver_with_no_given_nameserver():
    resolver = get_resolver(None)
    assert isinstance(resolver, dns.resolver.Resolver)
    assert resolver.nameservers == \
        dns.resolver.get_default_resolver().nameservers


def test_get_resolver_raises_UnableToResolveNameServerException():
    '''
    test if get_resolver('non.existing.nameserver') raises
    UnableToResolveNameServerException
    '''
    with pytest.raises(UnableToResolveNameServerException):
        get_resolver('non.existing.nameserver')


@pytest.fixture()
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


def test_get_name_rdatasets_returns_name_and_rdatasets(zonefile):
    '''
    Test if get_name_rdatasets(zonename, zonefile) returns
    dns.name.Name and dns.rdataset.Rdataset.
    '''
    name_rdatasets = get_name_rdatasets('example.com', zonefile)
    for name, rdataset in name_rdatasets:
        assert isinstance(name, dns.name.Name)
        assert isinstance(rdataset, dns.rdataset.Rdataset)


def test_get_name_rdatasets_raises_NoZoneFileException():
    '''
    Test if get_name_rdatasets(zonename, zonefile) raises NoZoneFileException
    '''
    with pytest.raises(NoZoneFileException):
        get_name_rdatasets('example.com', '/path/to/non/existing/file')


@pytest.mark.parametrize(
    ('input_rdataset', 'input_rdataset_answer', 'expected'),
    [
        (
            (1, 1, 28800, ip_192_0_2_1),
            (1, 1, 28800, ip_192_0_2_1),
            (True, True),
        ),
        (
            (1, 1, 28800, ip_192_0_2_1),
            (1, 1, 28800, ip_192_0_2_2),
            (False, True),
        ),
        (
            (1, 1, 28800, ip_192_0_2_1),
            (1, 1, 100, ip_192_0_2_1),
            (True, False),
        ),
        (
            (1, 1, 28800, ip_192_0_2_1),
            (1, 1, 100, ip_192_0_2_2),
            (False, False),
        ),
    ]
)
def test_chkrecord(input_rdataset, input_rdataset_answer, expected):
    '''
    Test if chkrecord(resolver, name, rdataset) returns matching rdatasets and
    ttl.
    '''
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

    assert chkrecord(
        Resolver(input_rdataset_answer),
        'example.com',
        dns.rdataset.from_text(*input_rdataset)
    ) == expected


def test_chkrecord_returns_when_NXDOMAIN():
    '''
    Test if chkrecord(resolver, name, rdataset) returns (False, False) when
    query raises NXDOMAIN.
    '''
    class Resolver(object):
        def query(self, name, rdtype, rdclass):
            raise dns.resolver.NXDOMAIN

    assert chkrecord(
        Resolver(),
        'example.com',
        dns.rdataset.from_text(1, 1, 28800, ip_192_0_2_1),
    ) == (False, False)
