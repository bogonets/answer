# -*- coding: utf-8 -*-

from typing import Any
from functools import wraps
from inspect import iscoroutinefunction
from recc.access_control.policy import Policy
from recc.variables.annotation import (
    ANNOTATION_GROUP_RULES,
    ANNOTATION_PROJECT_RULES,
    ANNOTATION_FEATURE_RULES,
    ANNOTATION_ADMIN_RULES,
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


def _add_annotation(func, annotation: str, data: Any):
    att = getattr(func, annotation, list())
    if isinstance(data, list):
        setattr(func, annotation, att + list(data))
    else:
        setattr(func, annotation, att + [data])
    return _wrapper(func)


def _set_group_rule(func, policy: Policy):
    return _add_annotation(func, ANNOTATION_GROUP_RULES, policy)


def _set_project_rule(func, policy: Policy):
    return _add_annotation(func, ANNOTATION_PROJECT_RULES, policy)


def has_group_layout_read(func):
    return _set_group_rule(func, Policy.HasManagerRead)


def has_group_layout_write(func):
    return _set_group_rule(func, Policy.HasManagerWrite)


def has_group_storage_read(func):
    return _set_group_rule(func, Policy.HasStorageRead)


def has_group_storage_write(func):
    return _set_group_rule(func, Policy.HasStorageWrite)


def has_group_manager_read(func):
    return _set_group_rule(func, Policy.HasManagerRead)


def has_group_manager_write(func):
    return _set_group_rule(func, Policy.HasManagerWrite)


def has_group_graph_read(func):
    return _set_group_rule(func, Policy.HasGraphRead)


def has_group_graph_write(func):
    return _set_group_rule(func, Policy.HasGraphWrite)


def has_group_member_read(func):
    return _set_group_rule(func, Policy.HasMemberRead)


def has_group_member_write(func):
    return _set_group_rule(func, Policy.HasMemberWrite)


def has_group_setting_read(func):
    return _set_group_rule(func, Policy.HasSettingRead)


def has_group_setting_write(func):
    return _set_group_rule(func, Policy.HasSettingWrite)


def has_project_layout_read(func):
    return _set_project_rule(func, Policy.HasManagerRead)


def has_project_layout_write(func):
    return _set_project_rule(func, Policy.HasManagerWrite)


def has_project_storage_read(func):
    return _set_project_rule(func, Policy.HasStorageRead)


def has_project_storage_write(func):
    return _set_project_rule(func, Policy.HasStorageWrite)


def has_project_manager_read(func):
    return _set_project_rule(func, Policy.HasManagerRead)


def has_project_manager_write(func):
    return _set_project_rule(func, Policy.HasManagerWrite)


def has_project_graph_read(func):
    return _set_project_rule(func, Policy.HasGraphRead)


def has_project_graph_write(func):
    return _set_project_rule(func, Policy.HasGraphWrite)


def has_project_member_read(func):
    return _set_project_rule(func, Policy.HasMemberRead)


def has_project_member_write(func):
    return _set_project_rule(func, Policy.HasMemberWrite)


def has_project_setting_read(func):
    return _set_project_rule(func, Policy.HasSettingRead)


def has_project_setting_write(func):
    return _set_project_rule(func, Policy.HasSettingWrite)


def has_features(*args):
    def _wrap(func):
        return _add_annotation(func, ANNOTATION_FEATURE_RULES, list(args))

    return _wrap


def has_administrator(func):
    setattr(func, ANNOTATION_ADMIN_RULES, True)
    return _wrapper(func)
