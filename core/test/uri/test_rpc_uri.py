# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.uri.rpc_uri import (
    RpcSchemeType,
    RpcDnsAddress,
    RpcUnixAddress,
    RpcUnixAbstractAddress,
    RpcIpv4Addresses,
    RpcIpv6Addresses,
    parse_rpc_dns_address,
    parse_rpc_unix_address,
    parse_rpc_unix_abstract_address,
    parse_rpc_ipv4_addresses,
    parse_rpc_ipv6_addresses,
    parse_rpc_address,
)


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

    def test_unix(self):
        unix1 = parse_rpc_unix_address("unix:/var/recc.sock")
        self.assertEqual("/var/recc.sock", unix1.path)

        unix2 = parse_rpc_unix_address("unix:./recc.sock")
        self.assertEqual("./recc.sock", unix2.path)

        unix3 = parse_rpc_unix_address("unix:///var/recc.sock")
        self.assertEqual("/var/recc.sock", unix3.path)

        with self.assertRaises(ValueError):
            parse_rpc_unix_address("unix://./recc.sock")

    def test_unix_abstract(self):
        unix_abs = parse_rpc_unix_abstract_address("unix-abstract:unknown.sock")
        self.assertEqual("unknown.sock", unix_abs.abstract_path)

    def test_ipv4(self):
        ip1 = parse_rpc_ipv4_addresses("ipv4:192.168.0.1,0.0.0.0:9999")
        self.assertEqual(2, len(ip1.addresses))
        self.assertEqual("192.168.0.1", ip1.addresses[0].address)
        self.assertIsNone(ip1.addresses[0].port)
        self.assertEqual("0.0.0.0", ip1.addresses[1].address)
        self.assertEqual(9999, ip1.addresses[1].port)

        ip2 = parse_rpc_ipv4_addresses("ipv4:127.0.0.1:0")
        self.assertEqual(1, len(ip2.addresses))
        self.assertEqual("127.0.0.1", ip2.addresses[0].address)
        self.assertEqual(0, ip2.addresses[0].port)

        with self.assertRaises(ValueError):
            parse_rpc_ipv4_addresses("ipv4:localhost")

    def test_ipv6(self):
        ip1 = parse_rpc_ipv6_addresses("ipv6:[2607:f8b0:400e:c00::ef],[::]:1234")
        self.assertEqual(2, len(ip1.addresses))
        self.assertEqual("[2607:f8b0:400e:c00::ef]", ip1.addresses[0].address)
        self.assertIsNone(ip1.addresses[0].port)
        self.assertEqual("[::]", ip1.addresses[1].address)
        self.assertEqual(1234, ip1.addresses[1].port)

        ip2 = parse_rpc_ipv6_addresses("ipv6:[::1]")
        self.assertEqual(1, len(ip2.addresses))
        self.assertEqual("[::1]", ip2.addresses[0].address)
        self.assertIsNone(ip2.addresses[0].port)

        with self.assertRaises(ValueError):
            parse_rpc_ipv6_addresses("ipv6:localhost")

    def test_parse_rpc_address(self):
        addr1 = parse_rpc_address("dns://dns-server:53/localhost:9999")
        self.assertEqual(RpcSchemeType.Dns, addr1[0])
        self.assertIsInstance(addr1[1], RpcDnsAddress)
        self.assertEqual("dns-server:53", addr1[1].authority)
        self.assertEqual("dns-server", addr1[1].authority_host)
        self.assertEqual(53, addr1[1].authority_port)
        self.assertEqual("localhost", addr1[1].host)
        self.assertEqual(9999, addr1[1].port)

        addr2 = parse_rpc_address("[::1]:1234")
        self.assertEqual(RpcSchemeType.Dns, addr2[0])
        self.assertIsInstance(addr2[1], RpcDnsAddress)
        self.assertIsNone(addr2[1].authority)
        self.assertIsNone(addr2[1].authority_host)
        self.assertIsNone(addr2[1].authority_port)
        self.assertEqual("[::1]", addr2[1].host)
        self.assertEqual(1234, addr2[1].port)

        addr3 = parse_rpc_address("unix:/var/recc.sock")
        self.assertEqual(RpcSchemeType.Unix, addr3[0])
        self.assertIsInstance(addr3[1], RpcUnixAddress)
        self.assertEqual("/var/recc.sock", addr3[1].path)

        addr4 = parse_rpc_address("unix-abstract:unknown.sock")
        self.assertEqual(RpcSchemeType.UnixAbstract, addr4[0])
        self.assertIsInstance(addr4[1], RpcUnixAbstractAddress)
        self.assertEqual("unknown.sock", addr4[1].abstract_path)

        addr5 = parse_rpc_address("ipv4:192.168.0.1,0.0.0.0:9999")
        self.assertEqual(RpcSchemeType.Ipv4, addr5[0])
        self.assertIsInstance(addr5[1], RpcIpv4Addresses)
        self.assertEqual(2, len(addr5[1].addresses))
        self.assertEqual("192.168.0.1", addr5[1].addresses[0].address)
        self.assertIsNone(addr5[1].addresses[0].port)
        self.assertEqual("0.0.0.0", addr5[1].addresses[1].address)
        self.assertEqual(9999, addr5[1].addresses[1].port)

        addr6 = parse_rpc_address("ipv6:[2607:f8b0:400e:c00::ef],[::]:1234")
        self.assertEqual(RpcSchemeType.Ipv6, addr6[0])
        self.assertIsInstance(addr6[1], RpcIpv6Addresses)
        self.assertEqual(2, len(addr6[1].addresses))
        self.assertEqual("[2607:f8b0:400e:c00::ef]", addr6[1].addresses[0].address)
        self.assertIsNone(addr6[1].addresses[0].port)
        self.assertEqual("[::]", addr6[1].addresses[1].address)
        self.assertEqual(1234, addr6[1].addresses[1].port)


if __name__ == "__main__":
    main()
