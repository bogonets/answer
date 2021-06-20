# -*- coding: utf-8 -*-

from typing import Optional, Final, List

TYPE_SEPARATOR: Final[str] = "/"
PARAMETER_SEPARATOR: Final[str] = ";"
ANY_WILDCARD: Final[str] = "*"


class MimeType:
    """
    A media type (formerly known as MIME type) is a two-part identifier
    for file formats and format contents transmitted on the Internet.

    See also:
    * https://en.wikipedia.org/wiki/Media_type
    * https://datatracker.ietf.org/doc/html/rfc2045#section-5.1
    * https://www.iana.org/assignments/media-types/media-types.xhtml
    """

    def __init__(
        self,
        family: str,
        subtype: str,
        parameter: Optional[str] = None,
        original: Optional[str] = None,
        name: Optional[str] = None,
        reference: Optional[str] = None,
    ):
        # The `type` of MIME is a Python reserved character.
        # Therefore, the name will be changed to `family`.
        self.family = family.strip().lower()

        # Does not parse `tree` and `suffix`.
        self.subtype = subtype.strip().lower()

        # Does not parse `attribute` and `value`.
        self.parameter = parameter

        # Full original text.
        self.original = original

        self.name = name
        self.reference = reference

    @property
    def mime(self) -> str:
        prefix = f"{self.family}{TYPE_SEPARATOR}{self.subtype}"
        if self.parameter:
            return f"{prefix}{PARAMETER_SEPARATOR}{self.parameter}"
        else:
            return prefix

    @classmethod
    def parse(
        cls,
        text: str,
        name: Optional[str] = None,
        reference: Optional[str] = None,
    ) -> "MimeType":
        types_and_param = text.split(PARAMETER_SEPARATOR, 1)
        assert 1 <= len(types_and_param) <= 2

        parameter: Optional[str] = None
        if len(types_and_param) == 2:
            parameter = types_and_param[1].strip()

        types = types_and_param[0].strip().split(TYPE_SEPARATOR, 1)
        assert 1 <= len(types) <= 2

        family = types[0]
        if len(types) == 1:
            if family == ANY_WILDCARD:
                subtype = ANY_WILDCARD
            else:
                subtype = str()
        else:
            assert len(types) == 2
            subtype = types[1]

        return cls(family, subtype, parameter, text, name, reference)

    def __str__(self) -> str:
        return self.mime

    def test_from_accept(self, accept: "MimeType") -> bool:
        if self.family == accept.family:
            pass
        elif accept.family == ANY_WILDCARD:
            pass
        elif self.family == ANY_WILDCARD:
            pass
        else:
            assert self.family != accept.family
            return False

        if self.subtype == accept.subtype:
            return True
        elif accept.subtype == ANY_WILDCARD:
            return True
        elif self.subtype == ANY_WILDCARD:
            return True
        else:
            assert self.subtype != accept.subtype
            return False

    def test_from_accepts(self, accepts: List["MimeType"]) -> bool:
        for accept in accepts:
            if self.test_from_accept(accept):
                return True
        return False


SINGLE_ANY: Final[str] = "*"
BOTH_ANY: Final[str] = "*/*"

APPLICATION_OCTET_STREAM: Final[str] = "application/octet-stream"
APPLICATION_JSON: Final[str] = "application/json"
TEXT_PLAIN: Final[str] = "text/plain"

MIME_ANY = MimeType.parse(SINGLE_ANY)
MIME_ANY_BOTH = MimeType.parse(BOTH_ANY)
MIME_APPLICATION_OCTET_STREAM = MimeType.parse(APPLICATION_OCTET_STREAM)
MIME_APPLICATION_JSON = MimeType.parse(APPLICATION_JSON)
MIME_TEXT_PLAIN = MimeType.parse(TEXT_PLAIN)
