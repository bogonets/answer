# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_PIP

INSERT_PIP = f"""
INSERT INTO {TABLE_PIP} (
    domain,
    name,
    file,
    hash_method,
    hash_value
) VALUES (
    $1, $2, $3, $4, $5
);
"""

DELETE_PIP_BY_DOMAIN_AND_NAME = f"""
DELETE FROM {TABLE_PIP}
WHERE domain=$1 AND name=$2;
"""

SELECT_PIP_BY_DOMAIN_AND_NAME = f"""
SELECT *
FROM {TABLE_PIP}
WHERE domain=$1 AND name=$2;
"""

SELECT_PIP_ALL = f"""
SELECT *
FROM {TABLE_PIP};
"""
