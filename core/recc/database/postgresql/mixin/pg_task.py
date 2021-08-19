# -*- coding: utf-8 -*-

from typing import Optional, Any, List, Dict
from datetime import datetime
from overrides import overrides
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.task import Task
from recc.database.interfaces.db_task import DbTask
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.task import (
    INSERT_TASK,
    UPDATE_TASK_DESCRIPTION_BY_UID,
    UPDATE_TASK_DESCRIPTION_BY_PROJECT_UID_AND_SLUG,
    UPDATE_TASK_EXTRA_BY_UID,
    UPDATE_TASK_EXTRA_BY_PROJECT_UID_AND_SLUG,
    UPDATE_TASK_KEYS_BY_UID,
    UPDATE_TASK_KEYS_BY_PROJECT_UID_AND_SLUG,
    DELETE_TASK_BY_UID,
    DELETE_TASK_BY_PROJECT_UID_AND_SLUG,
    SELECT_TASK_BY_UID,
    SELECT_TASK_BY_PROJECT_ID_AND_SLUG,
    SELECT_TASK_UID_BY_PROJECT_ID_AND_SLUG,
    SELECT_TASK_BY_PROJECT_ID,
    SELECT_TASK_BY_FULLPATH,
    SELECT_TASK_UID_BY_FULLPATH,
    get_update_task_query_by_uid,
)


class PgTask(DbTask, PgBase):
    @overrides
    async def insert_task(
        self,
        project_uid: int,
        slug: str,
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
        created_at=datetime.utcnow(),
    ) -> int:
        query = INSERT_TASK
        uid = await self.fetch_val(
            query,
            project_uid,
            slug,
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
        logger.info(f"insert_task({params_msg}) -> {uid}")
        return uid

    @overrides
    async def update_task_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_TASK_DESCRIPTION_BY_UID
        await self.execute(query, uid, description, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_task_description_by_uid({params_msg}) ok.")

    @overrides
    async def update_task_description_by_slug(
        self,
        project_uid: int,
        slug: str,
        description: str,
        updated_at=datetime.utcnow(),
    ) -> None:
        query = UPDATE_TASK_DESCRIPTION_BY_PROJECT_UID_AND_SLUG
        await self.execute(query, project_uid, slug, description, updated_at)
        params_msg = f"project_uid={project_uid},slug={slug}"
        logger.info(f"update_task_description_by_slug({params_msg}) ok.")

    @overrides
    async def update_task_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_TASK_EXTRA_BY_UID
        await self.execute(query, uid, extra, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_task_extra_by_uid({params_msg}) ok.")

    @overrides
    async def update_task_extra_by_slug(
        self, project_uid: int, slug: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_TASK_EXTRA_BY_PROJECT_UID_AND_SLUG
        await self.execute(query, project_uid, slug, extra, updated_at)
        params_msg = f"project_uid={project_uid},slug={slug}"
        logger.info(f"update_task_extra_by_slug({params_msg}) ok.")

    @overrides
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

    @overrides
    async def update_task_keys_by_slug(
        self,
        project_uid: int,
        slug: str,
        auth_algorithm: str,
        private_key: str,
        public_key: str,
        updated_at=datetime.utcnow(),
    ) -> None:
        query = UPDATE_TASK_KEYS_BY_PROJECT_UID_AND_SLUG
        await self.execute(
            query,
            project_uid,
            slug,
            auth_algorithm,
            private_key,
            public_key,
            updated_at,
        )
        params_msg = f"project_uid={project_uid},slug={slug}"
        logger.info(f"update_task_keys_by_slug({params_msg}) ok.")

    @overrides
    async def update_task_by_uid(
        self,
        uid: int,
        slug: Optional[str] = None,
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
            slug=slug,
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

    @overrides
    async def delete_task_by_uid(self, uid: int) -> None:
        query = DELETE_TASK_BY_UID
        await self.execute(query, uid)
        params_msg = f"uid={uid}"
        logger.info(f"delete_task_by_uid({params_msg}) ok.")

    @overrides
    async def delete_task_by_slug(self, project_uid: int, slug: str) -> None:
        query = DELETE_TASK_BY_PROJECT_UID_AND_SLUG
        await self.execute(query, project_uid, slug)
        params_msg = f"project_uid={project_uid},slug={slug}"
        logger.info(f"delete_task_by_slug({params_msg}) ok.")

    @overrides
    async def select_task_by_uid(self, uid: int) -> Task:
        query = SELECT_TASK_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found task: {params_msg}")
        result = Task(**dict(row))
        assert result.uid == uid
        logger.info(f"select_task_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_task_by_slug(self, project_uid: int, slug: str) -> Task:
        query = SELECT_TASK_BY_PROJECT_ID_AND_SLUG
        row = await self.fetch_row(query, project_uid, slug)
        params_msg = f"project_uid={project_uid},slug={slug}"
        if not row:
            raise RuntimeError(f"Not found task: {params_msg}")
        result = Task(**dict(row))
        assert result.project_uid == project_uid
        assert result.slug == slug
        logger.info(f"select_task_by_slug({params_msg}) ok.")
        return result

    @overrides
    async def select_task_uid_by_slug(self, project_uid: int, slug: str) -> int:
        query = SELECT_TASK_UID_BY_PROJECT_ID_AND_SLUG
        row = await self.fetch_row(query, project_uid, slug)
        params_msg = f"project_uid={project_uid},slug={slug}"
        if not row:
            raise RuntimeError(f"Not found task: {params_msg}")
        result = row.get("uid")
        if result is None:
            raise RuntimeError(f"Not found task: {params_msg}")
        logger.info(f"select_task_uid_by_slug({params_msg}) -> {result}")
        return result

    @overrides
    async def select_task_by_project_uid(self, project_uid: int) -> List[Task]:
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
        logger.info(f"select_task_by_project_uid({params_msg}) -> {result_msg}")
        return result

    @overrides
    async def select_task_by_fullpath(
        self, group_slug: str, project_slug: str, task_slug: str
    ) -> Task:
        query = SELECT_TASK_BY_FULLPATH
        row = await self.fetch_row(query, group_slug, project_slug, task_slug)
        params_msg = f"group={group_slug},project={project_slug},task={task_slug}"
        if not row:
            raise RuntimeError(f"Not found task: {params_msg}")
        if row.get("uid") is None:
            raise RuntimeError(f"Not found task: {params_msg}")
        result = Task(**dict(row))
        assert result.slug == task_slug
        logger.info(f"select_task_by_fullpath({params_msg}) ok.")
        return result

    @overrides
    async def select_task_uid_by_fullpath(
        self, group_slug: str, project_slug: str, task_slug: str
    ) -> int:
        query = SELECT_TASK_UID_BY_FULLPATH
        row = await self.fetch_row(query, group_slug, project_slug, task_slug)
        params_msg = f"group={group_slug},project={project_slug},task={task_slug}"
        if not row:
            raise RuntimeError(f"Not found task: {params_msg}")
        result = row.get("uid")
        if result is None:
            raise RuntimeError(f"Not found task: {params_msg}")
        logger.info(f"select_task_uid_by_fullpath({params_msg}) -> {result}")
        return result
