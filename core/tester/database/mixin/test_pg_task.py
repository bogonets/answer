# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from unittest import main

from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgTaskTestCase(PostgresqlTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.group_slug = "group"
        self.group_uid = await self.db.insert_group(self.group_slug)

        self.project_slug = "project"
        self.project_uid = await self.db.insert_project(
            self.group_uid, self.project_slug
        )
        self.project = await self.db.select_project_by_uid(self.project_uid)

    async def test_none_exists_get(self):
        group = self.group_slug
        project = self.project_slug
        slug = "task"
        unknown = "unknown"
        await self.db.insert_task(self.project_uid, slug)

        with self.assertRaises(LookupError):
            await self.db.select_task_by_fullpath(unknown, project, slug)
        with self.assertRaises(LookupError):
            await self.db.select_task_by_fullpath(group, unknown, slug)
        with self.assertRaises(LookupError):
            await self.db.select_task_by_fullpath(group, project, unknown)

        with self.assertRaises(LookupError):
            await self.db.select_task_uid_by_fullpath(unknown, project, slug)
        with self.assertRaises(LookupError):
            await self.db.select_task_uid_by_fullpath(group, unknown, slug)
        with self.assertRaises(LookupError):
            await self.db.select_task_uid_by_fullpath(group, project, unknown)

    async def test_create_and_get(self):
        slug1 = "slug1"
        slug2 = "slug2"
        name1 = "name1"
        name2 = "name2"
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        created_at2 = datetime.now().astimezone() + timedelta(days=2)
        result1_uid = await self.db.insert_task(
            self.project.uid, slug1, name1, created_at=created_at1
        )
        result2_uid = await self.db.insert_task(
            self.project.uid, slug2, name2, created_at=created_at2
        )
        task1 = await self.db.select_task_by_slug(self.project.uid, slug1)
        task2 = await self.db.select_task_by_slug(self.project.uid, slug2)
        self.assertEqual(result1_uid, task1.uid)
        self.assertEqual(result2_uid, task2.uid)

        self.assertEqual(self.project.uid, task1.project_uid)
        self.assertEqual(self.project.uid, task2.project_uid)
        self.assertEqual(slug1, task1.slug)
        self.assertEqual(slug2, task2.slug)
        self.assertEqual(name1, task1.name)
        self.assertEqual(name2, task2.name)
        self.assertIsNone(task1.description)
        self.assertIsNone(task2.description)
        self.assertIsNone(task1.extra)
        self.assertIsNone(task2.extra)
        self.assertIsNone(task1.rpc_address)
        self.assertIsNone(task2.rpc_address)
        self.assertEqual(created_at1, task1.created_at)
        self.assertEqual(created_at2, task2.created_at)
        self.assertIsNone(task1.maximum_restart_count)
        self.assertIsNone(task2.maximum_restart_count)
        self.assertIsNone(task1.numa_memory_nodes)
        self.assertIsNone(task2.numa_memory_nodes)
        self.assertIsNone(task1.base_image_name)
        self.assertIsNone(task2.base_image_name)
        self.assertIsNone(task1.publish_ports)
        self.assertIsNone(task2.publish_ports)
        self.assertEqual(created_at1, task1.updated_at)
        self.assertEqual(created_at2, task2.updated_at)

        task1_2nd = await self.db.select_task_by_uid(task1.uid)
        task2_2nd = await self.db.select_task_by_uid(task2.uid)
        self.assertEqual(task1, task1_2nd)
        self.assertEqual(task2, task2_2nd)

        group = self.group_slug
        project = self.project_slug
        task1_3rd = await self.db.select_task_by_fullpath(group, project, slug1)
        task2_3rd = await self.db.select_task_by_fullpath(group, project, slug2)
        self.assertEqual(task1, task1_3rd)
        self.assertEqual(task2, task2_3rd)

        task1_4th_uid = await self.db.select_task_uid_by_fullpath(group, project, slug1)
        task2_4th_uid = await self.db.select_task_uid_by_fullpath(group, project, slug2)
        self.assertEqual(task1.uid, task1_4th_uid)
        self.assertEqual(task2.uid, task2_4th_uid)

        task1_5th_uid = await self.db.select_task_uid_by_slug(self.project.uid, slug1)
        task2_5th_uid = await self.db.select_task_uid_by_slug(self.project.uid, slug2)
        self.assertEqual(task1.uid, task1_5th_uid)
        self.assertEqual(task2.uid, task2_5th_uid)

    async def test_update_description(self):
        slug1 = "task1"
        slug2 = "task2"
        await self.db.insert_task(self.project.uid, slug1)
        await self.db.insert_task(self.project.uid, slug2)
        task1_uid = (await self.db.select_task_by_slug(self.project.uid, slug1)).uid

        desc1 = "description1"
        desc2 = "description2"
        updated_at1 = datetime.now().astimezone() + timedelta(days=1)
        updated_at2 = datetime.now().astimezone() + timedelta(days=2)
        await self.db.update_task_description_by_uid(task1_uid, desc1, updated_at1)
        await self.db.update_task_description_by_slug(
            self.project.uid, slug2, desc2, updated_at2
        )

        task1 = await self.db.select_task_by_slug(self.project.uid, slug1)
        task2 = await self.db.select_task_by_slug(self.project.uid, slug2)
        self.assertEqual(desc1, task1.description)
        self.assertEqual(desc2, task2.description)
        self.assertEqual(updated_at1, task1.updated_at)
        self.assertEqual(updated_at2, task2.updated_at)

    async def test_update_extra(self):
        slug1 = "task1"
        slug2 = "task2"
        await self.db.insert_task(self.project.uid, slug1)
        await self.db.insert_task(self.project.uid, slug2)
        task1_uid = (await self.db.select_task_by_slug(self.project.uid, slug1)).uid

        extra1 = {"a": 1, "b": 2}
        extra2 = {"c": 3, "d": 4}
        updated_at1 = datetime.now().astimezone() + timedelta(days=1)
        updated_at2 = datetime.now().astimezone() + timedelta(days=2)
        await self.db.update_task_extra_by_uid(task1_uid, extra1, updated_at1)
        await self.db.update_task_extra_by_slug(
            self.project.uid, slug2, extra2, updated_at2
        )

        task1 = await self.db.select_task_by_slug(self.project.uid, slug1)
        task2 = await self.db.select_task_by_slug(self.project.uid, slug2)
        self.assertEqual(extra1, task1.extra)
        self.assertEqual(extra2, task2.extra)
        self.assertEqual(updated_at1, task1.updated_at)
        self.assertEqual(updated_at2, task2.updated_at)

    async def test_update_keys(self):
        slug1 = "task1"
        slug2 = "task2"
        await self.db.insert_task(self.project.uid, slug1)
        await self.db.insert_task(self.project.uid, slug2)
        task1_uid = (await self.db.select_task_by_slug(self.project.uid, slug1)).uid

        auth_algorithm1 = "algorithm1"
        auth_algorithm2 = "algorithm2"
        private_key1 = "private1"
        private_key2 = "private2"
        public_key1 = "public1"
        public_key2 = "public2"
        updated_at1 = datetime.now().astimezone() + timedelta(days=1)
        updated_at2 = datetime.now().astimezone() + timedelta(days=2)
        await self.db.update_task_keys_by_uid(
            task1_uid,
            auth_algorithm1,
            private_key1,
            public_key1,
            updated_at1,
        )
        await self.db.update_task_keys_by_slug(
            self.project.uid,
            slug2,
            auth_algorithm2,
            private_key2,
            public_key2,
            updated_at2,
        )

        task1 = await self.db.select_task_by_slug(self.project.uid, slug1)
        task2 = await self.db.select_task_by_slug(self.project.uid, slug2)
        self.assertEqual(auth_algorithm1, task1.auth_algorithm)
        self.assertEqual(auth_algorithm2, task2.auth_algorithm)
        self.assertEqual(private_key1, task1.private_key)
        self.assertEqual(private_key2, task2.private_key)
        self.assertEqual(public_key1, task1.public_key)
        self.assertEqual(public_key2, task2.public_key)
        self.assertEqual(updated_at1, task1.updated_at)
        self.assertEqual(updated_at2, task2.updated_at)

    async def test_update_task_by_uid(self):
        slug1 = "task1"
        await self.db.insert_task(self.project.uid, slug1)
        task_uid = (await self.db.select_task_by_slug(self.project.uid, slug1)).uid

        slug2 = "slug2"
        name = "name"
        description = "description"
        extra = {"aa": 1, "bb": 2}
        rpc_address = "[::]:20000"
        auth_algorithm = "algorithm"
        private_key = "private"
        public_key = "public"
        maximum_restart_count = 100
        numa_memory_nodes = "1-2"
        base_image_name = ""
        publish_ports = {"9999/tcp": 9999}
        updated_at = datetime.now().astimezone() + timedelta(days=1)

        await self.db.update_task_by_uid(
            task_uid,
            slug=slug2,
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

        task = await self.db.select_task_by_uid(task_uid)
        self.assertEqual(slug2, task.slug)
        self.assertEqual(name, task.name)
        self.assertEqual(description, task.description)
        self.assertEqual(extra, task.extra)
        self.assertEqual(rpc_address, task.rpc_address)
        self.assertEqual(updated_at, task.updated_at)
        self.assertEqual(maximum_restart_count, task.maximum_restart_count)
        self.assertEqual(numa_memory_nodes, task.numa_memory_nodes)
        self.assertEqual(base_image_name, task.base_image_name)
        self.assertEqual(publish_ports, task.publish_ports)
        self.assertEqual(updated_at, task.updated_at)

    async def test_delete(self):
        slug1 = "task1"
        slug2 = "task2"
        await self.db.insert_task(self.project.uid, slug1)
        await self.db.insert_task(self.project.uid, slug2)
        task1_uid = (await self.db.select_task_by_slug(self.project.uid, slug1)).uid

        tasks1 = await self.db.select_task_by_project_uid(self.project.uid)
        self.assertEqual(2, len(tasks1))

        await self.db.delete_task_by_uid(task1_uid)
        await self.db.delete_task_by_slug(self.project.uid, slug2)

        tasks2 = await self.db.select_task_by_project_uid(self.project.uid)
        self.assertEqual(0, len(tasks2))


if __name__ == "__main__":
    main()
