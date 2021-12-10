# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.port import Port


class DbPort(metaclass=ABCMeta):
    """
    Database port interface.
    """

    @abstractmethod
    async def insert_port(
        self,
        number: int,
        ref_uid: Optional[int] = None,
        ref_category: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_port_description_by_number(
        self,
        number: int,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_port_extra_by_number(
        self,
        number: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_port_by_number(
        self,
        number: int,
        ref_uid: Optional[int] = None,
        ref_category: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_port_by_number(self, number: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_port_by_number(self, number: int) -> Port:
        raise NotImplementedError

    @abstractmethod
    async def select_ports(self) -> List[Port]:
        raise NotImplementedError
