# -*- coding: utf-8 -*-

from abc import ABCMeta
from typing import Optional
from recc.database.interfaces.db_base_interface import DbBaseInterface
from recc.database.query_utils import merge_queries


class DbBase(DbBaseInterface, metaclass=ABCMeta):
    async def executes(
        self,
        *queries: str,
        timeout: Optional[float] = None,
    ) -> None:
        merged_single_query = merge_queries(*queries)
        await self.execute(merged_single_query, timeout=timeout)
