# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional


def eval_annotations(
    obj: Any,
    global_variables: Optional[Dict[str, Any]] = None,
    local_variables: Optional[Dict[str, Any]] = None,
) -> None:
    if not hasattr(obj, "__annotations__"):
        return

    if global_variables is None:
        global_variables = globals()
    if local_variables is None:
        local_variables = locals()

    assert isinstance(obj.__annotations__, dict)
    update_annotations: Dict[str, Any] = dict()

    for key, annotation in obj.__annotations__.items():
        if isinstance(annotation, str):
            type_origin = eval(annotation, global_variables, local_variables)
            if type_origin is not None:
                eval_annotations(type_origin, global_variables, local_variables)
                update_annotations[key] = type_origin
            else:
                update_annotations[key] = annotation
        else:
            update_annotations[key] = annotation

    obj.__annotations__ = update_annotations

    # It can be a wrapped object.
    # Where to use: `inspect.signature` -> ... -> `inspect.unwrap`

    if hasattr(obj, "__wrapped__"):
        eval_annotations(obj.__wrapped__, global_variables, local_variables)
