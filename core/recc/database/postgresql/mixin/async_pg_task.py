# -*- coding: utf-8 -*-

from typing import Optional, Any, List, Dict
from datetime import datetime
from recc.exception.recc_error import ReccNotFoundError
from recc.log.logging import recc_database_logger as logger
from recc.struct.task import Task
from recc.database.postgresql.mixin.async_pg_base import AsyncPgBase
from recc.database.postgresql.query.task import (
    INSERT_TASK,
    UPDATE_TASK_DESCRIPTION_BY_UID,
    UPDATE_TASK_DESCRIPTION_BY_PROJECT_UID_AND_NAME,
    UPDATE_TASK_EXTRA_BY_UID,
    UPDATE_TASK_EXTRA_BY_PROJECT_UID_AND_NAME,
    UPDATE_TASK_KEYS_BY_UID,
    UPDATE_TASK_KEYS_BY_PROJECT_UID_AND_NAME,
    DELETE_TASK_BY_UID,
    DELETE_TASK_BY_PROJECT_UID_AND_NAME,
    SELECT_TASK_BY_UID,
    SELECT_TASK_BY_PROJECT_ID_AND_NAME,
    SELECT_TASK_UID_BY_PROJECT_ID_AND_NAME,
    SELECT_TASK_BY_PROJECT_ID,
    SELECT_TASK_BY_FULLPATH,
    SELECT_TASK_UID_BY_FULLPATH,
    get_update_task_query_by_uid,
)


class AsyncPgTask(AsyncPgBase):
    async def create_task(
        self,
        project_uid: int,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        rpc_address: Optional[str] = None,
        auth_algorithm: Optional[str] = None,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        query = INSERT_TASK
        await self.execute(
            query,
            project_uid,
            name,
            description,
            extra,
            rpc_address,
            auth_algorithm,
            private_key,
            public_key,
            maximum_restart_count,
            numa_memory_nodes,
            base_image_name,
            publish_ports,
            created_at,
        )
        params_msg = f"project_uid={project_uid},name={name}"
        logger.info(f"create_task({params_msg}) ok.")

    async def update_task_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_TASK_DESCRIPTION_BY_UID
        await self.execute(query, uid, description, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_task_description_by_uid({params_msg}) ok.")

    async def update_task_description_by_name(
        self,
        project_uid: int,
        name: str,
        description: str,
        updated_at=datetime.utcnow(),
    ) -> None:
        query = UPDATE_TASK_DESCRIPTION_BY_PROJECT_UID_AND_NAME
        await self.execute(query, project_uid, name, description, updated_at)
        params_msg = f"project_uid={project_uid},name={name}"
        logger.info(f"update_task_description_by_name({params_msg}) ok.")

    async def update_task_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_TASK_EXTRA_BY_UID
        await self.execute(query, uid, extra, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_task_extra_by_uid({params_msg}) ok.")

    async def update_task_extra_by_name(
        self, project_uid: int, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_TASK_EXTRA_BY_PROJECT_UID_AND_NAME
        await self.execute(query, project_uid, name, extra, updated_at)
        params_msg = f"project_uid={project_uid},name={name}"
        logger.info(f"update_task_extra_by_name({params_msg}) ok.")

    async def update_task_keys_by_uid(
        self,
        uid: int,
        auth_algorithm: str,
        private_key: str,
        public_key: str,
        updated_at=datetime.utcnow(),
    ) -> None:
        query = UPDATE_TASK_KEYS_BY_UID
        await self.execute(
            query, uid, auth_algorithm, private_key, public_key, updated_at
        )
        params_msg = f"uid={uid}"
        logger.info(f"update_task_keys_by_uid({params_msg}) ok.")

    async def update_task_keys_by_name(
        self,
        project_uid: int,
        name: str,
        auth_algorithm: str,
        private_key: str,
        public_key: str,
        updated_at=datetime.utcnow(),
    ) -> None:
        query = UPDATE_TASK_KEYS_BY_PROJECT_UID_AND_NAME
        await self.execute(
            query,
            project_uid,
            name,
            auth_algorithm,
            private_key,
            public_key,
            updated_at,
        )
        params_msg = f"project_uid={project_uid},name={name}"
        logger.info(f"update_task_keys_by_name({params_msg}) ok.")

    async def update_task_by_uid(
        self,
        uid: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        rpc_address: Optional[str] = None,
        auth_algorithm: Optional[str] = None,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        query, args = get_update_task_query_by_uid(
            uid=uid,
            name=name,
            description=description,
            extra=extra,
            rpc_address=rpc_address,
            auth_algorithm=auth_algorithm,
            private_key=private_key,
            public_key=public_key,
            maximum_restart_count=maximum_restart_count,
            numa_memory_nodes=numa_memory_nodes,
            base_image_name=base_image_name,
            publish_ports=publish_ports,
            updated_at=updated_at,
        )
        await self.execute(query, *args)
        params_msg = f"uid={uid}"
        logger.info(f"update_task_by_uid({params_msg}) ok.")

    async def delete_task_by_uid(self, uid: int) -> None:
        query = DELETE_TASK_BY_UID
        await self.execute(query, uid)
        params_msg = f"uid={uid}"
        logger.info(f"delete_task_by_uid({params_msg}) ok.")

    async def delete_task_by_name(self, project_uid: int, name: str) -> None:
        query = DELETE_TASK_BY_PROJECT_UID_AND_NAME
        await self.execute(query, project_uid, name)
        params_msg = f"project_uid={project_uid},name={name}"
        logger.info(f"delete_task_by_name({params_msg}) ok.")

    async def get_task_by_uid(self, uid: int) -> Task:
        query = SELECT_TASK_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise ReccNotFoundError(f"Not found task: {params_msg}")
        result = Task(**dict(row))
        assert result.uid == uid
        logger.info(f"get_task_by_uid({params_msg}) ok.")
        return result

    async def get_task_by_name(self, project_uid: int, name: str) -> Task:
        query = SELECT_TASK_BY_PROJECT_ID_AND_NAME
        row = await self.fetch_row(query, project_uid, name)
        params_msg = f"project_uid={project_uid},name={name}"
        if not row:
            raise ReccNotFoundError(f"Not found task: {params_msg}")
        result = Task(**dict(row))
        assert result.project_uid == project_uid
        assert result.name == name
        logger.info(f"get_task_by_name({params_msg}) ok.")
        return result

    async def get_task_uid_by_name(self, project_uid: int, name: str) -> int:
        query = SELECT_TASK_UID_BY_PROJECT_ID_AND_NAME
        row = await self.fetch_row(query, project_uid, name)
        params_msg = f"project_uid={project_uid},name={name}"
        if not row:
            raise ReccNotFoundError(f"Not found task: {params_msg}")
        result = row.get("uid")
        if result is None:
            raise ReccNotFoundError(f"Not found task: {params_msg}")
        logger.info(f"get_task_uid_by_name({params_msg}) -> {result}")
        return result

    async def get_task_by_project_uid(self, project_uid: int) -> List[Task]:
        result: List[Task] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_TASK_BY_PROJECT_ID
                async for row in conn.cursor(query, project_uid):
                    item = Task(**dict(row))
                    assert item.project_uid == project_uid
                    result.append(item)
        params_msg = f"project_uid={project_uid}"
        result_msg = f"{len(result)} task"
        logger.info(f"get_task_by_project_uid({params_msg}) -> {result_msg}")
        return result

    async def get_task_by_fullpath(
        self, group_name: str, project_name: str, task_name: str
    ) -> Task:
        query = SELECT_TASK_BY_FULLPATH
        row = await self.fetch_row(query, group_name, project_name, task_name)
        params_msg = f"group={group_name},project={project_name},task={task_name}"
        if not row:
            raise ReccNotFoundError(f"Not found task: {params_msg}")
        if row.get("uid") is None:
            raise ReccNotFoundError(f"Not found task: {params_msg}")
        result = Task(**dict(row))
        assert result.name == task_name
        logger.info(f"get_task_by_fullpath({params_msg}) ok.")
        return result

    async def get_task_uid_by_fullpath(
        self, group_name: str, project_name: str, task_name: str
    ) -> int:
        query = SELECT_TASK_UID_BY_FULLPATH
        row = await self.fetch_row(query, group_name, project_name, task_name)
        params_msg = f"group={group_name},project={project_name},task={task_name}"
        if not row:
            raise ReccNotFoundError(f"Not found task: {params_msg}")
        result = row.get("uid")
        if result is None:
            raise ReccNotFoundError(f"Not found task: {params_msg}")
        logger.info(f"get_task_uid_by_fullpath({params_msg}) -> {result}")
        return result
