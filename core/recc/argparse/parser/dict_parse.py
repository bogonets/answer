# -*- coding: utf-8 -*-

from typing import Union, Dict, Any, Optional
from argparse import Namespace


def get_namespace_by_dict(
    obj: Union[Dict[str, Any], Any],
    *subsection_path: Optional[str],
) -> Namespace:
    if subsection_path:
        key = str(subsection_path[0])
        if isinstance(obj, dict):
            if key not in obj:
                raise KeyError(f"A `{key}` key not in the dictionary.")
            return get_namespace_by_dict(obj[key], *subsection_path[1:])
        else:
            if not hasattr(obj, key):
                raise KeyError(f"A `{key}` key not in the object.")
            return get_namespace_by_dict(getattr(obj, key), *subsection_path[1:])

    # Last depth.

    if not isinstance(obj, dict):
        raise TypeError("The last depth object must be a dictionary type.")

    return Namespace(**obj)
