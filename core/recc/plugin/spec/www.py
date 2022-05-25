# -*- coding: utf-8 -*-

from typing import Any, Dict, List

from recc.regex.resource_matcher import MatchItem
from recc.variables.plugin import SPEC_WWW


def parse_spec_www(spec: Dict[str, Any]) -> List[MatchItem]:
    if SPEC_WWW not in spec:
        return list()

    www = spec[SPEC_WWW]
    if not isinstance(www, (tuple, list, set)):
        raise TypeError(f"Unsupported `{SPEC_WWW}` type: {type(www).__name__}")

    return [MatchItem.parse(item) for item in www]
