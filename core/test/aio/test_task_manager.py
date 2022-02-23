# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase, main
from recc.aio.task_manager import TaskManager, AutoRemoveTaskManager
from asyncio import sleep as asyncio_sleep
from asyncio import TimeoutError, CancelledError


class TaskManagerTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tm = TaskManager()

    async def asyncTearDown(self):
        await self.tm.close()
        self.assertEqual(0, len(self.tm))

    async def test_default(self):
        async def _func():
            return 999

        key1 = "key1"
        self.assertEqual(0, len(self.tm))
        self.tm.create_task(key1, _func())
        self.assertEqual(1, len(self.tm))

        self.assertEqual(999, await self.tm.join(key1))
        self.assertTrue(self.tm[key1].done())
        self.assertFalse(self.tm[key1].cancelled())
        self.assertIsNone(self.tm[key1].exception())
        self.assertEqual(999, self.tm[key1].result())
        self.assertEqual(1, len(self.tm))

    async def test_timeout(self):
        async def _timeout_1s_func():
            await asyncio_sleep(1.0)

        key1 = "key1"
        self.assertEqual(0, len(self.tm))
        self.tm.create_task(key1, _timeout_1s_func(), 0.1)
        self.assertEqual(1, len(self.tm))

        with self.assertRaises(TimeoutError):
            await self.tm.join(key1)

        self.assertTrue(self.tm[key1].done())
        self.assertFalse(self.tm[key1].cancelled())
        self.assertIsNotNone(self.tm[key1].exception())
        self.assertIsInstance(self.tm[key1].exception(), TimeoutError)

    async def test_join_timeout(self):
        async def _timeout_10s_func():
            await asyncio_sleep(10.0)

        key1 = "key1"
        self.assertEqual(0, len(self.tm))
        self.tm.create_task(key1, _timeout_10s_func())
        self.assertEqual(1, len(self.tm))

        with self.assertRaises(TimeoutError):
            await self.tm.join(key1, 0.001)

        self.assertFalse(self.tm[key1].done())
        self.assertFalse(self.tm[key1].cancelled())

        self.tm[key1].cancel()
        self.assertFalse(self.tm[key1].done())
        self.assertFalse(self.tm[key1].cancelled())  # Not now

        with self.assertRaises(CancelledError):
            await self.tm.join(key1)

        self.assertTrue(self.tm[key1].done())
        self.assertTrue(self.tm[key1].cancelled())

        with self.assertRaises(CancelledError):
            self.tm[key1].exception()


class AutoRemoveTaskManagerTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tm = AutoRemoveTaskManager()

    async def asyncTearDown(self):
        await self.tm.close()
        self.assertEqual(0, len(self.tm))

    async def test_default(self):
        async def _func():
            return 777

        key1 = "key1"
        self.assertEqual(0, len(self.tm))
        task1 = self.tm.create_task(key1, _func())
        self.assertEqual(key1, task1.get_name())
        self.assertEqual(1, len(self.tm))

        self.assertEqual(777, await task1)
        self.assertTrue(task1.done())
        self.assertEqual(0, len(self.tm))

    async def test_timeout(self):
        async def _timeout_1s_func():
            await asyncio_sleep(1.0)

        key1 = "key1"
        self.assertEqual(0, len(self.tm))
        task1 = self.tm.create_task(key1, _timeout_1s_func(), 0.1)
        self.assertEqual(key1, task1.get_name())
        self.assertEqual(1, len(self.tm))

        with self.assertRaises(TimeoutError):
            await task1

        self.assertTrue(task1.done())
        self.assertFalse(task1.cancelled())
        self.assertIsNotNone(task1.exception())
        self.assertIsInstance(task1.exception(), TimeoutError)
        self.assertEqual(0, len(self.tm))


if __name__ == "__main__":
    main()
