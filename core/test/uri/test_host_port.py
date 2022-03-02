# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.uri.host_port import (
    parse_ipv4_or_domain_port,
    parse_ipv6_port,
    parse_host_port,
)


class HostPortTestCase(TestCase):
    def test_parse_ipv4_or_domain_port(self):
        hp1 = parse_ipv4_or_domain_port("127.0.0.1")
        self.assertEqual("127.0.0.1", hp1.host)
        self.assertIsNone(hp1.port)

        hp2 = parse_ipv4_or_domain_port("localhost:123")
        self.assertEqual("localhost", hp2.host)
        self.assertEqual(123, hp2.port)

        hp3 = parse_ipv4_or_domain_port("www.ipv6-literal.net:1234")
        self.assertEqual("www.ipv6-literal.net", hp3.host)
        self.assertEqual(1234, hp3.port)

        with self.assertRaises(ValueError):
            parse_ipv6_port("localhost:")

    def test_parse_ipv6_port(self):
        hp1 = parse_ipv6_port("[2001:0db8:85a3:08d3:1319:8a2e:0370:7334]")
        self.assertEqual("[2001:0db8:85a3:08d3:1319:8a2e:0370:7334]", hp1.host)
        self.assertIsNone(hp1.port)

        hp2 = parse_ipv6_port("[fe80::1ff:fe23:4567:890a%eth2]:9999")
        self.assertEqual("[fe80::1ff:fe23:4567:890a%eth2]", hp2.host)
        self.assertEqual(9999, hp2.port)

        hp3 = parse_ipv6_port("[fe80::1ff:fe23:4567:890a%25eth2]:0")
        self.assertEqual("[fe80::1ff:fe23:4567:890a%25eth2]", hp3.host)
        self.assertEqual(0, hp3.port)

        with self.assertRaises(ValueError):
            parse_ipv6_port("[::")
        with self.assertRaises(ValueError):
            parse_ipv6_port("::]")
        with self.assertRaises(ValueError):
            parse_ipv6_port("[::]:")

    def test_parse_host_port(self):
        hp1 = parse_host_port("127.0.0.1")
        self.assertEqual("127.0.0.1", hp1.host)
        self.assertIsNone(hp1.port)

        hp2 = parse_host_port("www.ipv6-literal.net:1234")
        self.assertEqual("www.ipv6-literal.net", hp2.host)
        self.assertEqual(1234, hp2.port)

        hp3 = parse_host_port("[2001:0db8:85a3:08d3:1319:8a2e:0370:7334]")
        self.assertEqual("[2001:0db8:85a3:08d3:1319:8a2e:0370:7334]", hp3.host)
        self.assertIsNone(hp3.port)

        hp4 = parse_host_port("[fe80::1ff:fe23:4567:890a%eth2]:9999")
        self.assertEqual("[fe80::1ff:fe23:4567:890a%eth2]", hp4.host)
        self.assertEqual(9999, hp4.port)

        hp5 = parse_host_port("[fe80::1ff:fe23:4567:890a%25eth2]:0")
        self.assertEqual("[fe80::1ff:fe23:4567:890a%25eth2]", hp5.host)
        self.assertEqual(0, hp5.port)


if __name__ == "__main__":
    main()
