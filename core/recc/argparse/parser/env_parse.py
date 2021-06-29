# -*- coding: utf-8 -*-

from typing import Dict, Optional
from argparse import Namespace
from recc.system.environ import get_os_envs_dict


def normalize_env_key(key: str, remove_prefix: Optional[str] = None) -> str:
    if remove_prefix and key.startswith(remove_prefix):
        remove_prefix_size = len(remove_prefix)
        key = key[remove_prefix_size:]
    return key.strip().lower().replace("-", "_")


def get_namespace_by_envs(
    envs: Dict[str, str],
    start_prefix: Optional[str] = None,
) -> Namespace:
    if start_prefix:
        filtered_envs = dict()
        for k, v in envs.items():
            if k.startswith(start_prefix):
                filtered_envs[k] = v
    else:
        filtered_envs = envs

    normalized_envs = dict()
    for k, v in filtered_envs.items():
        normalized_envs[normalize_env_key(k, start_prefix)] = v

    return Namespace(**normalized_envs)


def get_namespace_by_os_envs(start_prefix: Optional[str] = None) -> Namespace:
    return get_namespace_by_envs(get_os_envs_dict(), start_prefix)
