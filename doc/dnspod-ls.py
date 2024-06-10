#!/usr/bin/python3
import sys

from oslo_config import cfg
from pyddns.plugins.dnspod import Dnspod


def query():
    api = Dnspod()
    return api.list_domains()


def show(result):
    print(result)


def main():
    cfg.CONF(project='list-domains', description="list domains from dnspod",
             args=('--config-dir', '/etc/pyddns/plugins') if len(sys.argv) <= 1 else None)
    result = query()
    show(result)


if __name__ == '__main__':
    main()
