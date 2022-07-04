# -*- coding: utf-8 -*-

from io import StringIO
from typing import Any, Type, TypeVar, Union, get_args, get_origin, get_type_hints
from urllib.parse import parse_qs

from aiohttp.hdrs import CONTENT_ENCODING, CONTENT_LENGTH, CONTENT_TYPE
from aiohttp.web_exceptions import HTTPBadRequest, HTTPLengthRequired
from aiohttp.web_request import Request
from multidict import CIMultiDictProxy
from type_serialize import deserialize

from recc.driver.json import global_json_decoder
from recc.driver.xml import global_xml_decoder
from recc.driver.yaml import global_yaml_decoder
from recc.mime.mime_type import (
    MIME_APPLICATION_FORM,
    MIME_APPLICATION_JSON,
    MIME_APPLICATION_XML,
    MIME_APPLICATION_YAML,
    MIME_TEXT_PLAIN,
    MimeType,
)

_T = TypeVar("_T")


def header_logging_message(headers: CIMultiDictProxy[str]) -> str:
    content_type = headers.get(CONTENT_TYPE)
    content_encoding = headers.get(CONTENT_ENCODING)
    content_length = headers.get(CONTENT_LENGTH)

    msg_buffer = StringIO()
    if content_type:
        msg_buffer.write(f"Content-Type: {content_type}\n")
    if content_encoding:
        msg_buffer.write(f"Content-Encoding: {content_encoding}\n")
    if content_length:
        msg_buffer.write(f"Content-Length: {content_length}")
    return msg_buffer.getvalue()


def payload_to_object(headers: CIMultiDictProxy[str], payload: str) -> Any:
    content_type = headers.get(CONTENT_TYPE)
    content_length = headers.get(CONTENT_LENGTH)

    if content_type is None:
        raise HTTPBadRequest(reason="Empty content-type header")
    if content_length is None or int(content_length) <= 0:
        raise HTTPLengthRequired()

    # Skip the content decoding process.

    content_mime = MimeType.parse(content_type)
    data: Any
    if content_mime.test_from_accepts([MIME_APPLICATION_JSON, MIME_TEXT_PLAIN]):
        return global_json_decoder(payload)
    elif content_mime.test_from_accept(MIME_APPLICATION_YAML):
        return global_yaml_decoder(payload)
    elif content_mime.test_from_accept(MIME_APPLICATION_XML):
        return global_xml_decoder(payload)
    elif content_mime.test_from_accept(MIME_APPLICATION_FORM):
        return {k: v[-1] for k, v in parse_qs(payload).items()}
    raise HTTPBadRequest(reason=f"Unsupported content-type: {content_type}")


def payload_to_class(headers: CIMultiDictProxy[str], payload: str, cls: Type[_T]) -> _T:
    data = payload_to_object(headers, payload)
    return deserialize(data, cls)


def assert_required_arguments(obj: Any) -> None:
    for key, hint in get_type_hints(obj).items():
        type_origin = get_origin(hint)
        type_args = get_args(hint)

        if type_origin is Union:
            if type(None) in type_args:
                continue

        if not hasattr(obj, key):
            raise HTTPBadRequest(reason=f"Not exists `{key}` in content body")


async def request_payload_to_class(request: Request, cls: Type[_T]) -> _T:
    return payload_to_class(request.headers, await request.text(), cls)
