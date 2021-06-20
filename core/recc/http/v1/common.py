# -*- coding: utf-8 -*-

from typing import Any, Optional
from http import HTTPStatus
from aiohttp.web import json_response
from aiohttp.web_response import Response

RESPONSE_VERSION = "0.1"
STATUS_OK = "OK"
STATUS_ERROR = "ERROR"
PATH_PREFIX_API_V1 = "/api/v1"
PATH_PREFIX_EXTRA_AIRJOY = "/extra/airjoy"
PATH_PREFIX_EXTRA_POSOD = "/extra/posod"

no_name = "_"
at_session = "@session"

k_project = "proj"
k_layout = "layout"
k_user = "usr"
k_task = "task"
k_bucket = "bucket"
k_object = "obj"
k_lambda = "lambda"
k_output = "out"


def get_v1_path(path: str) -> str:
    assert path
    if path[0] == "/":
        return PATH_PREFIX_API_V1 + path
    else:
        return PATH_PREFIX_API_V1 + "/" + path


def get_airjoy_v1_path(path: str) -> str:
    assert path
    if path[0] == "/":
        return PATH_PREFIX_API_V1 + PATH_PREFIX_EXTRA_AIRJOY + path
    else:
        return PATH_PREFIX_API_V1 + PATH_PREFIX_EXTRA_AIRJOY + "/" + path


def get_posod_v1_path(path: str) -> str:
    assert path
    if path[0] == "/":
        return PATH_PREFIX_API_V1 + PATH_PREFIX_EXTRA_POSOD + path
    else:
        return PATH_PREFIX_API_V1 + PATH_PREFIX_EXTRA_POSOD + "/" + path


def create_response_data(
    name: str,
    status: str,
    detail="",
    result: Optional[Any] = None,
    version=RESPONSE_VERSION,
) -> dict:
    return {
        "name": name,
        "status": status,
        "detail": detail,
        "result": result if result else {},
        "version": version,
    }


def response_ok(
    name: str,
    detail="",
    result: Optional[Any] = None,
) -> Response:
    return json_response(
        data=create_response_data(name, STATUS_OK, detail, result, RESPONSE_VERSION),
        status=HTTPStatus.OK,
    )


def response_ok_without_detail(
    name: str,
    result: Optional[Any] = None,
) -> Response:
    return response_ok(name, "", result)


def response_error(
    name: str,
    detail="",
    result: Optional[Any] = None,
    status=HTTPStatus.OK,
) -> Response:
    return json_response(
        data=create_response_data(name, STATUS_ERROR, detail, result, RESPONSE_VERSION),
        status=status,
    )
