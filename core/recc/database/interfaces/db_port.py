# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional

from recc.database.struct.port import Port, SockType


class DbPort(metaclass=ABCMeta):
    """
    Database port interface.
    """

    @abstractmethod
    async def insert_port(
        self,
        number: int,
        sock: SockType,
        ref_uid: Optional[int] = None,
        ref_category: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_port_by_number(
        self,
        number: int,
        sock: SockType,
        ref_uid: Optional[int] = None,
        ref_category: Optional[str] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_port_by_number_and_sock(self, number: int, sock: SockType) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_port_by_number_and_sock(self, number: int, sock: SockType) -> Port:
        raise NotImplementedError

    @abstractmethod
    async def select_port_all(self) -> List[Port]:
        raise NotImplementedError

    @abstractmethod
    async def select_port_by_ref_uid_and_ref_category(
        self, ref_uid: int, ref_category: str
    ) -> List[Port]:
        raise NotImplementedError

    @abstractmethod
    async def select_port_number_all(self) -> List[int]:
        raise NotImplementedError
