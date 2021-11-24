# -*- coding: utf-8 -*-

from unittest import main, TestCase
from recc.packet.raw.raw_field_spec import RawFieldSpec
from recc.packet.raw.raw_packet_base import RawPacketBase

_TEST_SPEC = [
    RawFieldSpec("a", 1),
    RawFieldSpec("b", 3),
    RawFieldSpec("c", 2, range(0, 3)),
    RawFieldSpec("d", 1, [1, 2, 4, 5]),
]


class _TestPacket(RawPacketBase):

    a: int
    b: int
    c: int
    d: int

    def __init__(self):
        super().__init__(_TEST_SPEC)


class RawPacketBaseTestCase(TestCase):
    def test_from_hex(self):
        packet = _TestPacket()
        packet.from_hex("01000009000205")
        self.assertEqual(1, packet.a)
        self.assertEqual(9, packet.b)
        self.assertEqual(2, packet.c)
        self.assertEqual(5, packet.d)

    def test_from_hex_error(self):
        with self.assertRaises(IndexError):
            _TestPacket().from_hex("01000009000206")

    def test_to_hex(self):
        packet = _TestPacket()
        packet.from_dict(a=0, b=1, c=2, d=4)
        self.assertEqual("00000001000204", packet.to_hex())


if __name__ == "__main__":
    main()
