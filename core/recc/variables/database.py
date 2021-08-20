# -*- coding: utf-8 -*-

DB_TYPE_NAME_POSTGRES = "postgres"
DB_TYPE_NAME_MYSQL = "mysql"
DB_TYPE_NAME_SQLITE = "sqlite"

TABLE_PREFIX = "recc_"
TABLE_INFO = f"{TABLE_PREFIX}info"
TABLE_USER = f"{TABLE_PREFIX}user"
TABLE_GROUP = f"{TABLE_PREFIX}group"
TABLE_PERMISSION = f"{TABLE_PREFIX}permission"
TABLE_PROJECT = f"{TABLE_PREFIX}project"
TABLE_TASK = f"{TABLE_PREFIX}task"
TABLE_LAYOUT = f"{TABLE_PREFIX}layout"
TABLE_WIDGET = f"{TABLE_PREFIX}widget"
TABLE_PORT = f"{TABLE_PREFIX}port"
TABLE_GROUP_MEMBER = f"{TABLE_PREFIX}group_member"
TABLE_PROJECT_MEMBER = f"{TABLE_PREFIX}project_member"

INDEX_PREFIX = "recc_"
INDEX_USER_NAME = f"{INDEX_PREFIX}user_name"
INDEX_USER_EMAIL = f"{INDEX_PREFIX}user_email"
INDEX_GROUP_SLUG = f"{INDEX_PREFIX}group_name"
INDEX_PERMISSION_NAME = f"{INDEX_PREFIX}permission_name"
INDEX_PROJECT_NAME = f"{INDEX_PREFIX}project_name"
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

RECC_DB_VERSION_KEY = "recc.db.version"
RECC_UUID_KEY = "recc.uuid"
RECC_INSTALL_TIMESTAMP_KEY = "recc.install.timestamp"

DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_CLOSE_TIMEOUT_SECONDS = 30.0

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
PERMISSION_NAME_STR_SIZE = 128
PROJECT_SLUG_STR_SIZE = 128
PROJECT_NAME_STR_SIZE = 128
LAYOUT_NAME_STR_SIZE = 128
WIDGET_NAME_STR_SIZE = 128
WIDGET_TYPE_STR_SIZE = 128
GRAPH_NAME_STR_SIZE = 128
TASK_SLUG_STR_SIZE = 128
TASK_NAME_STR_SIZE = 128

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

ANONYMOUS_GROUP_SLUG = "-"
ANONYMOUS_GROUP_DESCRIPTION = "Anonymous Group"

PERMISSION_NAME_GUEST = "Guest"
PERMISSION_NAME_REPORTER = "Reporter"
PERMISSION_NAME_OPERATOR = "Operator"
PERMISSION_NAME_MAINTAINER = "Maintainer"
PERMISSION_NAME_OWNER = "Owner"

VISIBILITY_LEVEL_PRIVATE = 0
VISIBILITY_LEVEL_INTERNAL = 10
VISIBILITY_LEVEL_PUBLIC = 20

GROUP_UID_ANONYMOUS = 1
PERMISSION_UID_GUEST = 1
PERMISSION_UID_REPORTER = 2
PERMISSION_UID_OPERATOR = 3
PERMISSION_UID_MAINTAINER = 4
PERMISSION_UID_OWNER = 5
