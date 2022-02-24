# -*- coding: utf-8 -*-
# [WARNING] Do not use 3rd-party libraries in this file.

from typing import Tuple, Final

VersionTuple = Tuple[int, int, int]


def parse_semantic_version(ver: str) -> tuple:
    return tuple([int(d) for d in ver.split("-")[0].split(".")])


def parse_version_tuple(ver: str) -> VersionTuple:
    n = parse_semantic_version(ver)
    if len(n) != 3:
        raise ValueError(
            f"The argument `ver` is not in semantic versioning format: '{ver}'"
        )

    assert isinstance(n[0], int)
    assert isinstance(n[1], int)
    assert isinstance(n[2], int)

    if n[0] < 0:
        raise ValueError(
            f"The major version number must be greater than or equal to 0 (vs {n[0]})"
        )
    if n[1] < 0:
        raise ValueError(
            f"The minor version number must be greater than or equal to 0 (vs {n[1]})"
        )
    if n[2] < 0:
        raise ValueError(
            f"The patch version number must be greater than or equal to 0 (vs {n[2]})"
        )

    return n[0], n[1], n[2]


def normalize_version(ver: str) -> str:
    return ver.replace("-", ".")


version_text = "2.0.0-dev9"
version_tuple: Final[VersionTuple] = parse_version_tuple(version_text)

assert len(version_tuple) == 3
assert isinstance(version_tuple[0], int)
assert isinstance(version_tuple[1], int)
assert isinstance(version_tuple[2], int)
assert version_tuple[0] >= 0
assert version_tuple[1] >= 0
assert version_tuple[2] >= 0
