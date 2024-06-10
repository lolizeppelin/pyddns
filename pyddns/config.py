import itertools
from oslo_config import cfg
from oslo_config import types

ddns_opts = [
    cfg.StrOpt('storage',
               default='/var/lib/pyddns',
               help='已推送地址缓存'),
    cfg.IntOpt('timeout',
               short='t',
               min=10, max=65,
               default=30,
               help='进程最大执行时间'),
    cfg.BoolOpt('force',
                default=False,
                help='地址不变的情况下也推送'),
    cfg.StrOpt('notifier',
               default='dnspod',
               help='地址推送插件(默认ddns)'),
    cfg.StrOpt('scaner',
               default='default',
               help='地址搜索插件'),
    cfg.ListOpt('interfaces',
                short='i',
                default=["ppp0"],
                item_type=types.String(),
                help='需要搜索的网卡名'),
]

dnspod_opts = [
    cfg.StrOpt('api',
               default='https://dnsapi.cn',
               help='Dnspod api address'),
    cfg.IntOpt('id',
               required=True,
               help='Dnspod api token id'),
    cfg.StrOpt('token',
               secret=True,
               help='Dnspod api token'),
    cfg.HostnameOpt('domain',
                    required=True,
                    help='full sub domain on dnspod, e.g nas.my-domain.com'),
    cfg.IntOpt('record_id',
               required=True,
               help='Sub domain A record id on dnspod'),
]


def list_opts():
    return [
        ('DEFAULT', itertools.chain(ddns_opts)),
    ]


def list_dnspod_opts():
    return [
        ('dnspod', itertools.chain(dnspod_opts)),
    ]
