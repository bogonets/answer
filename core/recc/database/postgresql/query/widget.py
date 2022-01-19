# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_WIDGET

INSERT_WIDGET = f"""
INSERT INTO {TABLE_WIDGET} (
    layout_uid,
    name,
    description,
    extra,
    created_at
) VALUES (
    $1, $2, $3, $4, $5
) RETURNING uid;
"""

UPDATE_WIDGET_DESCRIPTION_BY_UID = f"""
UPDATE {TABLE_WIDGET}
SET description=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_WIDGET_DESCRIPTION_BY_LAYOUT_UID_AND_NAME = f"""
UPDATE {TABLE_WIDGET}
SET description=$3, updated_at=$4
WHERE layout_uid=$1 AND name=$2;
"""

UPDATE_WIDGET_EXTRA_BY_UID = f"""
UPDATE {TABLE_WIDGET}
SET extra=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_WIDGET_EXTRA_BY_LAYOUT_UID_AND_NAME = f"""
UPDATE {TABLE_WIDGET}
SET extra=$3, updated_at=$4
WHERE layout_uid=$1 AND name=$2;
"""

DELETE_WIDGET_BY_UID = f"""
DELETE FROM {TABLE_WIDGET}
WHERE uid=$1;
"""

DELETE_WIDGET_BY_LAYOUT_UID_AND_NAME = f"""
DELETE FROM {TABLE_WIDGET}
WHERE layout_uid=$1 AND name=$2;
"""

SELECT_WIDGET_BY_UID = f"""
SELECT *
FROM {TABLE_WIDGET}
WHERE uid=$1;
"""

SELECT_WIDGET_BY_LAYOUT_ID_AND_NAME = f"""
SELECT *
FROM {TABLE_WIDGET}
WHERE layout_uid=$1 AND name=$2;
"""

SELECT_WIDGET_BY_LAYOUT_ID = f"""
SELECT *
FROM {TABLE_WIDGET}
WHERE layout_uid=$1;
"""
