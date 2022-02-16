# -*- coding: utf-8 -*-
# [WARNING] Do not use 3rd-party libraries in this file.


def parse_semantic_version(ver: str) -> tuple:
    return tuple([int(d) for d in ver.split("-")[0].split(".")])


def normalize_version(ver: str) -> str:
    return ver.replace("-", ".")


version_text = "2.0.0-dev9"
version_info = parse_semantic_version(version_text)

database_version = version_text.split("-")[0]
database_info = parse_semantic_version(database_version)
