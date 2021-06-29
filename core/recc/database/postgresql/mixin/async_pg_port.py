# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from recc.exception.recc_error import ReccNotFoundError
from recc.log.logging import recc_database_logger as logger
from recc.struct.port import Port
from recc.database.postgresql.mixin.async_pg_base import AsyncPgBase
from recc.database.postgresql.query.port import (
    INSERT_PORT,
    UPDATE_PORT_DESCRIPTION_BY_NUMBER,
    UPDATE_PORT_EXTRA_BY_NUMBER,
    DELETE_PORT_BY_NUMBER,
    SELECT_PORT_BY_NUMBER,
    SELECT_PORT_BY_GROUP_UID,
    SELECT_PORT_BY_PROJECT_UID,
    SELECT_PORT_BY_TASK_UID,
    SELECT_PORT_ALL,
    get_update_port_query_by_number,
)


class AsyncPgPort(AsyncPgBase):
    async def create_port(
        self,
        number: int,
        group_uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        task_uid: Optional[int] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        query = INSERT_PORT
        await self.execute(
            query,
            number,
            group_uid,
            project_uid,
            task_uid,
            description,
            extra,
            created_at,
        )
        params_msg = f"number={number}"
        logger.info(f"create_port({params_msg}) ok.")

    async def update_port_description_by_number(
        self, number: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PORT_DESCRIPTION_BY_NUMBER
        await self.execute(query, number, description, updated_at)
        params_msg = f"number={number}"
        logger.info(f"update_port_description_by_number({params_msg}) ok.")

    async def update_port_extra_by_number(
        self, number: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PORT_EXTRA_BY_NUMBER
        await self.execute(query, number, extra, updated_at)
        params_msg = f"number={number}"
        logger.info(f"update_port_extra_by_number({params_msg}) ok.")

    async def update_port_by_number(
        self,
        number: int,
        group_uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        task_uid: Optional[int] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        query, args = get_update_port_query_by_number(
            number=number,
            group_uid=group_uid,
            project_uid=project_uid,
            task_uid=task_uid,
            description=description,
            extra=extra,
            updated_at=updated_at,
        )
        await self.execute(query, *args)
        params_msg = f"number={number}"
        logger.info(f"update_port_by_number({params_msg}) ok.")

    async def delete_port_by_number(self, number: int) -> None:
        query = DELETE_PORT_BY_NUMBER
        await self.execute(query, number)
        params_msg = f"number={number}"
        logger.info(f"delete_port_by_number({params_msg}) ok.")

    async def get_port_by_number(self, number: int) -> Port:
        query = SELECT_PORT_BY_NUMBER
        row = await self.fetch_row(query, number)
        params_msg = f"number={number}"
        if not row:
            raise ReccNotFoundError(f"Not found widget: {params_msg}")
        assert len(row) == 7
        result = Port(**dict(row))
        result.number = number
        logger.info(f"get_port_by_number({params_msg}) ok.")
        return result

    async def get_port_by_group_uid(self, group_uid: int) -> List[Port]:
        result: List[Port] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PORT_BY_GROUP_UID
                async for row in conn.cursor(query, group_uid):
                    item = Port(**dict(row))
                    item.group_uid = group_uid
                    result.append(item)
        params_msg = f"group_uid={group_uid}"
        result_msg = f"{len(result)} port"
        logger.info(f"get_port_by_group_uid({params_msg}) -> {result_msg}")
        return result

    async def get_port_by_project_uid(self, project_uid: int) -> List[Port]:
        result: List[Port] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PORT_BY_PROJECT_UID
                async for row in conn.cursor(query, project_uid):
                    item = Port(**dict(row))
                    item.project_uid = project_uid
                    result.append(item)
        params_msg = f"project_uid={project_uid}"
        result_msg = f"{len(result)} port"
        logger.info(f"get_port_by_project_uid({params_msg}) -> {result_msg}")
        return result

    async def get_port_by_task_uid(self, task_uid: int) -> List[Port]:
        result: List[Port] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PORT_BY_TASK_UID
                async for row in conn.cursor(query, task_uid):
                    item = Port(**dict(row))
                    item.task_uid = task_uid
                    result.append(item)
        params_msg = f"task_uid={task_uid}"
        result_msg = f"{len(result)} port"
        logger.info(f"get_port_by_task_uid({params_msg}) -> {result_msg}")
        return result

    async def get_ports(self) -> List[Port]:
        result: List[Port] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PORT_ALL
                async for row in conn.cursor(query):
                    result.append(Port(**dict(row)))
        result_msg = f"{len(result)} port"
        logger.info(f"get_ports() -> {result_msg}")
        return result
