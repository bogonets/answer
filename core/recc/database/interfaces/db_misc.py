# -*- coding: utf-8 -*-

from datetime import datetime
from abc import ABCMeta, abstractmethod


class DbMisc(metaclass=ABCMeta):
    """
    Database miscellaneous interface.
    """

    @abstractmethod
    async def create_tables(self, created_at=datetime.utcnow()) -> None:
        raise NotImplementedError

    @abstractmethod
    async def drop_tables(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_cache(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_anonymous_group_uid(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_guest_permission_uid(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_reporter_permission_uid(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_operator_permission_uid(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_maintainer_permission_uid(self) -> int:
        raise NotImplementedError
