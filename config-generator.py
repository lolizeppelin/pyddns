#! /usr/bin/env python
import os.path
from oslo_config import generator

path = os.path.dirname(__file__)
cfgs = (
    ['--namespace', 'pyddns', '--output-file', 'etc/pyddns/ddns.conf'],
    ['--namespace', 'pyddns.dnspod', '--output-file', 'etc/pyddns/plugins/dnspod.conf'],
)

os.chdir(path)

etc = os.path.join("etc", "pyddns")
if not os.path.exists(etc):
    os.makedirs(etc, mode=0o755)
if not os.path.exists(os.path.join(etc, "plugins")):
    os.makedirs(os.path.join(etc, "plugins"), mode=0o755)

for args in cfgs:
    generator.main(args)
