# -*- coding: utf-8 -*-

from typing import List
from enum import Enum, auto, unique
from recc.packet.role import RawRole


@unique
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

    HasFeatures = auto()


def has_layout_read(role: RawRole) -> None:
    if not role.r_layout:
        raise PermissionError("You do not have read access to the layout")


def has_layout_write(role: RawRole) -> None:
    if not role.w_layout:
        raise PermissionError("You do not have write access to the layout")


def has_storage_read(role: RawRole) -> None:
    if not role.r_storage:
        raise PermissionError("You do not have read access to the storage")


def has_storage_write(role: RawRole) -> None:
    if not role.w_storage:
        raise PermissionError("You do not have write access to the storage")


def has_manager_read(role: RawRole) -> None:
    if not role.r_manager:
        raise PermissionError("You do not have read access to the manager")


def has_manager_write(role: RawRole) -> None:
    if not role.w_manager:
        raise PermissionError("You do not have write access to the manager")


def has_graph_read(role: RawRole) -> None:
    if not role.r_graph:
        raise PermissionError("You do not have read access to the graph")


def has_graph_write(role: RawRole) -> None:
    if not role.w_graph:
        raise PermissionError("You do not have write access to the graph")


def has_member_read(role: RawRole) -> None:
    if not role.r_member:
        raise PermissionError("You do not have read access to the member")


def has_member_write(role: RawRole) -> None:
    if not role.w_member:
        raise PermissionError("You do not have write access to the member")


def has_setting_read(role: RawRole) -> None:
    if not role.r_setting:
        raise PermissionError("You do not have read access to the setting")


def has_setting_write(role: RawRole) -> None:
    if not role.w_setting:
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


def test_policy(policy: Policy, role: RawRole) -> None:
    assert policy is not Policy.HasFeatures
    assert policy in POLICY_TO_TESTER_MAP
    POLICY_TO_TESTER_MAP[policy](role)


def test_policies(policies: List[Policy], role: RawRole) -> None:
    for policy in policies:
        if policy == Policy.HasFeatures:
            continue
        test_policy(policy, role)
