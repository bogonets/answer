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
        group_uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        task_uid: Optional[int] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow().astimezone(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_port_description_by_number(
        self, number: int, description: str, updated_at=datetime.utcnow().astimezone()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_port_extra_by_number(
        self, number: int, extra: Any, updated_at=datetime.utcnow().astimezone()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_port_by_number(
        self,
        number: int,
        group_uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        task_uid: Optional[int] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow().astimezone(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_port_by_number(self, number: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_port_by_number(self, number: int) -> Port:
        raise NotImplementedError

    @abstractmethod
    async def select_port_by_group_uid(self, group_uid: int) -> List[Port]:
        raise NotImplementedError

    @abstractmethod
    async def select_port_by_project_uid(self, project_uid: int) -> List[Port]:
        raise NotImplementedError

    @abstractmethod
    async def select_port_by_task_uid(self, task_uid: int) -> List[Port]:
        raise NotImplementedError

    @abstractmethod
    async def select_ports(self) -> List[Port]:
        raise NotImplementedError
