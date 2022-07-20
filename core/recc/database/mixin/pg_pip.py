# -*- coding: utf-8 -*-

from typing import List

from recc.database.mixin._pg_base import PgBase
from recc.database.query.pip import (
    DELETE_PIP_BY_DOMAIN_AND_NAME,
    INSERT_PIP,
    SELECT_PIP_ALL,
    SELECT_PIP_BY_DOMAIN_AND_NAME,
)
from recc.packet.pip import Pip


class PgPip(PgBase):
    async def insert_pip(
        self,
        domain: str,
        name: str,
        file: str,
        hash_method: str,
        hash_value: str,
    ) -> None:
        await self.execute(INSERT_PIP, domain, name, file, hash_method, hash_value)

    async def delete_pip_by_domain_and_name(self, domain: str, name: str) -> None:
        await self.execute(DELETE_PIP_BY_DOMAIN_AND_NAME, domain, name)

    async def select_pip_by_domain_and_name(self, domain: str, name: str) -> List[Pip]:
        return await self.rows(Pip, SELECT_PIP_BY_DOMAIN_AND_NAME, domain, name)

    async def select_pip_all(self) -> List[Pip]:
        return await self.rows(Pip, SELECT_PIP_ALL)
