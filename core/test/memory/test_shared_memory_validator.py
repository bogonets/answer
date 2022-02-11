# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.memory.shared_memory_validator import (
    SharedMemoryTestInfo,
    register_shared_memory,
    validate_shared_memory,
)


class SharedMemoryValidatorTestCase(TestCase):
    def test_default(self):
        with register_shared_memory() as test:
            self.assertIsInstance(test, SharedMemoryTestInfo)
            self.assertTrue(validate_shared_memory(test.name, test.data))


if __name__ == "__main__":
    main()
