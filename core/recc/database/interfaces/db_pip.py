# -*- coding: utf-8 -*-

from typing import List
from abc import ABCMeta, abstractmethod
from recc.database.struct.pip import Pip


class DbPip(metaclass=ABCMeta):
    """
    Database pip interface.
    """

    @abstractmethod
    async def insert_pip(
        self,
        domain: str,
        name: str,
        file: str,
        hash_method: str,
        hash_value: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_pip_by_domain_and_name(self, domain: str, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_pip_by_domain_and_name(self, domain: str, name: str) -> List[Pip]:
        raise NotImplementedError

    @abstractmethod
    async def select_pip_all(self) -> List[Pip]:
        raise NotImplementedError
