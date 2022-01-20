# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional
from inspect import ismethod

ATTRIBUTE_FUNC = "__func__"
ATTRIBUTE_ANNOTATIONS = "__annotations__"
ATTRIBUTE_WRAPPED = "__wrapped__"


def eval_annotations(
    obj: Any,
    global_variables: Optional[Dict[str, Any]] = None,
    local_variables: Optional[Dict[str, Any]] = None,
) -> None:
    if ismethod(obj):
        assert hasattr(obj, ATTRIBUTE_FUNC)
        eval_annotations(
            getattr(obj, ATTRIBUTE_FUNC),
            global_variables,
            local_variables,
        )
        return

    if not hasattr(obj, ATTRIBUTE_ANNOTATIONS):
        return

    if global_variables is None:
        global_variables = globals()
    if local_variables is None:
        local_variables = locals()

    annotations = getattr(obj, ATTRIBUTE_ANNOTATIONS)
    assert isinstance(annotations, dict)
    update_annotations: Dict[str, Any] = dict()

    for key, annotation in annotations.items():
        if isinstance(annotation, str):
            type_origin = eval(annotation, global_variables, local_variables)
            if type_origin is not None:
                eval_annotations(type_origin, global_variables, local_variables)
                update_annotations[key] = type_origin
            else:
                update_annotations[key] = annotation
        else:
            update_annotations[key] = annotation

    setattr(obj, ATTRIBUTE_ANNOTATIONS, update_annotations)

    # It can be a wrapped object.
    # Where to use: `inspect.signature` -> ... -> `inspect.unwrap`

    if hasattr(obj, ATTRIBUTE_WRAPPED):
        eval_annotations(
            getattr(obj, ATTRIBUTE_WRAPPED),
            global_variables,
            local_variables,
        )
