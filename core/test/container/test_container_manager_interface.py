# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.container.container_manager_interface import ContainerStatus


class ContainerStatusTestCase(TestCase):
    def test_default(self):
        # fmt: off
        self.assertEqual(ContainerStatus.Created, ContainerStatus.from_str("created"))
        self.assertEqual(ContainerStatus.Restarting, ContainerStatus.from_str("restarting"))  # noqa
        self.assertEqual(ContainerStatus.Running, ContainerStatus.from_str("running"))
        self.assertEqual(ContainerStatus.Removing, ContainerStatus.from_str("removing"))
        self.assertEqual(ContainerStatus.Paused, ContainerStatus.from_str("paused"))
        self.assertEqual(ContainerStatus.Exited, ContainerStatus.from_str("exited"))
        self.assertEqual(ContainerStatus.Dead, ContainerStatus.from_str("dead"))
        # fmt: on

        self.assertEqual(ContainerStatus.Created, ContainerStatus.from_str("Created"))
        self.assertEqual(ContainerStatus.Created, ContainerStatus.from_str("createD"))
        self.assertRaises(KeyError, ContainerStatus.from_str, "c")


if __name__ == "__main__":
    main()
