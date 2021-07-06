# -*- coding: utf-8 -*-

INVALID_NAMING_RULE_PATTERN = r"[^a-zA-Z0-9_-]"

NAME_DELIMITER = "."
NAME_CONTAINER = "container"
NAME_VOLUME = "volume"
NAME_NETWORK = "network"
NAME_GLOBAL = "global"

PREFIX_RECC = "recc"
PREFIX_RECC_GLOBAL = f"{PREFIX_RECC}{NAME_DELIMITER}{NAME_GLOBAL}"

SUFFIX_SOCKET = "sock"

GLOBAL_CONTAINER = f"{PREFIX_RECC_GLOBAL}{NAME_DELIMITER}{NAME_CONTAINER}"
GLOBAL_VOLUME = f"{PREFIX_RECC_GLOBAL}{NAME_DELIMITER}{NAME_VOLUME}"
GLOBAL_NETWORK = f"{PREFIX_RECC_GLOBAL}{NAME_DELIMITER}{NAME_NETWORK}"
