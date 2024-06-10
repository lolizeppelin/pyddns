from oslo_config import cfg

from .ddns import Ddns
from .config import ddns_opts
from .plugins import load_scaner, load_notifier

def load() -> Ddns:
    """
    :return:
    """
    cfg.CONF.register_opts(ddns_opts)
    cfg.CONF(project='ddns')
    return Ddns(cfg.CONF.storage,
                load_scaner(cfg.CONF.scaner),
                load_notifier(cfg.CONF.notifier))