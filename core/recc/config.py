# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import List

from recc import www as recc_www_module
from recc.package.package_utils import get_module_directory


def _assert_isinstance(obj, cls) -> None:
    assert isinstance(obj, cls)


class Config(Namespace):

    http_bind: str
    http_port: int
    http_root: str
    http_timeout: float

    database_host: str
    database_port: int
    database_user: str
    database_pw: str
    database_name: str
    database_timeout: float

    cache_host: str
    cache_port: int
    cache_secret: str
    cache_prefix: str
    cache_timeout: float

    storage_host: str
    storage_port: int
    storage_access: str
    storage_secret: str
    storage_region: str
    storage_bucket: str
    storage_prefix: str
    storage_secure: bool
    storage_timeout: float

    plugin_prefix: str
    plugin_allow: List[str]
    plugin_deny: List[str]

    log_config: str
    log_level: str
    log_simply: bool

    signature: str
    access_token_duration: str
    refresh_token_duration: str

    public_signup: bool
    teardown: bool

    verbose: int
    developer: bool

    @staticmethod
    def release_keys() -> List[str]:
        return [
            "http_timeout",
            "log_level",
            "access_token_duration",
            "refresh_token_duration",
            "public_signup",
            "verbose",
        ]

    @classmethod
    def default(cls):
        return cls(
            http_bind="0.0.0.0",
            http_port=20000,
            http_root=get_module_directory(recc_www_module),
            http_timeout=60.0,
            database_host="localhost",
            database_port=5432,
            database_user="recc",
            database_pw="recc1234",
            database_name="recc",
            database_timeout=24.0,
            cache_host="localhost",
            cache_port=6379,
            cache_secret="",
            cache_prefix="recc:",
            cache_timeout=8.0,
            storage_host="localhost",
            storage_port=9000,
            storage_access="recc",
            storage_secret="recc1234",
            storage_region="",
            storage_bucket="recc",
            storage_prefix="",
            storage_secure=False,
            storage_timeout=32.0,
            plugin_prefix="answer_plugin_",
            plugin_allow=[],
            plugin_deny=[],
            log_config="",
            log_level="info",
            log_simply=False,
            signature="abcd1234",
            access_token_duration="10m",
            refresh_token_duration="1h",
            public_signup=False,
            teardown=False,
            verbose=0,
            developer=False,
        )

    @classmethod
    def test(cls):
        result = cls.default()
        result.http_port = 29999
        result.database_name = "recc.test"
        result.cache_prefix = "recc_test:"
        result.plugin_prefix = "recc_plugin_test_"
        result.log_level = "info"
        result.teardown = True
        result.verbose = 2
        result.developer = True
        return result

    def assertion(self, checker=_assert_isinstance) -> None:
        checker(self.http_bind, str)
        checker(self.http_port, int)
        checker(self.http_root, str)
        checker(self.http_timeout, float)

        checker(self.database_host, str)
        checker(self.database_port, int)
        checker(self.database_user, str)
        checker(self.database_pw, str)
        checker(self.database_name, str)
        checker(self.database_timeout, float)

        checker(self.cache_host, str)
        checker(self.cache_port, int)
        checker(self.cache_secret, str)
        checker(self.cache_prefix, str)
        checker(self.cache_timeout, float)

        checker(self.storage_host, str)
        checker(self.storage_port, int)
        checker(self.storage_access, str)
        checker(self.storage_secret, str)
        checker(self.storage_region, str)
        checker(self.storage_bucket, str)
        checker(self.storage_prefix, str)
        checker(self.storage_secure, bool)
        checker(self.storage_timeout, float)

        checker(self.plugin_prefix, str)
        checker(self.plugin_allow, list)
        checker(self.plugin_deny, list)

        checker(self.log_config, str)
        checker(self.log_level, str)
        checker(self.log_simply, bool)

        checker(self.signature, str)
        checker(self.access_token_duration, str)
        checker(self.refresh_token_duration, str)

        checker(self.public_signup, bool)
        checker(self.teardown, bool)

        checker(self.verbose, int)
        checker(self.developer, bool)
