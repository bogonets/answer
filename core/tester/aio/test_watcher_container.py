# -*- coding: utf-8 -*-

from typing import Optional
from unittest import TestCase, main

from recc.aio.watcher_container import WatcherContainer


class WatcherContainerTestCase(TestCase):
    def setUp(self):
        self.key = "test1"
        self.value = 10
        self.old: Optional[int] = None
        self.new: Optional[int] = None

    def _value_watcher(self, *args, **kwargs) -> None:
        self.value = args[0] + args[1] + kwargs["test"]

    def test_default(self):
        self.watchers = WatcherContainer()
        self.assertEqual(0, len(self.watchers))

        self.watchers[self.key] = self._value_watcher
        self.assertEqual(1, len(self.watchers))

        self.assertEqual(10, self.value)
        self.watchers.call_synced_watcher(self.key, 1, 20, test=300)
        self.assertEqual(321, self.value)


if __name__ == "__main__":
    main()
