# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Optional, Any, Dict

REQUEST_METHOD_SET = "set"
REQUEST_METHOD_GET = "get"


class LamdaInterface(metaclass=ABCMeta):
    """
    Lamda interface.
    """

    @abstractmethod
    def request(self, method: str, key: str, value: Any = None, **options) -> Any:
        raise NotImplementedError

    @abstractmethod
    def init(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def valid(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def destroy(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, **kwargs) -> Optional[Dict[str, Any]]:
        raise NotImplementedError


class Lamda(LamdaInterface):
    """
    Empty Lamda class.
    """

    def request(self, method: str, key: str, value: Any = None, **options) -> Any:
        return None

    def init(self) -> None:
        return

    def valid(self) -> bool:
        return True

    def destroy(self) -> None:
        pass

    def run(self, **kwargs) -> Optional[Dict[str, Any]]:
        return dict()
