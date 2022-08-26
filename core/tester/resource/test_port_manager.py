# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.resource.port_manager import PortManager


class RpcTestCase(TestCase):
    def test_init_error(self):
        with self.assertRaises(ValueError):
            PortManager(5, 5)
        with self.assertRaises(ValueError):
            PortManager(5, 1)

    def test_default(self):
        pm = PortManager(1, 5)
        self.assertTupleEqual((1, 5), pm.range)
        self.assertEqual(1, pm.min_port)
        self.assertEqual(5, pm.max_port)
        self.assertEqual(0, len(pm.alloc_ports))
        self.assertEqual(5, len(pm.free_ports))
        self.assertListEqual([1, 2, 3, 4, 5], list(pm.free_ports))

        port = pm.alloc()
        self.assertEqual(1, len(pm.alloc_ports))
        self.assertEqual(4, len(pm.free_ports))
        self.assertIn(port, pm.alloc_ports)
        self.assertNotIn(port, pm.free_ports)
        self.assertTrue(pm.range[0] <= port <= pm.range[1])

        pm.alloc()
        pm.alloc()
        pm.alloc()
        pm.alloc()
        self.assertEqual(5, len(pm.alloc_ports))
        self.assertEqual(0, len(pm.free_ports))

        with self.assertRaises(EOFError):
            pm.alloc()
        with self.assertRaises(ValueError):
            pm.alloc(200)

        pm.free(1)
        pm.free(2)
        pm.free(3)
        pm.free(4)
        pm.free(5)
        self.assertEqual(0, len(pm.alloc_ports))
        self.assertEqual(5, len(pm.free_ports))

    def test_free_force(self):
        pm = PortManager(1, 5)
        with self.assertRaises(ValueError):
            pm.free(100)

        pm.free(100, force=True)
        self.assertEqual(0, len(pm.alloc_ports))
        self.assertEqual(6, len(pm.free_ports))

        pm.alloc()
        pm.alloc()
        pm.alloc()
        pm.alloc()
        pm.alloc()
        pm.alloc()
        self.assertEqual(6, len(pm.alloc_ports))
        self.assertEqual(0, len(pm.free_ports))

        pm.free(1)
        pm.free(2)
        pm.free(3)
        pm.free(4)
        pm.free(5)
        self.assertEqual(1, len(pm.alloc_ports))
        self.assertEqual(5, len(pm.free_ports))

    def test_alloc_force(self):
        pm = PortManager(1, 5)
        with self.assertRaises(ValueError):
            pm.alloc(100)

        pm.alloc(100, force=True)
        self.assertEqual(1, len(pm.alloc_ports))
        self.assertEqual(5, len(pm.free_ports))
        self.assertIn(100, pm.alloc_ports)

        pm.free(100)
        self.assertEqual(0, len(pm.alloc_ports))
        self.assertEqual(5, len(pm.free_ports))

    def test_reset(self):
        pm = PortManager(1, 5)
        pm.reset(6, 7)
        self.assertEqual(0, len(pm.alloc_ports))
        self.assertEqual(2, len(pm.free_ports))
        self.assertIn(6, pm.free_ports)
        self.assertIn(7, pm.free_ports)

        pm.alloc()
        pm.alloc()
        self.assertEqual(2, len(pm.alloc_ports))
        self.assertEqual(0, len(pm.free_ports))
        self.assertIn(6, pm.alloc_ports)
        self.assertIn(7, pm.alloc_ports)

        pm.reset(6, 8)
        self.assertEqual(2, len(pm.alloc_ports))
        self.assertEqual(1, len(pm.free_ports))
        self.assertIn(6, pm.alloc_ports)
        self.assertIn(7, pm.alloc_ports)
        self.assertIn(8, pm.free_ports)

        pm.clear()
        self.assertEqual(0, len(pm.alloc_ports))
        self.assertEqual(3, len(pm.free_ports))
        self.assertIn(6, pm.free_ports)
        self.assertIn(7, pm.free_ports)
        self.assertIn(8, pm.free_ports)


if __name__ == "__main__":
    main()
