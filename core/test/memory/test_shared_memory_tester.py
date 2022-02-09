# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.memory.shared_memory_tester import (
    SharedMemoryTestInfo,
    shared_memory_tester,
    test_shared_memory,
)


class SharedMemoryTesterTestCase(TestCase):
    def test_default(self):
        with shared_memory_tester() as test:
            self.assertIsInstance(test, SharedMemoryTestInfo)
            self.assertTrue(test_shared_memory(test.name, test.data))


if __name__ == "__main__":
    main()
