# -*- coding: utf-8 -*-

import binascii
from base64 import b64decode, b64encode


class BasicAuth:
    """
    Http basic authentication.
    """

    TYPE = "Basic"
    TYPE_LOWER = TYPE.lower()

    def __init__(self, user_id: str, password="", encoding="latin1"):
        if ":" in user_id:
            raise ValueError('A ":" is not allowed in user_id RFC 1945#section-11.1)')

        self.user_id = user_id
        self.password = password
        self.encoding = encoding

    def __str__(self) -> str:
        return self.user_id

    def __repr__(self) -> str:
        return f"BasicAuth<id={self.user_id},encoding={self.encoding}>"

    @classmethod
    def decode_from_authorization_header(cls, auth_header, encoding="latin1"):
        """
        Create a :class:`BasicAuth` object from an ``Authorization`` HTTP header.
        """

        split = auth_header.strip().split(" ")
        if len(split) != 2:
            raise ValueError("Could not parse authorization header")

        if split[0].strip().lower() != cls.TYPE_LOWER:
            raise ValueError(f"Unknown authorization method {split[0]}")

        to_decode = split[1].strip()

        try:
            username, _, password = (
                b64decode(to_decode.encode("ascii")).decode(encoding).partition(":")
            )
        except binascii.Error:
            raise ValueError("Invalid base64 encoding")

        return cls(username, password, encoding)

    def encode(self) -> str:
        """
        Encode credentials.
        """

        credentials = f"{self.user_id}:{self.password}".encode(self.encoding)
        encoded_credentials = b64encode(credentials).decode(self.encoding)
        return f"{self.TYPE} {encoded_credentials}"
