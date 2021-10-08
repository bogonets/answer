# -*- coding: utf-8 -*-

from typing import List
from enum import Enum, auto
from recc.packet.permission import RawPermission


class Policy(Enum):
    HasLayoutRead = auto()
    HasLayoutWrite = auto()
    HasStorageRead = auto()
    HasStorageWrite = auto()
    HasManagerRead = auto()
    HasManagerWrite = auto()
    HasGraphRead = auto()
    HasGraphWrite = auto()
    HasMemberRead = auto()
    HasMemberWrite = auto()
    HasSettingRead = auto()
    HasSettingWrite = auto()


def has_layout_read(permission: RawPermission) -> None:
    if not permission.r_layout:
        raise PermissionError("You do not have read access to the layout")


def has_layout_write(permission: RawPermission) -> None:
    if not permission.w_layout:
        raise PermissionError("You do not have write access to the layout")


def has_storage_read(permission: RawPermission) -> None:
    if not permission.r_storage:
        raise PermissionError("You do not have read access to the storage")


def has_storage_write(permission: RawPermission) -> None:
    if not permission.w_storage:
        raise PermissionError("You do not have write access to the storage")


def has_manager_read(permission: RawPermission) -> None:
    if not permission.r_manager:
        raise PermissionError("You do not have read access to the manager")


def has_manager_write(permission: RawPermission) -> None:
    if not permission.w_manager:
        raise PermissionError("You do not have write access to the manager")


def has_graph_read(permission: RawPermission) -> None:
    if not permission.r_graph:
        raise PermissionError("You do not have read access to the graph")


def has_graph_write(permission: RawPermission) -> None:
    if not permission.w_graph:
        raise PermissionError("You do not have write access to the graph")


def has_member_read(permission: RawPermission) -> None:
    if not permission.r_member:
        raise PermissionError("You do not have read access to the member")


def has_member_write(permission: RawPermission) -> None:
    if not permission.w_member:
        raise PermissionError("You do not have write access to the member")


def has_setting_read(permission: RawPermission) -> None:
    if not permission.r_setting:
        raise PermissionError("You do not have read access to the setting")


def has_setting_write(permission: RawPermission) -> None:
    if not permission.w_setting:
        raise PermissionError("You do not have write access to the setting")


POLICY_TO_TESTER_MAP = {
    Policy.HasLayoutRead: has_layout_read,
    Policy.HasLayoutWrite: has_layout_write,
    Policy.HasStorageRead: has_storage_read,
    Policy.HasStorageWrite: has_storage_write,
    Policy.HasManagerRead: has_manager_read,
    Policy.HasManagerWrite: has_manager_write,
    Policy.HasGraphRead: has_graph_read,
    Policy.HasGraphWrite: has_graph_write,
    Policy.HasMemberRead: has_member_read,
    Policy.HasMemberWrite: has_member_write,
    Policy.HasSettingRead: has_setting_read,
    Policy.HasSettingWrite: has_setting_write,
}


def test_policy(policy: Policy, permission: RawPermission) -> None:
    assert policy in POLICY_TO_TESTER_MAP
    POLICY_TO_TESTER_MAP[policy](permission)


def test_policies(policies: List[Policy], permission: RawPermission) -> None:
    for policy in policies:
        test_policy(policy, permission)
