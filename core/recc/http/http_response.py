# -*- coding: utf-8 -*-

from enum import Enum
from multidict import CIMultiDict
from typing import Any, List, Optional, Union
from zlib import compress as zlib_compress
from gzip import compress as gzip_compress
from http import HTTPStatus
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.hdrs import (
    ACCEPT,
    ACCEPT_ENCODING,
    CONTENT_TYPE,
    CONTENT_ENCODING,
    CONTENT_LENGTH,
)
from aiohttp.web_exceptions import HTTPNotAcceptable
from recc.mime.mime_type import (
    MimeType,
    ANY_WILDCARD,
    MIME_APPLICATION_JSON,
    MIME_APPLICATION_XML,
    MIME_APPLICATION_YAML,
    MIME_TEXT_PLAIN,
    MIME_APPLICATION_JSON_UTF8,
    MIME_APPLICATION_XML_UTF8,
    MIME_APPLICATION_YAML_UTF8,
)
from recc.driver.json import global_json_encoder
from recc.driver.xml import global_xml_encoder
from recc.driver.yaml import global_yaml_encoder

APPLICATION = MIME_APPLICATION_JSON.family
JSON = MIME_APPLICATION_JSON.subtype
YAML = MIME_APPLICATION_YAML.subtype
XML = MIME_APPLICATION_XML.subtype
TEXT = MIME_TEXT_PLAIN.family
PLAIN = MIME_TEXT_PLAIN.subtype

ENCODING_DIRECTIVE_GZIP = "gzip"
ENCODING_DIRECTIVE_COMPRESS = "compress"
ENCODING_DIRECTIVE_DEFLATE = "deflate"
ENCODING_DIRECTIVE_BR = "br"
ENCODING_DIRECTIVE_IDENTITY = "identity"
ENCODING_DIRECTIVE_ANY_WILDCARD = "*"


class AcceptType(Enum):
    Json = 0
    Yaml = 1
    Xml = 2


class AcceptEncodingType(Enum):
    Gzip = 0
    Compress = 1
    Deflate = 2
    Br = 3
    Identity = 4


class AcceptEncoding:

    __slots__ = ("directive", "q")

    directive: str
    q: Optional[float]

    def __init__(self, directive: str, q: Optional[float] = None):
        self.directive = directive
        self.q = q

    def __repr__(self) -> str:
        return f"AcceptEncoding<directive={self.directive},q={self.q}>"


class Encoding:

    __slots__ = ("t", "q")

    t: AcceptEncodingType
    q: Optional[float]

    def __init__(self, t: AcceptEncodingType, q: Optional[float] = None):
        self.t = t
        self.q = q

    def __repr__(self) -> str:
        return f"Encoding<t={self.t},q={self.q}>"


def get_accept_type(header: Union[str, Request]) -> AcceptType:
    if isinstance(header, Request):
        try:
            accept_text = header.headers[ACCEPT]
        except KeyError:
            raise HTTPNotAcceptable(reason=f"Not exists `{ACCEPT}` header")
    else:
        accept_text = header
    accepts = [MimeType.parse(a.strip()) for a in accept_text.split(",")]

    is_any = False
    is_json = False
    is_yaml = False
    is_xml = False
    is_text = False

    for accept in accepts:
        if accept.family == ANY_WILDCARD and accept.subtype == ANY_WILDCARD:
            is_any = True
        elif accept.family == TEXT and accept.subtype == PLAIN:
            is_text = True
        elif accept.family == APPLICATION:
            if accept.subtype == JSON:
                is_json = True
            elif accept.subtype == XML:
                is_xml = True
            elif accept.subtype == YAML:
                is_yaml = True

    if is_any or is_json or is_text:
        return AcceptType.Json  # most preferred.
    if is_yaml:
        return AcceptType.Yaml  # second preferred.
    if is_xml:
        return AcceptType.Xml
    raise HTTPNotAcceptable(reason="Not acceptable MIMEs")


def get_encodings(text: str) -> List[AcceptEncoding]:
    result = list()
    for encoding in [e.strip().lower() for e in text.split(",")]:
        dq = [dq.strip() for dq in encoding.split(";")]
        directive = dq[0]
        q: Optional[float] = None
        if len(dq) >= 2:
            qv = dq[1].split("=")
            if len(qv) != 2:
                raise HTTPNotAcceptable(reason=f"Not acceptable parameter: {dq[1]}")
            if qv[0] != "q":
                raise HTTPNotAcceptable(reason=f"Not acceptable parameter key: {qv[0]}")
            q = float(qv[1])
        result.append(AcceptEncoding(directive, q))
    return result


def get_encoding(header: Union[str, Request]) -> Encoding:
    if isinstance(header, Request):
        try:
            encoding_text = header.headers[ACCEPT_ENCODING]
        except KeyError:
            raise HTTPNotAcceptable(reason=f"Not exists `{ACCEPT_ENCODING}` header")
    else:
        encoding_text = header
    encodings = get_encodings(encoding_text)

    is_gzip: Optional[int] = None
    is_compress: Optional[int] = None
    is_deflate: Optional[int] = None
    is_br: Optional[int] = None
    is_identity: Optional[int] = None
    is_any: Optional[int] = None

    identity_q0 = False
    any_q0 = False

    for i, encoding in enumerate(encodings):
        directive = encoding.directive
        if directive == ENCODING_DIRECTIVE_GZIP:
            is_gzip = i
        elif directive == ENCODING_DIRECTIVE_COMPRESS:
            is_compress = i
        elif directive == ENCODING_DIRECTIVE_DEFLATE:
            is_deflate = i
        elif directive == ENCODING_DIRECTIVE_BR:
            is_br = i
        elif directive == ENCODING_DIRECTIVE_IDENTITY:
            is_identity = i
            if encoding.q == 0:
                identity_q0 = True
        elif directive == ENCODING_DIRECTIVE_ANY_WILDCARD:
            is_any = i
            if encoding.q == 0:
                any_q0 = True

    # most preferred.
    if is_gzip is not None:
        return Encoding(AcceptEncodingType.Gzip, encodings[is_gzip].q)
    if is_any is not None and not any_q0:
        return Encoding(AcceptEncodingType.Gzip)

    # second preferred.
    if is_deflate is not None:
        return Encoding(AcceptEncodingType.Deflate, encodings[is_deflate].q)
    if is_identity is not None and not identity_q0:
        return Encoding(AcceptEncodingType.Identity, encodings[is_identity].q)

    if is_compress is not None:
        reason = f"Not acceptable encoding: {ENCODING_DIRECTIVE_COMPRESS}"
        raise HTTPNotAcceptable(reason=reason)
    if is_br is not None:
        reason = f"Not acceptable encoding: {ENCODING_DIRECTIVE_BR}"
        raise HTTPNotAcceptable(reason=reason)

    # As long as the identity value, meaning no encoding, is not explicitly forbidden,
    # by an identity;q=0 or a *;q=0 without another explicitly set value for identity,
    # the server must never send back a 406 Not Acceptable error.
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Encoding
    if identity_q0 or any_q0:
        raise HTTPNotAcceptable(reason="`q=0` is specified.")

    return Encoding(AcceptEncodingType.Identity)


def create_response(accept: AcceptType, encoding: Encoding, data: Any) -> Response:
    text: str
    content_type: str
    if accept == AcceptType.Json:
        text = global_json_encoder(data)
        content_type = str(MIME_APPLICATION_JSON_UTF8)
    elif accept == AcceptType.Yaml:
        text = global_yaml_encoder(data)
        content_type = str(MIME_APPLICATION_YAML_UTF8)
    elif accept == AcceptType.Xml:
        text = global_xml_encoder(data)
        content_type = str(MIME_APPLICATION_XML_UTF8)
    else:
        assert False, "Not accessible block."

    headers = [(CONTENT_TYPE, content_type)]

    text_bytes = text.encode(encoding="utf-8")
    body: bytes

    if encoding.t == AcceptEncodingType.Gzip:
        if encoding.q is not None:
            body = gzip_compress(text_bytes, compresslevel=int(encoding.q))
        else:
            body = gzip_compress(text_bytes)
        headers.append((CONTENT_ENCODING, ENCODING_DIRECTIVE_GZIP))
    elif encoding.t == AcceptEncodingType.Deflate:
        if encoding.q is not None:
            body = zlib_compress(text_bytes, level=int(encoding.q))
        else:
            body = zlib_compress(text_bytes)
        headers.append((CONTENT_ENCODING, ENCODING_DIRECTIVE_DEFLATE))
    elif encoding.t == AcceptEncodingType.Identity:
        body = text_bytes
    else:
        assert False, "Not accessible block."

    assert body is not None
    headers.append((CONTENT_LENGTH, str(len(body))))

    return Response(
        body=body,
        status=HTTPStatus.OK,
        reason="OK",
        headers=CIMultiDict(headers),
    )


def create_response_with_request(request: Request, data: Any) -> Response:
    # Do not use the `Accept-Charset` header.
    # https://developer.mozilla.org/ko/docs/Web/HTTP/Content_negotiation
    # https://www.eff.org/deeplinks/2010/01/primer-information-theory-and-privacy

    accept = get_accept_type(request)
    encoding = get_encoding(request)

    return create_response(accept, encoding, data)
