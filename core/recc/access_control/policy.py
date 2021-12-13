# -*- coding: utf-8 -*-

from typing import List
from enum import Enum, auto, unique
from recc.packet.rule import RawRule


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


def has_layout_read(rule: RawRule) -> None:
    if not rule.r_layout:
        raise PermissionError("You do not have read access to the layout")


def has_layout_write(rule: RawRule) -> None:
    if not rule.w_layout:
        raise PermissionError("You do not have write access to the layout")


def has_storage_read(rule: RawRule) -> None:
    if not rule.r_storage:
        raise PermissionError("You do not have read access to the storage")


def has_storage_write(rule: RawRule) -> None:
    if not rule.w_storage:
        raise PermissionError("You do not have write access to the storage")


def has_manager_read(rule: RawRule) -> None:
    if not rule.r_manager:
        raise PermissionError("You do not have read access to the manager")


def has_manager_write(rule: RawRule) -> None:
    if not rule.w_manager:
        raise PermissionError("You do not have write access to the manager")


def has_graph_read(rule: RawRule) -> None:
    if not rule.r_graph:
        raise PermissionError("You do not have read access to the graph")


def has_graph_write(rule: RawRule) -> None:
    if not rule.w_graph:
        raise PermissionError("You do not have write access to the graph")


def has_member_read(rule: RawRule) -> None:
    if not rule.r_member:
        raise PermissionError("You do not have read access to the member")


def has_member_write(rule: RawRule) -> None:
    if not rule.w_member:
        raise PermissionError("You do not have write access to the member")


def has_setting_read(rule: RawRule) -> None:
    if not rule.r_setting:
        raise PermissionError("You do not have read access to the setting")


def has_setting_write(rule: RawRule) -> None:
    if not rule.w_setting:
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


def test_policy(policy: Policy, rule: RawRule) -> None:
    assert policy is not Policy.HasFeatures
    assert policy in POLICY_TO_TESTER_MAP
    POLICY_TO_TESTER_MAP[policy](rule)


def test_policies(policies: List[Policy], rule: RawRule) -> None:
    for policy in policies:
        if policy == Policy.HasFeatures:
            continue
        test_policy(policy, rule)
