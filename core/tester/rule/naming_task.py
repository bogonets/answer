# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.rule.naming_task import naming_task, naming_task_network, naming_task_volume


class NamingTaskTestCase(TestCase):
    def test_naming_task(self):
        self.assertEqual("answer.container", naming_task("", "", ""))

    def test_naming_task_volume(self):
        self.assertEqual("answer.volume", naming_task_volume("", ""))

    def test_naming_task_network(self):
        self.assertEqual("answer.network", naming_task_network("", ""))


if __name__ == "__main__":
    main()
