# -*- coding: utf-8 -*-

INVALID_NAMING_RULE_PATTERN = r"[^a-zA-Z0-9_-]"

NAME_SEPARATOR = "."
NAME_CONTAINER = "container"
NAME_VOLUME = "volume"
NAME_NETWORK = "network"
NAME_GLOBAL = "global"

PREFIX_RECC = "recc"
PREFIX_RECC_GLOBAL = f"{PREFIX_RECC}{NAME_SEPARATOR}{NAME_GLOBAL}"

GLOBAL_CONTAINER = f"{PREFIX_RECC_GLOBAL}{NAME_SEPARATOR}{NAME_CONTAINER}"
GLOBAL_VOLUME = f"{PREFIX_RECC_GLOBAL}{NAME_SEPARATOR}{NAME_VOLUME}"
GLOBAL_NETWORK = f"{PREFIX_RECC_GLOBAL}{NAME_SEPARATOR}{NAME_NETWORK}"
