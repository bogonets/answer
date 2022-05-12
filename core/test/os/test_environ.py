# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.system.environ import exchange_env, get_env, get_os_envs_dict, opt_env

TEST_RECC_HTTP_BIND = "TEST_RECC_HTTP_BIND"


class EnvironTestCase(TestCase):
    def test_get_os_envs_dict(self):
        envs = get_os_envs_dict()
        self.assertIsInstance(envs, dict)
        self.assertLess(0, len(envs["PATH"]))

    def test_exchange_env(self):
        change_value = "1.2.3.4"
        original_http_bind_1 = get_env(TEST_RECC_HTTP_BIND)
        original_http_bind_2 = exchange_env(TEST_RECC_HTTP_BIND, change_value)
        self.assertEqual(original_http_bind_1, original_http_bind_2)

        changed_http_bind_1 = get_env(TEST_RECC_HTTP_BIND)
        self.assertEqual(change_value, changed_http_bind_1)

        changed_http_bind_2 = exchange_env(TEST_RECC_HTTP_BIND, original_http_bind_2)
        self.assertEqual(change_value, changed_http_bind_2)

        original_http_bind_3 = get_env(TEST_RECC_HTTP_BIND)
        self.assertEqual(original_http_bind_1, original_http_bind_3)

    def test_exists_env(self):
        not_exists_default = "__unknown__"
        val = opt_env("PATH", not_exists_default, str)
        self.assertNotEqual(not_exists_default, val)

    def test_casting_raise(self):
        self.assertEqual(9999, opt_env("PATH", 9999, int))

    def test_not_exists_env(self):
        not_exists_default = "__unknown__"
        val = opt_env("__not_exists_key__", not_exists_default, str)
        self.assertEqual(not_exists_default, val)


if __name__ == "__main__":
    main()
