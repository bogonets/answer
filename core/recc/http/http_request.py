# -*- coding: utf-8 -*-

from typing import Any, TypeVar, List, Optional, Dict
from io import StringIO
from aiohttp.web_request import Request
from aiohttp.hdrs import (
    CONTENT_TYPE,
    CONTENT_ENCODING,
    CONTENT_LENGTH,
)
from aiohttp.web_exceptions import HTTPBadRequest, HTTPLengthRequired
from recc.log.logging import recc_http_logger as logger
from recc.mime.mime_type import (
    MimeType,
    MIME_APPLICATION_JSON,
    MIME_APPLICATION_XML,
    MIME_APPLICATION_YAML,
    MIME_TEXT_PLAIN,
)
from recc.driver.json import global_json_decoder
from recc.driver.xml import global_xml_decoder
from recc.driver.yaml import global_yaml_decoder

_T = TypeVar("_T")

APPLICATION = MIME_APPLICATION_JSON.family
JSON = MIME_APPLICATION_JSON.subtype
YAML = MIME_APPLICATION_YAML.subtype
XML = MIME_APPLICATION_XML.subtype
TEXT = MIME_TEXT_PLAIN.family
PLAIN = MIME_TEXT_PLAIN.subtype


async def read_data(request: Request) -> Any:
    content_type = request.headers.get(CONTENT_TYPE)
    content_encoding = request.headers.get(CONTENT_ENCODING)
    content_length = request.headers.get(CONTENT_LENGTH)

    if content_type is None:
        raise HTTPBadRequest(reason="Empty content-type header")
    if content_length is None or int(content_length) <= 0:
        raise HTTPLengthRequired()

    msg_buffer = StringIO()
    if content_type:
        msg_buffer.write(f"Content-Type: {content_type}\n")
    if content_encoding:
        msg_buffer.write(f"Content-Encoding: {content_encoding}\n")
    if content_length:
        msg_buffer.write(f"Content-Length: {content_length}")
    msg = msg_buffer.getvalue()
    if msg:
        logger.debug("Request content headers:\n" + msg)

    # Skip the content decoding process.

    content_mime = MimeType.parse(content_type)
    data: Any
    if content_mime.test_from_accepts([MIME_APPLICATION_JSON, MIME_TEXT_PLAIN]):
        return global_json_decoder(await request.text())
    elif content_mime.test_from_accept(MIME_APPLICATION_YAML):
        return global_yaml_decoder(await request.text())
    elif content_mime.test_from_accept(MIME_APPLICATION_XML):
        return global_xml_decoder(await request.text())
    raise HTTPBadRequest(reason=f"Unsupported content-type: {content_type}")


async def read_dict(
    request: Request,
    assert_keys: Optional[List[str]] = None,
) -> Dict[str, Any]:
    data = await read_data(request)
    if not isinstance(data, dict):
        raise HTTPBadRequest(reason="Only dictionary-type requests are accepted")

    if assert_keys:
        for key in assert_keys:
            if key not in data:
                raise HTTPBadRequest(reason=f"Not exists key: {key}")

    return data