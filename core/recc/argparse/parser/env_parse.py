# -*- coding: utf-8 -*-

from typing import Dict, Optional
from argparse import Namespace
from recc.system.environ import get_os_envs_dict


def normalize_config_key(
    key: str,
    remove_prefix: Optional[str] = None,
    remove_suffix: Optional[str] = None,
) -> str:
    buffer = key
    if remove_prefix and buffer.startswith(remove_prefix):
        remove_prefix_size = len(remove_prefix)
        buffer = buffer[remove_prefix_size:]
    if remove_suffix and buffer.endswith(remove_suffix):
        remove_suffix_offset = len(buffer) - len(remove_suffix)
        buffer = buffer[:remove_suffix_offset]
    return buffer.strip().lower().replace("-", "_")


def get_filtered_namespace(
    envs: Dict[str, str],
    start_prefix: Optional[str] = None,
    end_suffix: Optional[str] = None,
) -> Namespace:
    if start_prefix or end_suffix:
        filtered_envs = dict()
        for k, v in envs.items():
            if start_prefix and not k.startswith(start_prefix):
                continue
            if end_suffix and not k.endswith(end_suffix):
                continue
            filtered_envs[k] = v
    else:
        filtered_envs = envs

    normalized_envs = dict()
    for k, v in filtered_envs.items():
        normalized_envs[normalize_config_key(k, start_prefix, end_suffix)] = v

    return Namespace(**normalized_envs)


def get_namespace_by_os_envs(
    start_prefix: Optional[str] = None,
    end_suffix: Optional[str] = None,
) -> Namespace:
    return get_filtered_namespace(get_os_envs_dict(), start_prefix, end_suffix)
