# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# tests/test_cli.py

from __future__ import print_function
from __future__ import unicode_literals
import pytest
import io
import dns.name
import dns.rdataset
import dns.resolver

from dnszonetest.main import get_resolver
from dnszonetest.main import get_name_rdatasets
from dnszonetest.exceptions import NoZoneFileException


def test_get_resolver_return_resolver_with_given_nameserver():
    resolver = get_resolver('google-public-dns-a.google.com')
    assert isinstance(resolver, dns.resolver.Resolver)
    assert resolver.nameservers == ['8.8.8.8']


def test_get_resolver_return_resolver_with_no_given_nameserver():
    resolver = get_resolver(None)
    assert isinstance(resolver, dns.resolver.Resolver)
    assert resolver.nameservers == \
        dns.resolver.get_default_resolver().nameservers


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
    test if get_name_rdatasets(zonename, zonefile) returns
    dns.name.Name and dns.rdataset.Rdataset.
    '''
    name_rdatasets = get_name_rdatasets('example.com', zonefile)
    for name, rdataset in name_rdatasets:
        assert isinstance(name, dns.name.Name)
        assert isinstance(rdataset, dns.rdataset.Rdataset)


def test_get_name_rdatasets_raises_NoZoneFileException():
    '''
    test if get_name_rdatasets(zonename, zonefile) raises NoZoneFileException
    '''
    with pytest.raises(NoZoneFileException):
        get_name_rdatasets('example.com', '/path/to/non/existing/file')
