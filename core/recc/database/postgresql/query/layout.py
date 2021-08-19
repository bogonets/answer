# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_LAYOUT


##########
# INSERT #
##########

INSERT_LAYOUT = f"""
INSERT INTO {TABLE_LAYOUT} (
    project_uid,
    name,
    description,
    extra,
    created_at
) VALUES (
    $1, $2, $3, $4, $5
) RETURNING uid;
"""

##########
# UPDATE #
##########

UPDATE_LAYOUT_DESCRIPTION_BY_UID = f"""
UPDATE {TABLE_LAYOUT}
SET description=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_LAYOUT_DESCRIPTION_BY_PROJECT_UID_AND_NAME = f"""
UPDATE {TABLE_LAYOUT}
SET description=$3, updated_at=$4
WHERE project_uid=$1 AND name LIKE $2;
"""

UPDATE_LAYOUT_EXTRA_BY_UID = f"""
UPDATE {TABLE_LAYOUT}
SET extra=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_LAYOUT_EXTRA_BY_PROJECT_UID_AND_NAME = f"""
UPDATE {TABLE_LAYOUT}
SET extra=$3, updated_at=$4
WHERE project_uid=$1 AND name LIKE $2;
"""

##########
# DELETE #
##########

DELETE_LAYOUT_BY_UID = f"""
DELETE FROM {TABLE_LAYOUT}
WHERE uid=$1;
"""

DELETE_LAYOUT_BY_PROJECT_UID_AND_NAME = f"""
DELETE FROM {TABLE_LAYOUT}
WHERE project_uid=$1 AND name LIKE $2;
"""

##########
# SELECT #
##########

SELECT_LAYOUT_BY_UID = f"""
SELECT project_uid, name, description, extra, created_at, updated_at
FROM {TABLE_LAYOUT}
WHERE uid=$1;
"""

SELECT_LAYOUT_BY_PROJECT_ID_AND_NAME = f"""
SELECT uid, description, extra, created_at, updated_at
FROM {TABLE_LAYOUT}
WHERE project_uid=$1 AND name LIKE $2;
"""

SELECT_LAYOUT_BY_PROJECT_ID = f"""
SELECT uid, name, description, extra, created_at, updated_at
FROM {TABLE_LAYOUT}
WHERE project_uid=$1;
"""
