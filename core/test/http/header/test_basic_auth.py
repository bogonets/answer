# -*- coding: utf-8 -*-

import unittest
from hashlib import sha256

from recc.http.header.basic_auth import BasicAuth


class ArgsTestCase(unittest.TestCase):

    # fmt: off
    test_auth = "Basic YWRtaW46OWFmMTViMzM2ZTZhOTYxOTkyODUzN2RmMzBiMmU2YTIzNzY1NjlmY2Y5ZDdlNzczZWNjZWRlNjU2MDY1MjlhMA=="  # noqa
    test_user = "admin"
    test_password_bytes = b"0000"
    test_password_sha256 = "9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0"  # noqa
    # fmt: on

    def test_sha256(self):
        encoded_pass = sha256(self.test_password_bytes)
        hex_str_pass = encoded_pass.hexdigest().lower()
        self.assertEqual(self.test_password_sha256, hex_str_pass)

    def test_encode_decode(self):
        auth = BasicAuth.decode_from_authorization_header(self.test_auth)
        self.assertEqual(self.test_user, auth.user_id)
        self.assertEqual(self.test_password_sha256, auth.password)
        self.assertEqual(self.test_auth, auth.encode())


if __name__ == "__main__":
    unittest.main()
