import collections
from oslo_config import cfg
from pyddns.plugins import Scanner

from pyddns.utils import is_external, sniff_interfaces, sniff_ipaddr_by_udp


class DefaultScanner(Scanner):

    def __init__(self):
        if cfg.CONF.interfaces:
            self.interfaces = sniff_interfaces(*cfg.CONF.interfaces)
        else:
            self.interfaces = sniff_interfaces()

    def load(self):
        if not self.interfaces:
            raise ValueError("not address found")
        return self.interfaces


class UdpScanner(Scanner):

    def load(self):
        ip = sniff_ipaddr_by_udp()
        return collections.OrderedDict({"udp": [ip, ]})
