# -*- coding: utf-8 -*-

from typing import Any, Union, List
from functools import wraps
from inspect import iscoroutinefunction
from recc.variables.annotation import ANNOTATION_PERMISSIONS, ANNOTATION_DOMAIN, Domain
from recc.variables.database import (
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_VP_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_VP_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_DELETE,
)


def _wrapper(func):
    if iscoroutinefunction(func):

        @wraps(func)
        async def _wrap1(*args, **kwargs):
            return await func(*args, **kwargs)

        return _wrap1
    else:

        @wraps(func)
        def _wrap2(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrap2


def _add_list_annotation(func, annotation: str, data: Any):
    att = getattr(func, annotation, list())
    if isinstance(data, list):
        setattr(func, annotation, att + list(data))
    else:
        setattr(func, annotation, att + [data])
    return _wrapper(func)


def _set_annotation(func, annotation: str, data: Any):
    setattr(func, annotation, data)
    return _wrapper(func)


def has_role(func, role: Union[int, str]):
    return _add_list_annotation(func, ANNOTATION_PERMISSIONS, role)


def has_layout_view(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW)


def has_layout_edit(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT)


def has_file_view(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_FILE_VIEW)


def has_file_edit(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_FILE_EDIT)


def has_table_view(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_TABLE_VIEW)


def has_table_edit(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_TABLE_EDIT)


def has_task_view(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_TASK_VIEW)


def has_task_edit(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_TASK_EDIT)


def has_vp_view(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_VP_VIEW)


def has_vp_edit(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_VP_EDIT)


def has_member_view(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_MEMBER_VIEW)


def has_member_edit(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_MEMBER_EDIT)


def has_setting_view(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW)


def has_setting_edit(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT)


def has_delete(func):
    return has_role(func, PERMISSION_SLUG_RECC_DOMAIN_DELETE)


def domain_group(func):
    return _set_annotation(func, ANNOTATION_DOMAIN, Domain.Group)


def domain_project(func):
    return _set_annotation(func, ANNOTATION_DOMAIN, Domain.Project)


def object_to_permissions(obj: Any) -> List[Union[int, str]]:
    if isinstance(obj, int):
        return [obj]
    elif isinstance(obj, str):
        return [obj]
    elif isinstance(obj, set) or isinstance(obj, list):
        result = list()
        for oo in obj:
            for o in object_to_permissions(oo):
                result.append(o)
        return result
    else:
        raise RuntimeError(f"Unsupported permission type: {type(obj).__name__}")
