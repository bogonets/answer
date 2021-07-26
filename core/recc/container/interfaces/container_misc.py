# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class ContainerMisc(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def inside_container() -> bool:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_current_container_key() -> str:
        raise NotImplementedError
