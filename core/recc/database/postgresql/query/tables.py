# -*- coding: utf-8 -*-

from recc.variables.database import (
    TABLE_INFO,
    TABLE_USER,
    TABLE_GROUP,
    TABLE_PERMISSION,
    TABLE_PROJECT,
    TABLE_TASK,
    TABLE_LAYOUT,
    TABLE_WIDGET,
    TABLE_PORT,
    TABLE_GROUP_MEMBER,
    TABLE_PROJECT_MEMBER,
    INFO_KEY_STR_SIZE,
    PASSWORD_HEX_STR_SIZE,
    SALT_HEX_STR_SIZE,
    NICKNAME_STR_SIZE,
    EMAIL_STR_SIZE,
    URL_STR_SIZE,
    PHONE_STR_SIZE,
    USER_NAME_STR_SIZE,
    GROUP_SLUG_STR_SIZE,
    GROUP_NAME_STR_SIZE,
    PERMISSION_NAME_STR_SIZE,
    PROJECT_NAME_STR_SIZE,
    LAYOUT_NAME_STR_SIZE,
    WIDGET_NAME_STR_SIZE,
    WIDGET_TYPE_STR_SIZE,
    TASK_NAME_STR_SIZE,
    TASK_NUMA_MEMORY_NODES_STR_SIZE,
    TASK_BASE_IMAGE_STR_SIZE,
    FEATURE_NAME_STR_SIZE,
)

# -----------
# Base tables
# -----------

CREATE_TABLE_INFO = f"""
CREATE TABLE IF NOT EXISTS {TABLE_INFO} (
    key VARCHAR({INFO_KEY_STR_SIZE}) PRIMARY KEY,
    value TEXT,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
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

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    last_login TIMESTAMP
);
"""

CREATE_TABLE_GROUP = f"""
CREATE TABLE IF NOT EXISTS {TABLE_GROUP} (
    uid SERIAL PRIMARY KEY,

    slug VARCHAR({GROUP_SLUG_STR_SIZE}) UNIQUE NOT NULL,
    name VARCHAR({GROUP_NAME_STR_SIZE}),
    description TEXT,
    features VARCHAR({FEATURE_NAME_STR_SIZE})[],
    extra JSONB,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
"""

CREATE_TABLE_PERMISSION = f"""
CREATE TABLE IF NOT EXISTS {TABLE_PERMISSION} (
    uid SERIAL PRIMARY KEY,

    name VARCHAR({PERMISSION_NAME_STR_SIZE}) UNIQUE NOT NULL,
    description TEXT,
    extra JSONB,

    r_layout BOOLEAN NOT NULL DEFAULT FALSE,
    w_layout BOOLEAN NOT NULL DEFAULT FALSE,

    r_storage BOOLEAN NOT NULL DEFAULT FALSE,
    w_storage BOOLEAN NOT NULL DEFAULT FALSE,

    r_manager BOOLEAN NOT NULL DEFAULT FALSE,
    w_manager BOOLEAN NOT NULL DEFAULT FALSE,

    r_graph BOOLEAN NOT NULL DEFAULT FALSE,
    w_graph BOOLEAN NOT NULL DEFAULT FALSE,

    r_member BOOLEAN NOT NULL DEFAULT FALSE,
    w_member BOOLEAN NOT NULL DEFAULT FALSE,

    r_setting BOOLEAN NOT NULL DEFAULT FALSE,
    w_setting BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
"""

CREATE_TABLE_PROJECT = f"""
CREATE TABLE IF NOT EXISTS {TABLE_PROJECT} (
    uid SERIAL PRIMARY KEY,

    group_uid INTEGER NOT NULL REFERENCES {TABLE_GROUP} (uid),
    name VARCHAR({PROJECT_NAME_STR_SIZE}) NOT NULL,
    UNIQUE(group_uid, name),

    description TEXT,
    features VARCHAR({FEATURE_NAME_STR_SIZE})[],
    extra JSONB,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
"""

CREATE_TABLE_TASK = f"""
CREATE TABLE IF NOT EXISTS {TABLE_TASK} (
    uid SERIAL PRIMARY KEY,

    project_uid INTEGER NOT NULL REFERENCES {TABLE_PROJECT} (uid),
    name VARCHAR({TASK_NAME_STR_SIZE}) NOT NULL,
    UNIQUE(project_uid, name),

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

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
"""

CREATE_TABLE_LAYOUT = f"""
CREATE TABLE IF NOT EXISTS {TABLE_LAYOUT} (
    uid SERIAL PRIMARY KEY,

    project_uid INTEGER NOT NULL REFERENCES {TABLE_PROJECT} (uid),
    name VARCHAR({LAYOUT_NAME_STR_SIZE}) NOT NULL,
    UNIQUE(project_uid, name),

    description TEXT,
    extra JSONB,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
"""

CREATE_TABLE_WIDGET = f"""
CREATE TABLE IF NOT EXISTS {TABLE_WIDGET} (
    uid SERIAL PRIMARY KEY,

    layout_uid INTEGER NOT NULL REFERENCES {TABLE_LAYOUT} (uid),
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

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
"""

# --------------------------
# Resource management tables
# --------------------------

CREATE_TABLE_PORT = f"""
CREATE TABLE IF NOT EXISTS {TABLE_PORT} (
    number INTEGER PRIMARY KEY,

    group_uid INTEGER REFERENCES {TABLE_GROUP} (uid),
    project_uid INTEGER REFERENCES {TABLE_PROJECT} (uid),
    task_uid INTEGER REFERENCES {TABLE_TASK} (uid),

    description TEXT,
    extra JSONB,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
"""

# -----------------
# Relational tables
# -----------------

CREATE_TABLE_GROUP_MEMBER = f"""
CREATE TABLE IF NOT EXISTS {TABLE_GROUP_MEMBER} (
    group_uid INTEGER NOT NULL REFERENCES {TABLE_GROUP} (uid),
    user_uid INTEGER NOT NULL REFERENCES {TABLE_USER} (uid),
    PRIMARY KEY(group_uid, user_uid),

    permission_uid INTEGER REFERENCES {TABLE_PERMISSION} (uid)
);
"""

CREATE_TABLE_PROJECT_MEMBER = f"""
CREATE TABLE IF NOT EXISTS {TABLE_PROJECT_MEMBER} (
    project_uid INTEGER NOT NULL REFERENCES {TABLE_PROJECT} (uid),
    user_uid INTEGER NOT NULL REFERENCES {TABLE_USER} (uid),
    PRIMARY KEY(project_uid, user_uid),

    permission_uid INTEGER REFERENCES {TABLE_PERMISSION} (uid)
);
"""

CREATE_TABLES = (
    # Base tables
    CREATE_TABLE_INFO,
    CREATE_TABLE_USER,
    CREATE_TABLE_GROUP,
    CREATE_TABLE_PERMISSION,
    CREATE_TABLE_PROJECT,
    CREATE_TABLE_TASK,
    CREATE_TABLE_LAYOUT,
    CREATE_TABLE_WIDGET,
    # Resource management tables
    CREATE_TABLE_PORT,
    # Relational tables
    CREATE_TABLE_GROUP_MEMBER,
    CREATE_TABLE_PROJECT_MEMBER,
)

# fmt: off
DROP_TABLE_INFO = f"DROP TABLE IF EXISTS {TABLE_INFO};"
DROP_TABLE_USER = f"DROP TABLE IF EXISTS {TABLE_USER};"
DROP_TABLE_GROUP = f"DROP TABLE IF EXISTS {TABLE_GROUP};"
DROP_TABLE_PERMISSION = f"DROP TABLE IF EXISTS {TABLE_PERMISSION};"
DROP_TABLE_PROJECT = f"DROP TABLE IF EXISTS {TABLE_PROJECT};"
DROP_TABLE_TASK = f"DROP TABLE IF EXISTS {TABLE_TASK};"
DROP_TABLE_LAYOUT = f"DROP TABLE IF EXISTS {TABLE_LAYOUT};"
DROP_TABLE_WIDGET = f"DROP TABLE IF EXISTS {TABLE_WIDGET};"
DROP_TABLE_PORT = f"DROP TABLE IF EXISTS {TABLE_PORT};"
DROP_TABLE_GROUP_MEMBER = f"DROP TABLE IF EXISTS {TABLE_GROUP_MEMBER};"
DROP_TABLE_PROJECT_MEMBER = f"DROP TABLE IF EXISTS {TABLE_PROJECT_MEMBER};"
# fmt: on

DROP_TABLES = (
    # Base tables
    DROP_TABLE_INFO,
    DROP_TABLE_USER,
    DROP_TABLE_GROUP,
    DROP_TABLE_PERMISSION,
    DROP_TABLE_PROJECT,
    DROP_TABLE_TASK,
    DROP_TABLE_LAYOUT,
    DROP_TABLE_WIDGET,
    # Resource management tables
    DROP_TABLE_PORT,
    # Relational tables
    DROP_TABLE_GROUP_MEMBER,
    DROP_TABLE_PROJECT_MEMBER,
)
