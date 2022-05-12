# -*- coding: utf-8 -*-

from tester.database.backup.v2_0_0.variables import (
    DAEMON_NAME_STR_SIZE,
    DAEMON_PLUGIN_STR_SIZE,
    DAEMON_SLUG_STR_SIZE,
    EMAIL_STR_SIZE,
    FEATURE_NAME_STR_SIZE,
    GROUP_NAME_STR_SIZE,
    GROUP_SLUG_STR_SIZE,
    INFO_KEY_STR_SIZE,
    LAYOUT_NAME_STR_SIZE,
    NICKNAME_STR_SIZE,
    PASSWORD_HEX_STR_SIZE,
    PERMISSION_SLUG_STR_SIZE,
    PHONE_STR_SIZE,
    PORT_CATEGORY_STR_SIZE,
    PROJECT_NAME_STR_SIZE,
    PROJECT_SLUG_STR_SIZE,
    ROLE_NAME_STR_SIZE,
    ROLE_SLUG_STR_SIZE,
    SALT_HEX_STR_SIZE,
    SHA256_HEX_STR_SIZE,
    TABLE_DAEMON,
    TABLE_GROUP,
    TABLE_GROUP_MEMBER,
    TABLE_INFO,
    TABLE_LAYOUT,
    TABLE_PERMISSION,
    TABLE_PORT,
    TABLE_PROJECT,
    TABLE_PROJECT_MEMBER,
    TABLE_ROLE,
    TABLE_ROLE_PERMISSION,
    TABLE_TASK,
    TABLE_USER,
    TABLE_WIDGET,
    TASK_BASE_IMAGE_STR_SIZE,
    TASK_NAME_STR_SIZE,
    TASK_NUMA_MEMORY_NODES_STR_SIZE,
    TASK_SLUG_STR_SIZE,
    URL_STR_SIZE,
    USER_NAME_STR_SIZE,
    VISIBILITY_LEVEL_PRIVATE,
    WIDGET_NAME_STR_SIZE,
    WIDGET_TYPE_STR_SIZE,
)

# -----------
# Base tables
# -----------

CREATE_TABLE_INFO = f"""
CREATE TABLE IF NOT EXISTS {TABLE_INFO} (
    key VARCHAR({INFO_KEY_STR_SIZE}) PRIMARY KEY,
    value TEXT,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);
"""

CREATE_TABLE_USER = f"""
CREATE TABLE IF NOT EXISTS {TABLE_USER} (
    uid SERIAL PRIMARY KEY,

    username VARCHAR({USER_NAME_STR_SIZE}) UNIQUE NOT NULL,  -- Non-modifiable field.
    password CHAR({PASSWORD_HEX_STR_SIZE}) NOT NULL,
    salt CHAR({SALT_HEX_STR_SIZE}) NOT NULL,

    nickname VARCHAR({NICKNAME_STR_SIZE}),
    email VARCHAR({EMAIL_STR_SIZE}) UNIQUE,
    phone1 VARCHAR({PHONE_STR_SIZE}),
    phone2 VARCHAR({PHONE_STR_SIZE}),
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    extra JSONB,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    last_login TIMESTAMPTZ
);
"""

CREATE_TABLE_GROUP = f"""
CREATE TABLE IF NOT EXISTS {TABLE_GROUP} (
    uid SERIAL PRIMARY KEY,

    slug VARCHAR({GROUP_SLUG_STR_SIZE}) UNIQUE NOT NULL,
    name VARCHAR({GROUP_NAME_STR_SIZE}),
    description TEXT,
    features VARCHAR({FEATURE_NAME_STR_SIZE})[],
    visibility INTEGER NOT NULL DEFAULT {VISIBILITY_LEVEL_PRIVATE},
    extra JSONB,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);
"""

CREATE_TABLE_PERMISSION = f"""
CREATE TABLE IF NOT EXISTS {TABLE_PERMISSION} (
    uid SERIAL PRIMARY KEY,
    slug VARCHAR({PERMISSION_SLUG_STR_SIZE}) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);
"""

CREATE_TABLE_ROLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_ROLE} (
    uid SERIAL PRIMARY KEY,
    slug VARCHAR({ROLE_SLUG_STR_SIZE}) UNIQUE NOT NULL,
    name VARCHAR({ROLE_NAME_STR_SIZE}),
    description TEXT,
    extra JSONB,

    hidden BOOLEAN NOT NULL DEFAULT FALSE,
    lock BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);
"""

CREATE_TABLE_ROLE_PERMISSION = f"""
CREATE TABLE IF NOT EXISTS {TABLE_ROLE_PERMISSION} (
    role_uid INTEGER NOT NULL
        REFERENCES {TABLE_ROLE} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    permission_uid INTEGER NOT NULL
        REFERENCES {TABLE_PERMISSION} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY(role_uid, permission_uid)
);
"""

CREATE_TABLE_PROJECT = f"""
CREATE TABLE IF NOT EXISTS {TABLE_PROJECT} (
    uid SERIAL PRIMARY KEY,

    group_uid INTEGER NOT NULL
        REFERENCES {TABLE_GROUP} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    slug VARCHAR({PROJECT_SLUG_STR_SIZE}) NOT NULL,
    UNIQUE(group_uid, slug),

    name VARCHAR({PROJECT_NAME_STR_SIZE}),
    description TEXT,
    features VARCHAR({FEATURE_NAME_STR_SIZE})[],
    visibility INTEGER NOT NULL DEFAULT {VISIBILITY_LEVEL_PRIVATE},
    extra JSONB,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);
"""

CREATE_TABLE_TASK = f"""
CREATE TABLE IF NOT EXISTS {TABLE_TASK} (
    uid SERIAL PRIMARY KEY,

    project_uid INTEGER NOT NULL
        REFERENCES {TABLE_PROJECT} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    slug VARCHAR({TASK_SLUG_STR_SIZE}) NOT NULL,
    UNIQUE(project_uid, slug),

    name VARCHAR({TASK_NAME_STR_SIZE}),
    description TEXT,
    extra JSONB,

    rpc_address VARCHAR({URL_STR_SIZE}),

    auth_algorithm TEXT,
    private_key TEXT,
    public_key TEXT,

    maximum_restart_count INTEGER,
    numa_memory_nodes VARCHAR({TASK_NUMA_MEMORY_NODES_STR_SIZE}),
    base_image_name VARCHAR({TASK_BASE_IMAGE_STR_SIZE}),
    publish_ports JSONB,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);
"""

CREATE_TABLE_LAYOUT = f"""
CREATE TABLE IF NOT EXISTS {TABLE_LAYOUT} (
    uid SERIAL PRIMARY KEY,

    project_uid INTEGER NOT NULL
        REFERENCES {TABLE_PROJECT} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    name VARCHAR({LAYOUT_NAME_STR_SIZE}) NOT NULL,
    UNIQUE(project_uid, name),

    description TEXT,
    extra JSONB,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);
"""

CREATE_TABLE_WIDGET = f"""
CREATE TABLE IF NOT EXISTS {TABLE_WIDGET} (
    uid SERIAL PRIMARY KEY,

    layout_uid INTEGER NOT NULL
        REFERENCES {TABLE_LAYOUT} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    name VARCHAR({WIDGET_NAME_STR_SIZE}) NOT NULL,
    UNIQUE(layout_uid, name),

    description TEXT,
    extra JSONB,

    type_name VARCHAR({WIDGET_TYPE_STR_SIZE}),
    pos_x1 REAL,
    pos_y1 REAL,
    pos_x2 REAL,
    pos_y2 REAL,
    z_order INTEGER,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);
"""

# --------------------------
# Resource management tables
# --------------------------

CREATE_TABLE_PORT = f"""
CREATE TABLE IF NOT EXISTS {TABLE_PORT} (
    number INTEGER PRIMARY KEY,

    ref_uid INTEGER,
    ref_category VARCHAR({PORT_CATEGORY_STR_SIZE}),

    description TEXT,
    extra JSONB,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);
"""

CREATE_TABLE_DAEMON = f"""
CREATE TABLE IF NOT EXISTS {TABLE_DAEMON} (
    uid SERIAL PRIMARY KEY,

    plugin VARCHAR({DAEMON_PLUGIN_STR_SIZE}) NOT NULL,
    slug VARCHAR({DAEMON_SLUG_STR_SIZE}) UNIQUE NOT NULL,
    name VARCHAR({DAEMON_NAME_STR_SIZE}),
    address VARCHAR({URL_STR_SIZE}),
    requirements_sha256 VARCHAR({SHA256_HEX_STR_SIZE}),
    description TEXT,
    extra JSONB,

    enable BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);
"""

# -----------------
# Relational tables
# -----------------

CREATE_TABLE_GROUP_MEMBER = f"""
CREATE TABLE IF NOT EXISTS {TABLE_GROUP_MEMBER} (
    group_uid INTEGER NOT NULL
        REFERENCES {TABLE_GROUP} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    user_uid INTEGER NOT NULL
        REFERENCES {TABLE_USER} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY(group_uid, user_uid),

    role_uid INTEGER
        REFERENCES {TABLE_ROLE} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
"""

CREATE_TABLE_PROJECT_MEMBER = f"""
CREATE TABLE IF NOT EXISTS {TABLE_PROJECT_MEMBER} (
    project_uid INTEGER NOT NULL
        REFERENCES {TABLE_PROJECT} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    user_uid INTEGER NOT NULL
        REFERENCES {TABLE_USER} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY(project_uid, user_uid),

    role_uid INTEGER
        REFERENCES {TABLE_ROLE} (uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
"""

CREATE_TABLES = (
    # Base tables
    CREATE_TABLE_INFO,
    CREATE_TABLE_USER,
    CREATE_TABLE_GROUP,
    CREATE_TABLE_PERMISSION,
    CREATE_TABLE_ROLE,
    CREATE_TABLE_ROLE_PERMISSION,
    CREATE_TABLE_PROJECT,
    CREATE_TABLE_TASK,
    CREATE_TABLE_LAYOUT,
    CREATE_TABLE_WIDGET,
    # Resource management tables
    CREATE_TABLE_PORT,
    CREATE_TABLE_DAEMON,
    # Relational tables
    CREATE_TABLE_GROUP_MEMBER,
    CREATE_TABLE_PROJECT_MEMBER,
)

# fmt: off
DROP_TABLE_INFO = f"DROP TABLE IF EXISTS {TABLE_INFO};"
DROP_TABLE_USER = f"DROP TABLE IF EXISTS {TABLE_USER};"
DROP_TABLE_GROUP = f"DROP TABLE IF EXISTS {TABLE_GROUP};"
DROP_TABLE_PERMISSION = f"DROP TABLE IF EXISTS {TABLE_PERMISSION};"
DROP_TABLE_ROLE = f"DROP TABLE IF EXISTS {TABLE_ROLE};"
DROP_TABLE_ROLE_PERMISSION = f"DROP TABLE IF EXISTS {TABLE_ROLE_PERMISSION};"
DROP_TABLE_PROJECT = f"DROP TABLE IF EXISTS {TABLE_PROJECT};"
DROP_TABLE_TASK = f"DROP TABLE IF EXISTS {TABLE_TASK};"
DROP_TABLE_LAYOUT = f"DROP TABLE IF EXISTS {TABLE_LAYOUT};"
DROP_TABLE_WIDGET = f"DROP TABLE IF EXISTS {TABLE_WIDGET};"
DROP_TABLE_PORT = f"DROP TABLE IF EXISTS {TABLE_PORT};"
DROP_TABLE_DAEMON = f"DROP TABLE IF EXISTS {TABLE_DAEMON};"
DROP_TABLE_GROUP_MEMBER = f"DROP TABLE IF EXISTS {TABLE_GROUP_MEMBER};"
DROP_TABLE_PROJECT_MEMBER = f"DROP TABLE IF EXISTS {TABLE_PROJECT_MEMBER};"
# fmt: on

DROP_TABLES = (
    # Base tables
    DROP_TABLE_INFO,
    DROP_TABLE_USER,
    DROP_TABLE_GROUP,
    DROP_TABLE_PERMISSION,
    DROP_TABLE_ROLE,
    DROP_TABLE_ROLE_PERMISSION,
    DROP_TABLE_PROJECT,
    DROP_TABLE_TASK,
    DROP_TABLE_LAYOUT,
    DROP_TABLE_WIDGET,
    # Resource management tables
    DROP_TABLE_PORT,
    DROP_TABLE_DAEMON,
    # Relational tables
    DROP_TABLE_GROUP_MEMBER,
    DROP_TABLE_PROJECT_MEMBER,
)
