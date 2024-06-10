import collections
import socket
import psutil
import tldextract
from typing import OrderedDict
from typing import List

from netaddr import IPAddress
from netaddr import IPNetwork

CLASS_A = IPNetwork('10.0.0.0/255.0.0.0')
CLASS_B = IPNetwork('172.16.0.0/255.240.0.0')
CLASS_C = IPNetwork('192.168.0.0/255.255.0.0')
CLASS_D = IPNetwork('100.64.0.0/255.192.0.0')
INTERNALS = frozenset([CLASS_A, CLASS_B, CLASS_C, CLASS_D])


def is_external(address: str) -> bool:
    """address is external address"""
    for network in INTERNALS:
        if IPAddress(address) in network:
            return False
    return True


def sniff_ipaddr_by_udp() -> str:
    """sniff external ipaddress by udp"""
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8,8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return ""
    finally:
        if s:
            s.close()


def sniff_interfaces(*devices: str) -> OrderedDict[str, List[str]]:
    """get all address from interface"""
    interfaces = psutil.net_if_addrs()
    keys = [key for key in devices] if len(devices) > 0 \
        else [name for name in sorted(interfaces.keys()) if name != "lo"]
    address = collections.OrderedDict()
    for name in keys:
        ips = sorted([addr.address for addr in interfaces[name] if addr.family == 2])
        address[name] = ips
    return address


def split_domain(domain: str) -> (str, str):
    e = tldextract.extract(domain)
    return "%s.%s" % (e.domain, e.suffix), e.subdomain
