import collections
from pyddns.plugins import Scanner

from pyddns.utils import is_external, sniff_interfaces, sniff_ipaddr_by_udp


class DefaultScanner(Scanner):

    def __init__(self):
        self.interfaces = sniff_interfaces()

    def load(self):
        address = collections.OrderedDict()

        return address
