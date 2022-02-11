# -*- coding: utf-8 -*-

from unittest import TestCase, main
from multiprocessing.shared_memory import SharedMemory
from recc.memory.shared_memory_queue import SharedMemoryQueue


class SharedMemoryQueueTestCase(TestCase):
    def setUp(self):
        self.buffer_size = 4
        self.smq = SharedMemoryQueue()

    def tearDown(self):
        self.smq.clear()

    def test_default(self):
        self.assertEqual(0, self.smq.size_waiting())
        self.assertEqual(0, self.smq.size_working())

        test0 = b"aaa"
        written0 = self.smq.write(test0)
        name0 = written0.sm_name
        self.assertTrue(name0)
        self.assertEqual(0, self.smq.size_waiting())
        self.assertEqual(1, self.smq.size_working())

        result0 = self.smq.read(name0, size=len(test0))
        self.assertEqual(test0, result0)

        self.smq.restore(name0)
        self.assertEqual(1, self.smq.size_waiting())
        self.assertEqual(0, self.smq.size_working())

        test1 = b"kk"
        written1 = self.smq.write(test1, offset=1)
        name1 = written1.sm_name
        self.assertEqual(name1, name0)
        self.assertEqual(0, self.smq.size_waiting())
        self.assertEqual(1, self.smq.size_working())

        result1 = self.smq.read(name0, offset=1, size=len(test1))
        self.assertEqual(test1, result1)

        self.smq.clear()
        self.assertEqual(0, self.smq.size_waiting())
        self.assertEqual(0, self.smq.size_working())

    def test_rant(self):
        self.assertEqual(0, self.smq.size_waiting())
        self.assertEqual(0, self.smq.size_working())

        test0 = b"aaa"
        with self.smq.rent(len(test0)) as sm:
            self.assertEqual(0, self.smq.size_waiting())
            self.assertEqual(1, self.smq.size_working())

            sm.buf[: len(test0)] = test0

            self.assertIsInstance(sm, SharedMemory)
            result0 = self.smq.read(sm.name, size=len(test0))
            self.assertEqual(test0, result0)

        self.assertEqual(1, self.smq.size_waiting())
        self.assertEqual(0, self.smq.size_working())


if __name__ == "__main__":
    main()
