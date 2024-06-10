import json
import os
import sys
import signal
import threading
import logging
import collections

from oslo_config import cfg

from typing import OrderedDict, List

from .plugins import Scanner
from .plugins import Notifier


def kill(signo, frame):
    logging.error("timeout, process suicide now")
    sys.exit(1)


class SignalHandler(object):
    """Systemd TimeoutStartSec"""

    IGNORE = frozenset(['SIG_DFL', 'SIG_IGN'])

    def __init__(self):
        self._signals_by_name = dict((name, getattr(signal, name))
                                     for name in dir(signal)
                                     if name.startswith("SIG")
                                     and name not in self.IGNORE)

    def handle_signal(self, handle):
        for signame in ('SIGTERM', 'SIGHUP', 'SIGINT'):
            signo = self._signals_by_name[signame]
            signal.signal(signo, handle)


class Ddns:

    def __init__(self, path, scaner: Scanner, notifier: Notifier):
        self.file = os.path.join(path, "dns.json")
        self.scaner = scaner
        self.notifier = notifier

        # timer for exit
        SignalHandler().handle_signal(kill)
        timer = threading.Timer(cfg.CONF.timeout, lambda: sys.exit(1))
        timer.daemon = True
        timer.start()

    def flush(self, address: OrderedDict[str, List[str]]):
        """flush address to state file"""
        buff = json.dumps(address)
        with open(self.file, 'w') as f:
            f.write(buff)

    @property
    def last(self) -> OrderedDict[str, List[str]] | None:
        """last address"""
        if not os.path.exists(self.file):
            return None
        with open(self.file, 'r') as f:
            return json.loads(f.read(), object_pairs_hook=collections.OrderedDict)

    def run(self):
        try:
            self.notifier.authenticate(cfg.CONF.timeout / 2)
            address = self.scaner.load()
            if not address:
                logging.warning("address not found from scaner %s", cfg.CONF.scaner)
                return
            if not cfg.CONF.force and self.last == address:
                logging.debug("address not change")
                return
            logging.debug("try push address")
            if self.notifier.push(address):
                logging.info("address pushed")
                # push success, flush address
                self.flush(address)
        except Exception:
            logging.exception("run ddns failed")
            sys.exit(1)
