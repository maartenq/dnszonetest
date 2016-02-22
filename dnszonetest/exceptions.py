#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai et ts=4 sw=4 sts=4 fenc=UTF-8 ft=python

"""
dnszonetest.exceptions
-----------------------
All exceptions used in the Dnszonetest code base are defined here.
"""


class DnszonetestException(Exception):
    """
    Base exception class. All Dnszonetest-specific exceptions should subclass
    this class.
    """


class UnableToResolveNameServerException(DnszonetestException):
    """
    Raised nameserver IP number(s) could not be resolved.
    """


class NoZoneFileException(DnszonetestException):
    """
    Raised when zone file does not exist.
    """
