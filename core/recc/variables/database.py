# -*- coding: utf-8 -*-

from typing import Final, Literal, get_args

DatabaseTypeLiteral = Literal["postgres", "mysql", "sqlite"]

_DATABASE_TYPE_LITERAL_ARGS = get_args(DatabaseTypeLiteral)

DB_TYPE_NAME_POSTGRES: Final[str] = _DATABASE_TYPE_LITERAL_ARGS[0]
DB_TYPE_NAME_MYSQL: Final[str] = _DATABASE_TYPE_LITERAL_ARGS[1]
DB_TYPE_NAME_SQLITE: Final[str] = _DATABASE_TYPE_LITERAL_ARGS[2]

TABLE_PREFIX = "recc_"
TABLE_INFO = f"{TABLE_PREFIX}info"
TABLE_USER = f"{TABLE_PREFIX}user"
TABLE_GROUP = f"{TABLE_PREFIX}group"
TABLE_PERMISSION = f"{TABLE_PREFIX}permission"
TABLE_ROLE = f"{TABLE_PREFIX}role"
TABLE_ROLE_PERMISSION = f"{TABLE_PREFIX}role_permission"
TABLE_PROJECT = f"{TABLE_PREFIX}project"
TABLE_TASK = f"{TABLE_PREFIX}task"
TABLE_LAYOUT = f"{TABLE_PREFIX}layout"
TABLE_WIDGET = f"{TABLE_PREFIX}widget"
TABLE_PORT = f"{TABLE_PREFIX}port"
TABLE_DAEMON = f"{TABLE_PREFIX}daemon"
TABLE_GROUP_MEMBER = f"{TABLE_PREFIX}group_member"
TABLE_PROJECT_MEMBER = f"{TABLE_PREFIX}project_member"

INDEX_PREFIX = "recc_"
INDEX_USER_NAME = f"{INDEX_PREFIX}user_name"
INDEX_USER_EMAIL = f"{INDEX_PREFIX}user_email"
INDEX_GROUP_SLUG = f"{INDEX_PREFIX}group_slug"
INDEX_PROJECT_SLUG = f"{INDEX_PREFIX}project_slug"
INDEX_ROLE_SLUG = f"{INDEX_PREFIX}role_slug"
INDEX_TASK_NAME = f"{INDEX_PREFIX}task_name"
INDEX_LAYOUT_NAME = f"{INDEX_PREFIX}layout_name"
INDEX_WIDGET_NAME = f"{INDEX_PREFIX}widget_name"

VIEW_PREFIX = "recc_"
VIEW_INFO_DB_VERSION = f"{VIEW_PREFIX}info_db_version"
VIEW_USER_ADMIN = f"{VIEW_PREFIX}user_admin"
VIEW_USER_ADMIN_COUNT = f"{VIEW_PREFIX}user_admin_count"

FUNC_PREFIX = "recc_"
FUNC_APPROPRIATE_PERMISSION = f"{FUNC_PREFIX}appropriate_permission"

INFO_KEY_RECC_DB_VERSION = "recc.db.version"
INFO_KEY_RECC_DB_INIT = "recc.db.init"
INFO_KEY_RECC_ARGPARSE_CONFIG = "recc.argparse.config"
INFO_KEY_RECC_UUID = "recc.uuid"
INFO_KEY_RECC_INSTALL_TIMESTAMP = "recc.install.timestamp"
INFO_KEY_OEM = "oem"

CONFIG_PREFIX_RECC_ARGPARSE_CONFIG = INFO_KEY_RECC_ARGPARSE_CONFIG + "."

DATABASE_COMMAND_TIMEOUT_SECONDS = 60.0
DATABASE_CLOSE_TIMEOUT_SECONDS = 60.0

SHA256_BYTE = 32
SHA256_HEX_STR_SIZE = SHA256_BYTE * 2

INFO_KEY_STR_SIZE = 256
USER_NAME_STR_SIZE = 128
PASSWORD_BYTE = 32
PASSWORD_HEX_STR_SIZE = PASSWORD_BYTE * 2
SALT_BYTE = 32
SALT_HEX_STR_SIZE = SALT_BYTE * 2
NICKNAME_STR_SIZE = 128
EMAIL_STR_SIZE = 320  # https://tools.ietf.org/html/rfc3696#section-3
URL_STR_SIZE = 2048
PHONE_STR_SIZE = 128
GROUP_SLUG_STR_SIZE = 128
GROUP_NAME_STR_SIZE = 128
PERMISSION_SLUG_STR_SIZE = 256
ROLE_SLUG_STR_SIZE = 128
ROLE_NAME_STR_SIZE = 128
PROJECT_SLUG_STR_SIZE = 128
PROJECT_NAME_STR_SIZE = 128
LAYOUT_NAME_STR_SIZE = 128
WIDGET_NAME_STR_SIZE = 128
WIDGET_TYPE_STR_SIZE = 128
GRAPH_NAME_STR_SIZE = 128
TASK_SLUG_STR_SIZE = 128
TASK_NAME_STR_SIZE = 128
PORT_CATEGORY_STR_SIZE = 128
DAEMON_PLUGIN_STR_SIZE = 256
DAEMON_SLUG_STR_SIZE = 128
DAEMON_NAME_STR_SIZE = 128

# IPv6 addresses will consists of
# - 8 sets of 4 characters -> `32` characters.
# - each separated by a colon(':') -> `7` characters.
# - prefix('[') and suffix(']') -> `2` characters.
_MAXIMUM_IPV6_EXAMPLE = "[2001:0db8:85a3:08d3:1319:8a2e:0370:7334]"
TASK_RPC_BIND_STR_SIZE = 41  # 32 + 7 + 2
assert TASK_RPC_BIND_STR_SIZE == len(_MAXIMUM_IPV6_EXAMPLE)

_MAXIMUM_NUMA_EXAMPLE = "1000-9999"  # Maybe impossible
TASK_NUMA_MEMORY_NODES_STR_SIZE = 9
assert TASK_NUMA_MEMORY_NODES_STR_SIZE == len(_MAXIMUM_NUMA_EXAMPLE)

TASK_BASE_IMAGE_STR_SIZE = 128
FEATURE_NAME_STR_SIZE = 128

PERMISSION_FAKE_RECC_INHERITANCE_GROUP = "_.recc.inheritance.group"

PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW = "recc.domain.layout.view"
PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT = "recc.domain.layout.edit"
PERMISSION_SLUG_RECC_DOMAIN_FILE_VIEW = "recc.domain.file.view"
PERMISSION_SLUG_RECC_DOMAIN_FILE_EDIT = "recc.domain.file.edit"
PERMISSION_SLUG_RECC_DOMAIN_TABLE_VIEW = "recc.domain.table.view"
PERMISSION_SLUG_RECC_DOMAIN_TABLE_EDIT = "recc.domain.table.edit"
PERMISSION_SLUG_RECC_DOMAIN_TASK_VIEW = "recc.domain.task.view"
PERMISSION_SLUG_RECC_DOMAIN_TASK_EDIT = "recc.domain.task.edit"
PERMISSION_SLUG_RECC_DOMAIN_VP_VIEW = "recc.domain.vp.view"
PERMISSION_SLUG_RECC_DOMAIN_VP_EDIT = "recc.domain.vp.edit"
PERMISSION_SLUG_RECC_DOMAIN_MEMBER_VIEW = "recc.domain.member.view"
PERMISSION_SLUG_RECC_DOMAIN_MEMBER_EDIT = "recc.domain.member.edit"
PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW = "recc.domain.setting.view"
PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT = "recc.domain.setting.edit"
PERMISSION_SLUG_RECC_DOMAIN_DELETE = "recc.domain.delete"

DEFAULT_PERMISSION_SLUGS = (
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_VP_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_VP_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_DELETE,
)

ROLE_UID_OWNER = 1
"""
It is assumed that the owner's UID must be `1`.
"""

ROLE_SLUG_OWNER = "owner"
ROLE_SLUG_MAINTAINER = "maintainer"
ROLE_SLUG_DEVELOPER = "developer"
ROLE_SLUG_REPORTER = "reporter"
ROLE_SLUG_GUEST = "guest"

DEFAULT_ROLE_SLUGS = (
    ROLE_SLUG_OWNER,
    ROLE_SLUG_MAINTAINER,
    ROLE_SLUG_DEVELOPER,
    ROLE_SLUG_REPORTER,
    ROLE_SLUG_GUEST,
)

PERMISSIONS_OF_OWNER = (
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_VP_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_VP_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_DELETE,
)
PERMISSIONS_OF_MAINTAINER = (
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_VP_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_VP_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT,
)
PERMISSIONS_OF_DEVELOPER = (
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_VP_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_VP_EDIT,
)
PERMISSIONS_OF_REPORTER = (
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_VIEW,
)
PERMISSIONS_OF_GUEST = (PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,)

DEFAULT_ROLE_PERMISSIONS_MAP = {
    ROLE_SLUG_OWNER: PERMISSIONS_OF_OWNER,
    ROLE_SLUG_MAINTAINER: PERMISSIONS_OF_MAINTAINER,
    ROLE_SLUG_DEVELOPER: PERMISSIONS_OF_DEVELOPER,
    ROLE_SLUG_REPORTER: PERMISSIONS_OF_REPORTER,
    ROLE_SLUG_GUEST: PERMISSIONS_OF_GUEST,
}

VISIBILITY_LEVEL_PRIVATE = 0
VISIBILITY_LEVEL_INTERNAL = 10
VISIBILITY_LEVEL_PUBLIC = 20
