# -*- coding: utf-8 -*-

from typing import Any, TypeVar, Type
from io import StringIO
from aiohttp.web_request import Request
from aiohttp.hdrs import (
    CONTENT_TYPE,
    CONTENT_ENCODING,
    CONTENT_LENGTH,
)
from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPLengthRequired,
    HTTPInternalServerError,
)
from recc.exception.recc_error import ReccDeserializeError
from recc.log.logging import recc_http_logger as logger
from recc.serializable.deserialize import deserialize_default
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


async def read_content(request: Request, cls: Type[_T]) -> _T:
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
        data = global_json_decoder(await request.text())
    elif content_mime.test_from_accept(MIME_APPLICATION_YAML):
        data = global_yaml_decoder(await request.text())
    elif content_mime.test_from_accept(MIME_APPLICATION_XML):
        data = global_xml_decoder(await request.text())
    else:
        raise HTTPBadRequest(reason=f"Unsupported content-type: {content_type}")

    assert data is not None
    try:
        return deserialize_default(data, cls)
    except ReccDeserializeError as e:
        logger.exception(e)
        raise HTTPInternalServerError(reason="Content deserialize error")
