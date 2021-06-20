# -*- coding: utf-8 -*-

from recc.exception.recc_error import ReccDecodeError


class BearerAuth:
    """
    Http bearer authentication.
    """

    TYPE = "Bearer"
    TYPE_LOWER = TYPE.lower()

    def __init__(self, token: str):
        self.token = token

    @classmethod
    def decode_from_authorization_header(cls, auth_header):
        """
        Create a :class:`BearerAuth` object from an ``Authorization`` HTTP header.
        """

        split = auth_header.strip().split(" ")
        if len(split) != 2:
            raise ReccDecodeError("Could not parse authorization header.")

        if split[0].strip().lower() != cls.TYPE_LOWER:
            raise ReccDecodeError(f"Unknown authorization method {split[0]}")

        return cls(split[1].strip())

    def encode(self):
        """
        Encode credentials.
        """

        return f"{self.TYPE} {self.token}"
