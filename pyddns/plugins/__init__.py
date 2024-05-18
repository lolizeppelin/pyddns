from stevedore import driver
from abc import ABCMeta, abstractmethod
from typing import OrderedDict, List


class Scanner(metaclass=ABCMeta):
    @abstractmethod
    def load(self) -> OrderedDict[str, List[str]]:
        """
        获取外网地址
        :return:
        """


class Notifier(metaclass=ABCMeta):

    @abstractmethod
    def authenticate(self, timeout: int) -> bool:
        """
        登录认证
        :return:
        """

    @abstractmethod
    def push(self, address: OrderedDict[str, List[str]]) -> bool:
        """
        推送地址到外网
        :return:
        """


def load_notifier(plugin: str) -> Notifier:
    """
    :return:
    """
    mgr = driver.DriverManager('pyddns.notifier.plugins', plugin,
                               warn_on_missing_entrypoint=False)

    return mgr.driver()


def load_scaner(plugin: str) -> Scanner:
    """
    :return:
    """
    mgr = driver.DriverManager('pyddns.scaner.plugins', plugin,
                               warn_on_missing_entrypoint=False)

    return mgr.driver()
