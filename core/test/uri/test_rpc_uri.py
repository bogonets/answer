# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.uri.rpc_uri import parse_rpc_dns_address


class RpcAddressParseTestCase(TestCase):
    def test_dns_with_authority(self):
        dns1 = parse_rpc_dns_address("dns://dns-server:53/localhost:9999")
        self.assertEqual("dns-server:53", dns1.authority)
        self.assertEqual("dns-server", dns1.authority_host)
        self.assertEqual(53, dns1.authority_port)
        self.assertEqual("localhost", dns1.host)
        self.assertEqual(9999, dns1.port)

        dns2 = parse_rpc_dns_address("dns://dns-server/[::1]:1234")
        self.assertEqual("dns-server", dns2.authority)
        self.assertEqual("dns-server", dns2.authority_host)
        self.assertIsNone(dns2.authority_port)
        self.assertEqual("[::1]", dns2.host)
        self.assertEqual(1234, dns2.port)

        dns3 = parse_rpc_dns_address("dns://[::1]:9999/[::]:443")
        self.assertEqual("[::1]:9999", dns3.authority)
        self.assertEqual("[::1]", dns3.authority_host)
        self.assertEqual(9999, dns3.authority_port)
        self.assertEqual("[::]", dns3.host)
        self.assertEqual(443, dns3.port)

        dns4 = parse_rpc_dns_address("dns://192.168.0.1:53/0.0.0.0:80")
        self.assertEqual("192.168.0.1:53", dns4.authority)
        self.assertEqual("192.168.0.1", dns4.authority_host)
        self.assertEqual(53, dns4.authority_port)
        self.assertEqual("0.0.0.0", dns4.host)
        self.assertEqual(80, dns4.port)

    def test_dns(self):
        dns1 = parse_rpc_dns_address("dns:localhost.com:80")
        self.assertIsNone(dns1.authority)
        self.assertIsNone(dns1.authority_host)
        self.assertIsNone(dns1.authority_port)
        self.assertEqual("localhost.com", dns1.host)
        self.assertEqual(80, dns1.port)

        dns2 = parse_rpc_dns_address("dns:localhost.net")
        self.assertIsNone(dns2.authority)
        self.assertIsNone(dns2.authority_host)
        self.assertIsNone(dns2.authority_port)
        self.assertEqual("localhost.net", dns2.host)
        self.assertIsNone(dns2.port)

        dns3 = parse_rpc_dns_address("dns:192.168.0.2")
        self.assertIsNone(dns3.authority)
        self.assertIsNone(dns3.authority_host)
        self.assertIsNone(dns3.authority_port)
        self.assertEqual("192.168.0.2", dns3.host)
        self.assertIsNone(dns3.port)

        dns4 = parse_rpc_dns_address("127.0.0.1")
        self.assertIsNone(dns4.authority)
        self.assertIsNone(dns4.authority_host)
        self.assertIsNone(dns4.authority_port)
        self.assertEqual("127.0.0.1", dns4.host)
        self.assertIsNone(dns4.port)

        dns5 = parse_rpc_dns_address("[2001:0db8:85a3:08d3:1319:8a2e:0370:7334]")
        self.assertIsNone(dns5.authority)
        self.assertIsNone(dns5.authority_host)
        self.assertIsNone(dns5.authority_port)
        self.assertEqual("[2001:0db8:85a3:08d3:1319:8a2e:0370:7334]", dns5.host)
        self.assertIsNone(dns5.port)

        dns6 = parse_rpc_dns_address("0.0.0.0:9999")
        self.assertIsNone(dns6.authority)
        self.assertIsNone(dns6.authority_host)
        self.assertIsNone(dns6.authority_port)
        self.assertEqual("0.0.0.0", dns6.host)
        self.assertEqual(9999, dns6.port)

        dns7 = parse_rpc_dns_address("[::1]:1234")
        self.assertIsNone(dns7.authority)
        self.assertIsNone(dns7.authority_host)
        self.assertIsNone(dns7.authority_port)
        self.assertEqual("[::1]", dns7.host)
        self.assertEqual(1234, dns7.port)


if __name__ == "__main__":
    main()
