# -*- coding: utf-8 -*-

DB_TYPE_NAME_POSTGRES = "postgres"
DB_TYPE_NAME_MYSQL = "mysql"
DB_TYPE_NAME_SQLITE = "sqlite"

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
# VIEW_USER_GROUP = f"{VIEW_PREFIX}user_group"
# VIEW_USER_PROJECT = f"{VIEW_PREFIX}user_project"
# VIEW_USER_TASK = f"{VIEW_PREFIX}user_task"
# VIEW_USER_LAYOUT = f"{VIEW_PREFIX}user_layout"
# VIEW_USER_WIDGET = f"{VIEW_PREFIX}user_widget"
# VIEW_GROUP_PROJECT = f"{VIEW_PREFIX}group_project"
# VIEW_GROUP_TASK = f"{VIEW_PREFIX}group_task"
# VIEW_GROUP_LAYOUT = f"{VIEW_PREFIX}group_layout"
# VIEW_GROUP_WIDGET = f"{VIEW_PREFIX}group_widget"
# VIEW_PROJECT_TASK = f"{VIEW_PREFIX}project_task"
# VIEW_PROJECT_LAYOUT = f"{VIEW_PREFIX}project_layout"
# VIEW_PROJECT_WIDGET = f"{VIEW_PREFIX}project_widget"
# VIEW_LAYOUT_WIDGET = f"{VIEW_PREFIX}layout_widget"

INFO_KEY_RECC_DB_VERSION = "recc.db.version"
INFO_KEY_RECC_DB_INIT = "recc.db.init"
INFO_KEY_RECC_ARGPARSE_CONFIG = "recc.argparse.config"
INFO_KEY_RECC_UUID = "recc.uuid"
INFO_KEY_RECC_INSTALL_TIMESTAMP = "recc.install.timestamp"
INFO_KEY_OEM = "oem"

CONFIG_PREFIX_RECC_ARGPARSE_CONFIG = INFO_KEY_RECC_ARGPARSE_CONFIG + "."

DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_CLOSE_TIMEOUT_SECONDS = 30.0

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

PERMISSION_SLUG_RECC_GROUP_PROJECT_LAYOUT_VIEW = "recc.group.project.layout.view"
PERMISSION_SLUG_RECC_GROUP_PROJECT_LAYOUT_EDIT = "recc.group.project.layout.edit"
PERMISSION_SLUG_RECC_GROUP_PROJECT_STORAGE_VIEW = "recc.group.project.storage.view"
PERMISSION_SLUG_RECC_GROUP_PROJECT_STORAGE_EDIT = "recc.group.project.storage.edit"
PERMISSION_SLUG_RECC_GROUP_PROJECT_MANAGER_VIEW = "recc.group.project.manager.view"
PERMISSION_SLUG_RECC_GROUP_PROJECT_MANAGER_EDIT = "recc.group.project.manager.edit"
PERMISSION_SLUG_RECC_GROUP_PROJECT_GRAPH_VIEW = "recc.group.project.graph.view"
PERMISSION_SLUG_RECC_GROUP_PROJECT_GRAPH_EDIT = "recc.group.project.graph.edit"
PERMISSION_SLUG_RECC_GROUP_PROJECT_MEMBER_VIEW = "recc.group.project.member.view"
PERMISSION_SLUG_RECC_GROUP_PROJECT_MEMBER_EDIT = "recc.group.project.member.edit"
PERMISSION_SLUG_RECC_GROUP_PROJECT_SETTING_VIEW = "recc.group.project.setting.view"
PERMISSION_SLUG_RECC_GROUP_PROJECT_SETTING_EDIT = "recc.group.project.setting.edit"

PERMISSION_SLUG_RECC_GROUP_PROJECT_NEW = "recc.group.project.new"
PERMISSION_SLUG_RECC_GROUP_PROJECT_DEL = "recc.group.project.del"
PERMISSION_SLUG_RECC_GROUP_PROJECT_VIEW = "recc.group.project.view"
PERMISSION_SLUG_RECC_GROUP_PROJECT_EDIT = "recc.group.project.edit"

PERMISSION_SLUG_RECC_GROUP_MEMBER_VIEW = "recc.group.member.view"
PERMISSION_SLUG_RECC_GROUP_MEMBER_EDIT = "recc.group.member.edit"
PERMISSION_SLUG_RECC_GROUP_SETTING_VIEW = "recc.group.setting.view"
PERMISSION_SLUG_RECC_GROUP_SETTING_EDIT = "recc.group.setting.edit"
PERMISSION_SLUG_RECC_GROUP_DELETE = "recc.group.delete"

DEFAULT_PERMISSION_SLUGS = (
    PERMISSION_SLUG_RECC_GROUP_PROJECT_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_LAYOUT_EDIT,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_STORAGE_VIEW,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_STORAGE_EDIT,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_MANAGER_VIEW,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_MANAGER_EDIT,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_GRAPH_VIEW,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_GRAPH_EDIT,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_MEMBER_VIEW,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_MEMBER_EDIT,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_SETTING_VIEW,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_SETTING_EDIT,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_NEW,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_DEL,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_VIEW,
    PERMISSION_SLUG_RECC_GROUP_PROJECT_EDIT,
    PERMISSION_SLUG_RECC_GROUP_MEMBER_VIEW,
    PERMISSION_SLUG_RECC_GROUP_MEMBER_EDIT,
    PERMISSION_SLUG_RECC_GROUP_SETTING_VIEW,
    PERMISSION_SLUG_RECC_GROUP_SETTING_EDIT,
    PERMISSION_SLUG_RECC_GROUP_DELETE,
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

VISIBILITY_LEVEL_PRIVATE = 0
VISIBILITY_LEVEL_INTERNAL = 10
VISIBILITY_LEVEL_PUBLIC = 20
