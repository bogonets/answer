# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Dict, Optional

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


def filter_dict(
    envs: Dict[str, str],
    start_prefix: Optional[str] = None,
    end_suffix: Optional[str] = None,
) -> Dict[str, str]:
    if not start_prefix and not end_suffix:
        return envs

    result = dict()
    for k, v in envs.items():
        if start_prefix and not k.startswith(start_prefix):
            continue
        if end_suffix and not k.endswith(end_suffix):
            continue
        result[k] = v
    return result


def get_filtered_dict(
    envs: Dict[str, str],
    start_prefix: Optional[str] = None,
    end_suffix: Optional[str] = None,
) -> Dict[str, str]:
    normalized_envs = dict()
    for k, v in filter_dict(envs, start_prefix, end_suffix).items():
        normalized_envs[normalize_config_key(k, start_prefix, end_suffix)] = v
    return normalized_envs


def get_filtered_namespace(
    envs: Dict[str, str],
    start_prefix: Optional[str] = None,
    end_suffix: Optional[str] = None,
) -> Namespace:
    return Namespace(**get_filtered_dict(envs, start_prefix, end_suffix))


def get_namespace_by_os_envs(
    start_prefix: Optional[str] = None,
    end_suffix: Optional[str] = None,
) -> Namespace:
    return get_filtered_namespace(get_os_envs_dict(), start_prefix, end_suffix)


def get_namespace_by_os_env_files(
    start_prefix: Optional[str] = None,
    end_suffix: Optional[str] = None,
    encoding: Optional[str] = None,
) -> Namespace:
    result = Namespace()
    envs = get_filtered_dict(get_os_envs_dict(), start_prefix, end_suffix)
    for key, value in envs.items():
        with open(value, "r", encoding=encoding) as f:
            setattr(result, key, f.read())
    return result
