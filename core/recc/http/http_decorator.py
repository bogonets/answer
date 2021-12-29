# -*- coding: utf-8 -*-

from typing import Any, Union, List
from functools import wraps
from inspect import iscoroutinefunction
from recc.variables.annotation import ANNOTATION_PERMISSIONS, ANNOTATION_DOMAIN, Domain
from recc.variables.database import (
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_STORAGE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_STORAGE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_MANAGER_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_MANAGER_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_GRAPH_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_GRAPH_EDIT,
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


def _set_role(func, role: Union[int, str]):
    return _add_list_annotation(func, ANNOTATION_PERMISSIONS, role)


def has_layout_view(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW)


def has_layout_edit(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT)


def has_storage_view(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_STORAGE_VIEW)


def has_storage_edit(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_STORAGE_EDIT)


def has_manager_view(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_MANAGER_VIEW)


def has_manager_edit(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_MANAGER_EDIT)


def has_graph_view(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_GRAPH_VIEW)


def has_graph_edit(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_GRAPH_EDIT)


def has_member_view(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_MEMBER_VIEW)


def has_member_edit(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_MEMBER_EDIT)


def has_setting_view(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW)


def has_setting_edit(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT)


def has_delete(func):
    return _set_role(func, PERMISSION_SLUG_RECC_DOMAIN_DELETE)


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
