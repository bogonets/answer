# -*- coding: utf-8 -*-

from typing import List, Union
from recc.variables.database import (
    TABLE_ROLE,
    TABLE_PERMISSION,
    TABLE_ROLE_PERMISSION,
    DEFAULT_ROLE_PERMISSIONS_MAP,
)

INSERT_ROLE_PERMISSION = f"""
INSERT INTO {TABLE_ROLE_PERMISSION} (
    role_uid,
    permission_uid
) VALUES (
    $1,
    $2
);
"""

DELETE_ROLE_PERMISSION = f"""
DELETE FROM {TABLE_ROLE_PERMISSION}
WHERE role_uid=$1 AND permission_uid=$2;
"""

SELECT_ROLE_PERMISSION_ALL = f"""
SELECT *
FROM {TABLE_ROLE_PERMISSION};
"""

SELECT_ROLE_PERMISSION_BY_ROLE_UID = f"""
SELECT *
FROM {TABLE_ROLE_PERMISSION}
WHERE role_uid=$1;
"""

_DELETE_ROLE_PERMISSION_BY_ROLE_UID_FORMAT = f"""
DELETE FROM {TABLE_ROLE_PERMISSION}
WHERE role_uid={{role_uid}};
"""

_INSERT_ROLE_PERMISSION_BY_PERMISSION_SLUG_FORMAT = f"""
INSERT INTO {TABLE_ROLE_PERMISSION} (
    role_uid,
    permission_uid
) VALUES (
    {{role_uid}},
    (SELECT uid FROM {TABLE_PERMISSION} WHERE slug='{{permission_slug}}')
);
"""

_INSERT_ROLE_PERMISSION_BY_ONLY_SLUG_FORMAT = f"""
INSERT INTO {TABLE_ROLE_PERMISSION} (
    role_uid,
    permission_uid
) VALUES (
    (SELECT uid FROM {TABLE_ROLE} WHERE slug='{{role_slug}}'),
    (SELECT uid FROM {TABLE_PERMISSION} WHERE slug='{{permission_slug}}')
);
"""


def delete_role_permission_by_role_uid(role_uid: int) -> str:
    return _DELETE_ROLE_PERMISSION_BY_ROLE_UID_FORMAT.format(role_uid=role_uid)


def insert_role_permission_by_slug(
    role_uid_or_slug: Union[int, str],
    permission_slug: str,
) -> str:
    if isinstance(role_uid_or_slug, int):
        return _INSERT_ROLE_PERMISSION_BY_PERMISSION_SLUG_FORMAT.format(
            role_uid=role_uid_or_slug,
            permission_slug=permission_slug,
        )
    else:
        assert isinstance(role_uid_or_slug, str)
        return _INSERT_ROLE_PERMISSION_BY_ONLY_SLUG_FORMAT.format(
            role_slug=role_uid_or_slug,
            permission_slug=permission_slug,
        )


def _default_insert_role_permissions() -> List[str]:
    result = list()
    for role_slug, permissions in DEFAULT_ROLE_PERMISSIONS_MAP.items():
        assert isinstance(role_slug, str)
        for permission_slug in permissions:
            assert isinstance(permission_slug, str)
            query = insert_role_permission_by_slug(role_slug, permission_slug)
            result.append(query)
    return result


DEFAULT_INSERT_ROLE_PERMISSIONS = _default_insert_role_permissions()
