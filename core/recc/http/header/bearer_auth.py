# -*- coding: utf-8 -*-


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
            raise ValueError("Could not parse authorization header")

        if split[0].strip().lower() != cls.TYPE_LOWER:
            raise ValueError(f"Unknown authorization method {split[0]}")

        return cls(split[1].strip())

    def encode(self):
        """
        Encode credentials.
        """

        return f"{self.TYPE} {self.token}"
