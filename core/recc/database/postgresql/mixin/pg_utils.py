# -*- coding: utf-8 -*-

from typing import Optional, Any, List, Dict, Iterable
from overrides import overrides
from recc.database.interfaces.db_utils import DbUtils
from recc.database.postgresql.mixin.pg_base import PgBase


class PgUtils(DbUtils, PgBase):
    """
    PostgreSQL utilities.
    """

    @overrides
    async def execute_query(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Any:
        return await self.execute(query, *args, timeout)

    @overrides
    async def execute_queries(
        self,
        queries: Iterable[str],
        timeout: Optional[float] = None,
    ) -> Any:
        return await self.executes(queries, timeout)

    @overrides
    async def fetch_rows(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        result = list()
        records = await self.fetch(query, *args, timeout=timeout)
        for record in records:
            result.append(dict(record))
        return result

    @overrides
    async def fetch_first_row(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        return dict(await self.fetch_row(query, *args, timeout=timeout))

    @overrides
    async def fetch_first_row_and_column(
        self,
        query: str,
        *args,
        column=0,
        timeout: Optional[float] = None,
    ) -> Any:
        return await self.fetch_val(query, *args, column=column, timeout=timeout)
