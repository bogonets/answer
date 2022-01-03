# -*- coding: utf-8 -*-

from typing import List, Union, Iterable, Optional
from recc.variables.database import (
    TABLE_ROLE,
    TABLE_PERMISSION,
    TABLE_ROLE_PERMISSION,
    ROLE_SLUG_OWNER,
    ROLE_SLUG_MAINTAINER,
    ROLE_SLUG_DEVELOPER,
    ROLE_SLUG_REPORTER,
    ROLE_SLUG_GUEST,
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

_SAFE_INSERT_ROLE_PERMISSION_BY_PERMISSION_SLUG_FORMAT = f"""
INSERT INTO {TABLE_ROLE_PERMISSION} (
    role_uid,
    permission_uid
) SELECT
    {{role_uid}},
    (SELECT uid FROM {TABLE_PERMISSION} WHERE slug='{{permission_slug}}')
WHERE
    NOT EXISTS (
        SELECT *
        FROM {TABLE_ROLE_PERMISSION}
        WHERE
            role_uid={{role_uid}}
            AND permission_uid=(
                SELECT uid
                FROM {TABLE_PERMISSION}
                WHERE slug='{{permission_slug}}'
            )
    );
"""

_SAFE_INSERT_ROLE_PERMISSION_BY_ONLY_SLUG_FORMAT = f"""
INSERT INTO {TABLE_ROLE_PERMISSION} (
    role_uid,
    permission_uid
) SELECT
    (SELECT uid FROM {TABLE_ROLE} WHERE slug='{{role_slug}}'),
    (SELECT uid FROM {TABLE_PERMISSION} WHERE slug='{{permission_slug}}')
WHERE
    NOT EXISTS (
        SELECT *
        FROM {TABLE_ROLE_PERMISSION}
        WHERE
            role_uid=(
                SELECT uid
                FROM {TABLE_ROLE}
                WHERE slug='{{role_slug}}'
            )
            AND permission_uid=(
                SELECT uid
                FROM {TABLE_PERMISSION}
                WHERE slug='{{permission_slug}}'
            )
    );
"""


def delete_role_permission_by_role_uid(role_uid: int) -> str:
    return _DELETE_ROLE_PERMISSION_BY_ROLE_UID_FORMAT.format(role_uid=role_uid)


def safe_insert_role_permission_by_slug(
    role_uid_or_slug: Union[int, str],
    permission_slug: str,
) -> str:
    if isinstance(role_uid_or_slug, int):
        return _SAFE_INSERT_ROLE_PERMISSION_BY_PERMISSION_SLUG_FORMAT.format(
            role_uid=role_uid_or_slug,
            permission_slug=permission_slug,
        )
    else:
        assert isinstance(role_uid_or_slug, str)
        return _SAFE_INSERT_ROLE_PERMISSION_BY_ONLY_SLUG_FORMAT.format(
            role_slug=role_uid_or_slug,
            permission_slug=permission_slug,
        )


def safe_insert_role_permissions(**kwargs: Iterable[str]) -> List[str]:
    result = list()
    for role_slug, permissions in kwargs.items():
        assert isinstance(role_slug, str)
        for permission_slug in permissions:
            assert isinstance(permission_slug, str)
            query = safe_insert_role_permission_by_slug(role_slug, permission_slug)
            result.append(query)
    return result


def safe_insert_role_permissions_for_defaults(
    owner: Optional[Iterable[str]] = None,
    maintainer: Optional[Iterable[str]] = None,
    developer: Optional[Iterable[str]] = None,
    reporter: Optional[Iterable[str]] = None,
    guest: Optional[Iterable[str]] = None,
) -> List[str]:
    permissions = dict()
    if owner:
        permissions[ROLE_SLUG_OWNER] = owner
    if maintainer:
        permissions[ROLE_SLUG_MAINTAINER] = maintainer
    if developer:
        permissions[ROLE_SLUG_DEVELOPER] = developer
    if reporter:
        permissions[ROLE_SLUG_REPORTER] = reporter
    if guest:
        permissions[ROLE_SLUG_GUEST] = guest
    return safe_insert_role_permissions(**permissions)


def _default_safe_insert_role_permissions() -> List[str]:
    return safe_insert_role_permissions(**DEFAULT_ROLE_PERMISSIONS_MAP)


DEFAULT_INSERT_ROLE_PERMISSIONS = _default_safe_insert_role_permissions()
