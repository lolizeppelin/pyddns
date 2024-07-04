import requests
import json
from typing import OrderedDict, List
from urllib.parse import urlencode
from oslo_config import cfg
from pyddns import utils
from pyddns.plugins import Notifier
from pyddns.config import dnspod_opts

CONF = cfg.CONF

cfg.CONF.register_opts(dnspod_opts, 'dnspod')

dnspod_headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "User-Agent": "python-pyddns/1.0.0"
}


def _check_code(result):
    code = int(result.get('status')['code'])
    if code != 1:
        raise ValueError('dnspod api code %d, msg %s' % (code, result.get('status')['message']))


class Dnspod(Notifier):

    def __init__(self):
        self.conf = cfg.CONF.dnspod
        self.timeout = cfg.CONF.timeout / 2
        self.domain, self.subdomain = utils.split_domain(self.conf.domain)

    def authenticate(self, timeout):
        return True

    def push(self, address: OrderedDict[str, List[str]]) -> bool:
        """
        匹配任意外网地址推送
        :return:
        """
        for address in address.values():
            for ip in address:
                if utils.is_external(ip):
                    self.update(ip)
                    return True
        return False

    def update(self, ipaddr):
        """
        https://www.dnspod.cn/docs/records.html#dns
        """
        if ipaddr == self.info_a['record']['value']:
            return None
        params = dict(
            format='json', lang='en', record_type='A',
            record_line_id="0",
            domain=self.domain, sub_domain=self.subdomain,
            record_id=self.conf.record_id,
            value=ipaddr,
            login_token='%d,%s' % (self.conf.id, self.conf.token)
        )
        res = requests.post(self.conf.api + '/Record.Ddns', headers=dnspod_headers,
                            data=urlencode(params), timeout=self.timeout)
        result = json.loads(res.text)
        _check_code(result)
        return result

    @property
    def info_a(self):
        params = dict(
            format='json', lang='en',
            domain=self.domain, record_id=self.conf.record_id,
            login_token='%d,%s' % (self.conf.id, self.conf.token)
        )
        res = requests.post(self.conf.api + '/Record.Info',
                            headers=dnspod_headers, data=urlencode(params),
                            timeout=self.timeout)
        result = res.json()
        _check_code(result)
        return result

    def list_domains(self):
        """
        query record from dnspod for sub domain
        :return:
        """
        params = dict(
            format='json', lang='en', record_type='A', record_line_id="0",
            domain=self.domain, sub_domain=self.subdomain,
            login_token='%d,%s' % (self.conf.id, self.conf.token)
        )
        res = requests.post(self.conf.api + '/Record.List',
                            headers=dnspod_headers, data=urlencode(params),
                            timeout=self.timeout)
        result = res.json()
        _check_code(result)
        return result
