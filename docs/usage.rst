=====
Usage
=====

see `dnszonetest -h`::

    usage: dnszonetest [-h] [-d NAMESERVER] [-v] [-q] [-r] [-t] [-n] [-s]
                       zonename zonefile

    DNS Zone Test

    positional arguments:
      zonename              zone name
      zonefile              zone file

    optional arguments:
      -h, --help            show this help message and exit
      -d NAMESERVER, --nameserver NAMESERVER
                            DNS server to query.
      -v, --verbose         Show verbose info (level DEBUG).
      -q, --quiet           No output.
      -r, --norec           Set No Recursion flag.
      -t, --ttl             Compare TTL values.
      -n, --ns              Compare NS records.
      -s, --soa             Compare SOA records.
