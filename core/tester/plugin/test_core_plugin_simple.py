# -*- coding: utf-8 -*-

from unittest import main

from recc.plugin.core_plugin import CorePlugin
from tester.unittest.plugin_test_case import PluginTestCase


class CorePluginSimpleTestCase(PluginTestCase):
    async def test_default(self):
        module_name = self.recc_plugin_test_simple
        self.assertIn(module_name, self.test_core_plugin_names)

        plugin = CorePlugin(module_name)
        self.assertEqual(module_name, plugin.module_name)

        self.assertTrue(plugin.has_on_create)
        self.assertTrue(plugin.has_on_destroy)
        self.assertTrue(plugin.has_on_open)
        self.assertTrue(plugin.has_on_close)

        self.assertFalse(plugin.has_on_create_group)
        self.assertFalse(plugin.has_on_delete_group)
        self.assertFalse(plugin.has_on_create_project)
        self.assertFalse(plugin.has_on_delete_project)

        self.assertFalse(plugin.has_on_routes)

        fake_context = object()
        plugin.on_create(fake_context)

        await plugin.on_open()
        await plugin.on_close()
        plugin.on_destroy()


if __name__ == "__main__":
    main()
