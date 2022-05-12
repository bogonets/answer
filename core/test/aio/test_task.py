# -*- coding: utf-8 -*-

from asyncio import CancelledError, create_task, get_event_loop
from asyncio import sleep as asyncio_sleep
from unittest import IsolatedAsyncioTestCase, main

from recc.aio.task import all_tasks


async def _timeout_1s_cb():
    await asyncio_sleep(1.0)


class TaskTestCase(IsolatedAsyncioTestCase):
    async def test_all_tasks(self):
        name = "Task1"
        task = create_task(_timeout_1s_cb(), name=name)
        self.assertFalse(task.done())

        tasks = all_tasks(get_event_loop())
        self.assertLess(0, len(tasks))
        find_task = list(filter(lambda x: x.get_name() == name, tasks))
        self.assertEqual(1, len(find_task))
        self.assertEqual(name, find_task[0].get_name())

        task.cancel()
        with self.assertRaises(CancelledError):
            await task

        self.assertTrue(task.done())
        self.assertTrue(task.cancelled())


if __name__ == "__main__":
    main()
