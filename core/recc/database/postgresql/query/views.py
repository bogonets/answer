# -*- coding: utf-8 -*-

from recc.variables.database import (
    TABLE_INFO,
    TABLE_USER,
    TABLE_GROUP,
    TABLE_PROJECT,
    TABLE_TASK,
    TABLE_LAYOUT,
    TABLE_WIDGET,
    TABLE_GROUP_MEMBER,
    VIEW_INFO_DB_VERSION,
    VIEW_USER_GROUP,
    VIEW_USER_ADMIN,
    VIEW_USER_ADMIN_COUNT,
    VIEW_USER_PROJECT,
    VIEW_USER_TASK,
    VIEW_USER_LAYOUT,
    VIEW_USER_WIDGET,
    VIEW_GROUP_PROJECT,
    VIEW_GROUP_TASK,
    VIEW_GROUP_LAYOUT,
    VIEW_GROUP_WIDGET,
    VIEW_PROJECT_TASK,
    VIEW_PROJECT_LAYOUT,
    VIEW_PROJECT_WIDGET,
    VIEW_LAYOUT_WIDGET,
    RECC_DB_VERSION_KEY,
)

CREATE_VIEW_INFO_DB_VERSION = f"""
CREATE OR REPLACE VIEW {VIEW_INFO_DB_VERSION}
AS SELECT
    value AS version
FROM
    {TABLE_INFO}
WHERE
    key LIKE '{RECC_DB_VERSION_KEY}';
"""

CREATE_VIEW_USER_ADMIN = f"""
CREATE OR REPLACE VIEW {VIEW_USER_ADMIN}
AS SELECT
    uid, username, email
FROM
    {TABLE_USER}
WHERE
    is_admin=TRUE;
"""

CREATE_VIEW_USER_ADMIN_COUNT = f"""
CREATE OR REPLACE VIEW {VIEW_USER_ADMIN_COUNT}
AS SELECT
    count(uid) AS count
FROM
    {TABLE_USER}
WHERE
    is_admin=TRUE;
"""

CREATE_VIEW_USER_GROUP = f"""
CREATE OR REPLACE VIEW {VIEW_USER_GROUP}
AS SELECT
    u.uid AS u_uid,
    u.username AS u_name,
    u.email AS u_email,
    g.uid AS g_uid,
    g.name AS g_name,
    g.description AS g_description,
    g.extra AS g_extra,
    g.created_at AS g_created_at,
    g.updated_at AS g_updated_at
FROM
    {TABLE_USER} u
    INNER JOIN {TABLE_GROUP_MEMBER} gm ON gm.user_uid=u.uid
    INNER JOIN {TABLE_GROUP} g ON g.uid=gm.group_uid;
"""

CREATE_VIEW_USER_PROJECT = f"""
CREATE OR REPLACE VIEW {VIEW_USER_PROJECT}
AS SELECT
    u.uid AS u_uid,
    u.username AS u_name,
    u.email AS u_email,
    g.uid AS g_uid,
    g.name AS g_name,
    p.uid AS p_uid,
    p.name AS p_name,
    p.description AS p_description,
    p.extra AS p_extra,
    p.created_at AS p_created_at,
    p.updated_at AS p_updated_at
FROM
    {TABLE_USER} u
    INNER JOIN {TABLE_GROUP_MEMBER} gm ON gm.user_uid=u.uid
    INNER JOIN {TABLE_GROUP} g ON g.uid=gm.group_uid
    INNER JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid;
"""

CREATE_VIEW_USER_TASK = f"""
CREATE OR REPLACE VIEW {VIEW_USER_TASK}
AS SELECT
    u.uid AS u_uid,
    u.username AS u_name,
    u.email AS u_email,
    g.uid AS g_uid,
    g.name AS g_name,
    p.uid AS p_uid,
    p.name AS p_name,
    t.uid AS t_uid,
    t.name AS t_name,
    t.description AS t_description,
    t.extra AS t_extra,
    t.created_at AS t_created_at,
    t.updated_at AS t_updated_at
FROM
    {TABLE_USER} u
    INNER JOIN {TABLE_GROUP_MEMBER} gm ON gm.user_uid=u.uid
    INNER JOIN {TABLE_GROUP} g ON g.uid=gm.group_uid
    INNER JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid
    INNER JOIN {TABLE_TASK} t ON t.project_uid=p.uid;
"""

CREATE_VIEW_USER_LAYOUT = f"""
CREATE OR REPLACE VIEW {VIEW_USER_LAYOUT}
AS SELECT
    u.uid AS u_uid,
    u.username AS u_name,
    u.email AS u_email,
    g.uid AS g_uid,
    g.name AS g_name,
    p.uid AS p_uid,
    p.name AS p_name,
    l.uid AS l_uid,
    l.name AS l_name,
    l.description AS l_description,
    l.extra AS l_extra,
    l.created_at AS l_created_at,
    l.updated_at AS l_updated_at
FROM
    {TABLE_USER} u
    INNER JOIN {TABLE_GROUP_MEMBER} gm ON gm.user_uid=u.uid
    INNER JOIN {TABLE_GROUP} g ON g.uid=gm.group_uid
    INNER JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid
    INNER JOIN {TABLE_LAYOUT} l ON l.project_uid=p.uid;
"""

CREATE_VIEW_USER_WIDGET = f"""
CREATE OR REPLACE VIEW {VIEW_USER_WIDGET}
AS SELECT
    u.uid AS u_uid,
    u.username AS u_name,
    u.email AS u_email,
    g.uid AS g_uid,
    g.name AS g_name,
    p.uid AS p_uid,
    p.name AS p_name,
    l.uid AS l_uid,
    l.name AS l_name,
    w.uid AS w_uid,
    w.name AS w_name,
    w.description AS w_description,
    w.extra AS w_extra,
    w.type_name AS w_type_name,
    w.pos_x1 AS w_pos_x1,
    w.pos_y1 AS w_pos_y1,
    w.pos_x2 AS w_pos_x2,
    w.pos_y2 AS w_pos_y2,
    w.z_order AS w_z_order,
    w.created_at AS w_created_at,
    w.updated_at AS w_updated_at
FROM
    {TABLE_USER} u
    INNER JOIN {TABLE_GROUP_MEMBER} gm ON gm.user_uid=u.uid
    INNER JOIN {TABLE_GROUP} g ON g.uid=gm.group_uid
    INNER JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid
    INNER JOIN {TABLE_LAYOUT} l ON l.project_uid=p.uid
    INNER JOIN {TABLE_WIDGET} w ON w.layout_uid=l.uid;
"""

CREATE_VIEW_GROUP_PROJECT = f"""
CREATE OR REPLACE VIEW {VIEW_GROUP_PROJECT}
AS SELECT
    g.uid AS g_uid,
    g.name AS g_name,
    p.uid AS p_uid,
    p.name AS p_name,
    p.description AS p_description,
    p.extra AS p_extra,
    p.created_at AS p_created_at,
    p.updated_at AS p_updated_at
FROM
    {TABLE_GROUP} g
    INNER JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid;
"""

CREATE_VIEW_GROUP_TASK = f"""
CREATE OR REPLACE VIEW {VIEW_GROUP_TASK}
AS SELECT
    g.uid AS g_uid,
    g.name AS g_name,
    p.uid AS p_uid,
    p.name AS p_name,
    t.uid AS t_uid,
    t.name AS t_name,
    t.description AS t_description,
    t.extra AS t_extra,
    t.created_at AS t_created_at,
    t.updated_at AS t_updated_at
FROM
    {TABLE_GROUP} g
    INNER JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid
    INNER JOIN {TABLE_TASK} t ON t.project_uid=p.uid;
"""

CREATE_VIEW_GROUP_LAYOUT = f"""
CREATE OR REPLACE VIEW {VIEW_GROUP_LAYOUT}
AS SELECT
    g.uid AS g_uid,
    g.name AS g_name,
    p.uid AS p_uid,
    p.name AS p_name,
    l.uid AS l_uid,
    l.name AS l_name,
    l.description AS l_description,
    l.extra AS l_extra,
    l.created_at AS l_created_at,
    l.updated_at AS l_updated_at
FROM
    {TABLE_GROUP} g
    INNER JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid
    INNER JOIN {TABLE_LAYOUT} l ON l.project_uid=p.uid;
"""

CREATE_VIEW_GROUP_WIDGET = f"""
CREATE OR REPLACE VIEW {VIEW_GROUP_WIDGET}
AS SELECT
    g.uid AS g_uid,
    g.name AS g_name,
    p.uid AS p_uid,
    p.name AS p_name,
    l.uid AS l_uid,
    l.name AS l_name,
    w.uid AS w_uid,
    w.name AS w_name,
    w.description AS w_description,
    w.extra AS w_extra,
    w.type_name AS w_type_name,
    w.pos_x1 AS w_pos_x1,
    w.pos_y1 AS w_pos_y1,
    w.pos_x2 AS w_pos_x2,
    w.pos_y2 AS w_pos_y2,
    w.z_order AS w_z_order,
    w.created_at AS w_created_at,
    w.updated_at AS w_updated_at
FROM
    {TABLE_GROUP} g
    INNER JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid
    INNER JOIN {TABLE_LAYOUT} l ON l.project_uid=p.uid
    INNER JOIN {TABLE_WIDGET} w ON w.layout_uid=l.uid;
"""

CREATE_VIEW_PROJECT_TASK = f"""
CREATE OR REPLACE VIEW {VIEW_PROJECT_TASK}
AS SELECT
    p.uid AS p_uid,
    p.name AS p_name,
    t.uid AS t_uid,
    t.name AS t_name,
    t.description AS t_description,
    t.extra AS t_extra,
    t.created_at AS t_created_at,
    t.updated_at AS t_updated_at
FROM
    {TABLE_PROJECT} p
    INNER JOIN {TABLE_TASK} t ON t.project_uid=p.uid;
"""

CREATE_VIEW_PROJECT_LAYOUT = f"""
CREATE OR REPLACE VIEW {VIEW_PROJECT_LAYOUT}
AS SELECT
    p.uid AS p_uid,
    p.name AS p_name,
    l.uid AS l_uid,
    l.name AS l_name,
    l.description AS l_description,
    l.extra AS l_extra,
    l.created_at AS l_created_at,
    l.updated_at AS l_updated_at
FROM
    {TABLE_PROJECT} p
    INNER JOIN {TABLE_LAYOUT} l ON l.project_uid=p.uid;
"""

CREATE_VIEW_PROJECT_WIDGET = f"""
CREATE OR REPLACE VIEW {VIEW_PROJECT_WIDGET}
AS SELECT
    p.uid AS p_uid,
    p.name AS p_name,
    l.uid AS l_uid,
    l.name AS l_name,
    w.uid AS w_uid,
    w.name AS w_name,
    w.description AS w_description,
    w.extra AS w_extra,
    w.type_name AS w_type_name,
    w.pos_x1 AS w_pos_x1,
    w.pos_y1 AS w_pos_y1,
    w.pos_x2 AS w_pos_x2,
    w.pos_y2 AS w_pos_y2,
    w.z_order AS w_z_order,
    w.created_at AS w_created_at,
    w.updated_at AS w_updated_at
FROM
    {TABLE_PROJECT} p
    INNER JOIN {TABLE_LAYOUT} l ON l.project_uid=p.uid
    INNER JOIN {TABLE_WIDGET} w ON w.layout_uid=l.uid;
"""

CREATE_VIEW_LAYOUT_WIDGET = f"""
CREATE OR REPLACE VIEW {VIEW_LAYOUT_WIDGET}
AS SELECT
    l.uid AS l_uid,
    l.name AS l_name,
    w.uid AS w_uid,
    w.name AS w_name,
    w.description AS w_description,
    w.extra AS w_extra,
    w.type_name AS w_type_name,
    w.pos_x1 AS w_pos_x1,
    w.pos_y1 AS w_pos_y1,
    w.pos_x2 AS w_pos_x2,
    w.pos_y2 AS w_pos_y2,
    w.z_order AS w_z_order,
    w.created_at AS w_created_at,
    w.updated_at AS w_updated_at
FROM
    {TABLE_LAYOUT} l
    INNER JOIN {TABLE_WIDGET} w ON w.layout_uid=l.uid;
"""

CREATE_VIEWS = (
    CREATE_VIEW_INFO_DB_VERSION,
    CREATE_VIEW_USER_ADMIN,
    CREATE_VIEW_USER_ADMIN_COUNT,
    CREATE_VIEW_USER_GROUP,
    CREATE_VIEW_USER_PROJECT,
    CREATE_VIEW_USER_TASK,
    CREATE_VIEW_USER_LAYOUT,
    CREATE_VIEW_USER_WIDGET,
    CREATE_VIEW_GROUP_PROJECT,
    CREATE_VIEW_GROUP_TASK,
    CREATE_VIEW_GROUP_LAYOUT,
    CREATE_VIEW_GROUP_WIDGET,
    CREATE_VIEW_PROJECT_TASK,
    CREATE_VIEW_PROJECT_LAYOUT,
    CREATE_VIEW_PROJECT_WIDGET,
    CREATE_VIEW_LAYOUT_WIDGET,
)

DROP_VIEW_INFO_VERSION = f"DROP VIEW IF EXISTS {VIEW_INFO_DB_VERSION};"
DROP_VIEW_USER_GROUP = f"DROP VIEW IF EXISTS {VIEW_USER_GROUP};"
DROP_VIEW_USER_ADMIN = f"DROP VIEW IF EXISTS {VIEW_USER_ADMIN};"
DROP_VIEW_USER_ADMIN_COUNT = f"DROP VIEW IF EXISTS {VIEW_USER_ADMIN_COUNT};"
DROP_VIEW_USER_PROJECT = f"DROP VIEW IF EXISTS {VIEW_USER_PROJECT};"
DROP_VIEW_USER_TASK = f"DROP VIEW IF EXISTS {VIEW_USER_TASK};"
DROP_VIEW_USER_LAYOUT = f"DROP VIEW IF EXISTS {VIEW_USER_LAYOUT};"
DROP_VIEW_USER_WIDGET = f"DROP VIEW IF EXISTS {VIEW_USER_WIDGET};"
DROP_VIEW_GROUP_PROJECT = f"DROP VIEW IF EXISTS {VIEW_GROUP_PROJECT};"
DROP_VIEW_GROUP_TASK = f"DROP VIEW IF EXISTS {VIEW_GROUP_TASK};"
DROP_VIEW_GROUP_LAYOUT = f"DROP VIEW IF EXISTS {VIEW_GROUP_LAYOUT};"
DROP_VIEW_GROUP_WIDGET = f"DROP VIEW IF EXISTS {VIEW_GROUP_WIDGET};"
DROP_VIEW_PROJECT_TASK = f"DROP VIEW IF EXISTS {VIEW_PROJECT_TASK};"
DROP_VIEW_PROJECT_LAYOUT = f"DROP VIEW IF EXISTS {VIEW_PROJECT_LAYOUT};"
DROP_VIEW_PROJECT_WIDGET = f"DROP VIEW IF EXISTS {VIEW_PROJECT_WIDGET};"
DROP_VIEW_LAYOUT_WIDGET = f"DROP VIEW IF EXISTS {VIEW_LAYOUT_WIDGET};"

DROP_VIEWS = (
    DROP_VIEW_INFO_VERSION,
    DROP_VIEW_USER_GROUP,
    DROP_VIEW_USER_ADMIN,
    DROP_VIEW_USER_ADMIN_COUNT,
    DROP_VIEW_USER_PROJECT,
    DROP_VIEW_USER_TASK,
    DROP_VIEW_USER_LAYOUT,
    DROP_VIEW_USER_WIDGET,
    DROP_VIEW_GROUP_PROJECT,
    DROP_VIEW_GROUP_TASK,
    DROP_VIEW_GROUP_LAYOUT,
    DROP_VIEW_GROUP_WIDGET,
    DROP_VIEW_PROJECT_TASK,
    DROP_VIEW_PROJECT_LAYOUT,
    DROP_VIEW_PROJECT_WIDGET,
    DROP_VIEW_LAYOUT_WIDGET,
)
