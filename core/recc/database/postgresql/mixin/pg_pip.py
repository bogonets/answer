# -*- coding: utf-8 -*-

from typing import List
from overrides import overrides
from recc.database.struct.pip import Pip
from recc.database.interfaces.db_pip import DbPip
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.pip import (
    INSERT_PIP,
    DELETE_PIP_BY_DOMAIN_AND_NAME,
    SELECT_PIP_BY_DOMAIN_AND_NAME,
)


class PgPip(DbPip, PgBase):
    @overrides
    async def insert_pip(
        self,
        domain: str,
        name: str,
        file: str,
        hash_method: str,
        hash_value: str,
    ) -> None:
        await self.execute(INSERT_PIP, domain, name, file, hash_method, hash_value)

    @overrides
    async def delete_pip_by_domain_and_name(self, domain: str, name: str) -> None:
        await self.execute(DELETE_PIP_BY_DOMAIN_AND_NAME, domain, name)

    @overrides
    async def select_pip_by_domain_and_name(self, domain: str, name: str) -> List[Pip]:
        return await self.rows(Pip, SELECT_PIP_BY_DOMAIN_AND_NAME, domain, name)
