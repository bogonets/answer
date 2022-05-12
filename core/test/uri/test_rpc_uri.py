# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.uri.rpc_uri import (
    RpcDnsAddress,
    RpcIpv4Addresses,
    RpcIpv6Addresses,
    RpcSchemeType,
    RpcUnixAbstractAddress,
    RpcUnixAddress,
    parse_rpc_address,
    parse_rpc_address_as_class,
    parse_rpc_dns_address,
    parse_rpc_ipv4_addresses,
    parse_rpc_ipv6_addresses,
    parse_rpc_unix_abstract_address,
    parse_rpc_unix_address,
)


class RpcAddressParseTestCase(TestCase):
    def test_dns_with_authority(self):
        uri1 = "dns://dns-server:53/localhost:9999"
        dns1 = parse_rpc_dns_address(uri1)
        self.assertEqual("dns-server:53", dns1.authority)
        self.assertEqual("dns-server", dns1.authority_host)
        self.assertEqual(53, dns1.authority_port)
        self.assertEqual("localhost", dns1.host)
        self.assertEqual(9999, dns1.port)
        self.assertEqual(uri1, str(dns1))

        uri2 = "dns://dns-server/[::1]:1234"
        dns2 = parse_rpc_dns_address(uri2)
        self.assertEqual("dns-server", dns2.authority)
        self.assertEqual("dns-server", dns2.authority_host)
        self.assertIsNone(dns2.authority_port)
        self.assertEqual("[::1]", dns2.host)
        self.assertEqual(1234, dns2.port)
        self.assertEqual(uri2, str(dns2))

        uri3 = "dns://[::1]:9999/[::]:443"
        dns3 = parse_rpc_dns_address(uri3)
        self.assertEqual("[::1]:9999", dns3.authority)
        self.assertEqual("[::1]", dns3.authority_host)
        self.assertEqual(9999, dns3.authority_port)
        self.assertEqual("[::]", dns3.host)
        self.assertEqual(443, dns3.port)
        self.assertEqual(uri3, str(dns3))

        uri4 = "dns://192.168.0.1:53/0.0.0.0:80"
        dns4 = parse_rpc_dns_address(uri4)
        self.assertEqual("192.168.0.1:53", dns4.authority)
        self.assertEqual("192.168.0.1", dns4.authority_host)
        self.assertEqual(53, dns4.authority_port)
        self.assertEqual("0.0.0.0", dns4.host)
        self.assertEqual(80, dns4.port)
        self.assertEqual(uri4, str(dns4))

    def test_dns(self):
        uri1 = "dns:localhost.com:80"
        dns1 = parse_rpc_dns_address(uri1)
        self.assertIsNone(dns1.authority)
        self.assertIsNone(dns1.authority_host)
        self.assertIsNone(dns1.authority_port)
        self.assertEqual("localhost.com", dns1.host)
        self.assertEqual(80, dns1.port)
        self.assertEqual(uri1, str(dns1))

        uri2 = "dns:localhost.net"
        dns2 = parse_rpc_dns_address(uri2)
        self.assertIsNone(dns2.authority)
        self.assertIsNone(dns2.authority_host)
        self.assertIsNone(dns2.authority_port)
        self.assertEqual("localhost.net", dns2.host)
        self.assertIsNone(dns2.port)
        self.assertEqual(uri2, str(dns2))

        uri3 = "dns:192.168.0.2"
        dns3 = parse_rpc_dns_address(uri3)
        self.assertIsNone(dns3.authority)
        self.assertIsNone(dns3.authority_host)
        self.assertIsNone(dns3.authority_port)
        self.assertEqual("192.168.0.2", dns3.host)
        self.assertIsNone(dns3.port)
        self.assertEqual(uri3, str(dns3))

        uri4 = "127.0.0.1"
        dns4 = parse_rpc_dns_address(uri4)
        self.assertIsNone(dns4.authority)
        self.assertIsNone(dns4.authority_host)
        self.assertIsNone(dns4.authority_port)
        self.assertEqual("127.0.0.1", dns4.host)
        self.assertIsNone(dns4.port)
        self.assertEqual(f"dns:{uri4}", str(dns4))

        uri5 = "[2001:0db8:85a3:08d3:1319:8a2e:0370:7334]"
        dns5 = parse_rpc_dns_address(uri5)
        self.assertIsNone(dns5.authority)
        self.assertIsNone(dns5.authority_host)
        self.assertIsNone(dns5.authority_port)
        self.assertEqual("[2001:0db8:85a3:08d3:1319:8a2e:0370:7334]", dns5.host)
        self.assertIsNone(dns5.port)
        self.assertEqual(f"dns:{uri5}", str(dns5))

        uri6 = "0.0.0.0:9999"
        dns6 = parse_rpc_dns_address(uri6)
        self.assertIsNone(dns6.authority)
        self.assertIsNone(dns6.authority_host)
        self.assertIsNone(dns6.authority_port)
        self.assertEqual("0.0.0.0", dns6.host)
        self.assertEqual(9999, dns6.port)
        self.assertEqual(f"dns:{uri6}", str(dns6))

        uri7 = "[::1]:1234"
        dns7 = parse_rpc_dns_address(uri7)
        self.assertIsNone(dns7.authority)
        self.assertIsNone(dns7.authority_host)
        self.assertIsNone(dns7.authority_port)
        self.assertEqual("[::1]", dns7.host)
        self.assertEqual(1234, dns7.port)
        self.assertEqual(f"dns:{uri7}", str(dns7))

    def test_unix(self):
        uri1 = "unix:/var/recc.sock"
        unix1 = parse_rpc_unix_address(uri1)
        self.assertEqual("/var/recc.sock", unix1.path)
        self.assertEqual(uri1, str(unix1))

        uri2 = "unix:./recc.sock"
        unix2 = parse_rpc_unix_address(uri2)
        self.assertEqual("./recc.sock", unix2.path)
        self.assertEqual(uri2, str(unix2))

        uri3 = "unix:///var/recc.sock"
        unix3 = parse_rpc_unix_address(uri3)
        self.assertEqual("/var/recc.sock", unix3.path)
        self.assertEqual("unix:/var/recc.sock", str(unix3))

        with self.assertRaises(ValueError):
            parse_rpc_unix_address("unix://./recc.sock")

    def test_unix_abstract(self):
        uri = "unix-abstract:unknown.sock"
        unix_abs = parse_rpc_unix_abstract_address(uri)
        self.assertEqual("unknown.sock", unix_abs.abstract_path)
        self.assertEqual(uri, str(unix_abs))

    def test_ipv4(self):
        uri1 = "ipv4:192.168.0.1,0.0.0.0:9999"
        ip1 = parse_rpc_ipv4_addresses(uri1)
        self.assertEqual(2, len(ip1.addresses))
        self.assertEqual("192.168.0.1", ip1.addresses[0].address)
        self.assertIsNone(ip1.addresses[0].port)
        self.assertEqual("0.0.0.0", ip1.addresses[1].address)
        self.assertEqual(9999, ip1.addresses[1].port)
        self.assertEqual(uri1, str(ip1))

        uri2 = "ipv4:127.0.0.1:0"
        ip2 = parse_rpc_ipv4_addresses(uri2)
        self.assertEqual(1, len(ip2.addresses))
        self.assertEqual("127.0.0.1", ip2.addresses[0].address)
        self.assertEqual(0, ip2.addresses[0].port)
        self.assertEqual(uri2, str(ip2))

        with self.assertRaises(ValueError):
            parse_rpc_ipv4_addresses("ipv4:localhost")

    def test_ipv6(self):
        uri1 = "ipv6:[2607:f8b0:400e:c00::ef],[::]:1234"
        ip1 = parse_rpc_ipv6_addresses(uri1)
        self.assertEqual(2, len(ip1.addresses))
        self.assertEqual("[2607:f8b0:400e:c00::ef]", ip1.addresses[0].address)
        self.assertIsNone(ip1.addresses[0].port)
        self.assertEqual("[::]", ip1.addresses[1].address)
        self.assertEqual(1234, ip1.addresses[1].port)
        self.assertEqual(uri1, str(ip1))

        uri2 = "ipv6:[::1]"
        ip2 = parse_rpc_ipv6_addresses(uri2)
        self.assertEqual(1, len(ip2.addresses))
        self.assertEqual("[::1]", ip2.addresses[0].address)
        self.assertIsNone(ip2.addresses[0].port)
        self.assertEqual(uri2, str(ip2))

        with self.assertRaises(ValueError):
            parse_rpc_ipv6_addresses("ipv6:localhost")

    def test_parse_rpc_address(self):
        uri1 = "dns://dns-server:53/localhost:9999"
        addr1 = parse_rpc_address(uri1)
        self.assertEqual(RpcSchemeType.Dns, addr1[0])
        self.assertIsInstance(addr1[1], RpcDnsAddress)
        self.assertEqual("dns-server:53", addr1[1].authority)
        self.assertEqual("dns-server", addr1[1].authority_host)
        self.assertEqual(53, addr1[1].authority_port)
        self.assertEqual("localhost", addr1[1].host)
        self.assertEqual(9999, addr1[1].port)
        self.assertEqual(uri1, str(addr1[1]))

        uri2 = "[::1]:1234"
        addr2 = parse_rpc_address(uri2)
        self.assertEqual(RpcSchemeType.Dns, addr2[0])
        self.assertIsInstance(addr2[1], RpcDnsAddress)
        self.assertIsNone(addr2[1].authority)
        self.assertIsNone(addr2[1].authority_host)
        self.assertIsNone(addr2[1].authority_port)
        self.assertEqual("[::1]", addr2[1].host)
        self.assertEqual(1234, addr2[1].port)
        self.assertEqual(f"dns:{uri2}", str(addr2[1]))

        uri3 = "unix:/var/recc.sock"
        addr3 = parse_rpc_address(uri3)
        self.assertEqual(RpcSchemeType.Unix, addr3[0])
        self.assertIsInstance(addr3[1], RpcUnixAddress)
        self.assertEqual("/var/recc.sock", addr3[1].path)
        self.assertEqual(uri3, str(addr3[1]))

        uri4 = "unix-abstract:unknown.sock"
        addr4 = parse_rpc_address(uri4)
        self.assertEqual(RpcSchemeType.UnixAbstract, addr4[0])
        self.assertIsInstance(addr4[1], RpcUnixAbstractAddress)
        self.assertEqual("unknown.sock", addr4[1].abstract_path)
        self.assertEqual(uri4, str(addr4[1]))

        uri5 = "ipv4:192.168.0.1,0.0.0.0:9999"
        addr5 = parse_rpc_address(uri5)
        self.assertEqual(RpcSchemeType.Ipv4, addr5[0])
        self.assertIsInstance(addr5[1], RpcIpv4Addresses)
        self.assertEqual(2, len(addr5[1].addresses))
        self.assertEqual("192.168.0.1", addr5[1].addresses[0].address)
        self.assertIsNone(addr5[1].addresses[0].port)
        self.assertEqual("0.0.0.0", addr5[1].addresses[1].address)
        self.assertEqual(9999, addr5[1].addresses[1].port)
        self.assertEqual(uri5, str(addr5[1]))

        uri6 = "ipv6:[2607:f8b0:400e:c00::ef],[::]:1234"
        addr6 = parse_rpc_address(uri6)
        self.assertEqual(RpcSchemeType.Ipv6, addr6[0])
        self.assertIsInstance(addr6[1], RpcIpv6Addresses)
        self.assertEqual(2, len(addr6[1].addresses))
        self.assertEqual("[2607:f8b0:400e:c00::ef]", addr6[1].addresses[0].address)
        self.assertIsNone(addr6[1].addresses[0].port)
        self.assertEqual("[::]", addr6[1].addresses[1].address)
        self.assertEqual(1234, addr6[1].addresses[1].port)
        self.assertEqual(uri6, str(addr6[1]))


class ParseRpcAddressAsClassTestCase(TestCase):
    def test_case_01(self):
        address = "dns://dns-server:53/localhost:1234"
        obj = parse_rpc_address_as_class(address)
        self.assertTrue(obj.is_dns)
        self.assertFalse(obj.is_unix)
        self.assertFalse(obj.is_unix_abstract)
        self.assertFalse(obj.is_ipv4)
        self.assertFalse(obj.is_ipv6)
        self.assertTrue(obj.has_dns_authority)
        self.assertTrue(obj.has_dns_host)
        self.assertTrue(obj.has_dns_port)
        self.assertFalse(obj.has_unix_path)
        self.assertFalse(obj.has_unix_abstract_path)
        self.assertFalse(obj.has_ipv4_addresses)
        self.assertFalse(obj.has_ipv6_addresses)
        self.assertFalse(obj.has_ip_addresses)
        self.assertTrue(obj.has_any_port)
        self.assertEqual(1, len(obj.all_ports))
        self.assertEqual(1234, obj.all_ports[0])
        self.assertIsInstance(obj.as_dns, RpcDnsAddress)
        self.assertRaises(TypeError, lambda: obj.as_unix)
        self.assertRaises(TypeError, lambda: obj.as_unix_abstract)
        self.assertRaises(TypeError, lambda: obj.as_ipv4)
        self.assertRaises(TypeError, lambda: obj.as_ipv6)
        self.assertEqual("dns-server:53", obj.authority)
        self.assertEqual("dns-server", obj.authority_host)
        self.assertEqual(53, obj.authority_port)
        self.assertEqual("localhost", obj.host)
        self.assertEqual(1234, obj.port)
        self.assertRaises(TypeError, lambda: obj.path)
        self.assertRaises(TypeError, lambda: obj.abstract_path)
        self.assertRaises(TypeError, lambda: obj.addresses)
        self.assertEqual(address, str(obj))
        self.assertEqual(address, repr(obj))

    def test_case_02(self):
        address = "ipv6:[2607:f8b0:400e:c00::ef],[::]:1234,[::1]:80"
        obj = parse_rpc_address_as_class(address)
        self.assertFalse(obj.is_dns)
        self.assertFalse(obj.is_unix)
        self.assertFalse(obj.is_unix_abstract)
        self.assertFalse(obj.is_ipv4)
        self.assertTrue(obj.is_ipv6)
        self.assertFalse(obj.has_dns_authority)
        self.assertFalse(obj.has_dns_host)
        self.assertFalse(obj.has_dns_port)
        self.assertFalse(obj.has_unix_path)
        self.assertFalse(obj.has_unix_abstract_path)
        self.assertFalse(obj.has_ipv4_addresses)
        self.assertTrue(obj.has_ipv6_addresses)
        self.assertTrue(obj.has_ip_addresses)
        self.assertTrue(obj.has_any_port)
        self.assertEqual(2, len(obj.all_ports))
        self.assertEqual(1234, obj.all_ports[0])
        self.assertEqual(80, obj.all_ports[1])
        self.assertRaises(TypeError, lambda: obj.as_dns)
        self.assertRaises(TypeError, lambda: obj.as_unix)
        self.assertRaises(TypeError, lambda: obj.as_unix_abstract)
        self.assertRaises(TypeError, lambda: obj.as_ipv4)
        self.assertIsInstance(obj.as_ipv6, RpcIpv6Addresses)
        self.assertRaises(TypeError, lambda: obj.authority)
        self.assertRaises(TypeError, lambda: obj.authority_host)
        self.assertRaises(TypeError, lambda: obj.authority_port)
        self.assertRaises(TypeError, lambda: obj.host)
        self.assertRaises(TypeError, lambda: obj.port)
        self.assertRaises(TypeError, lambda: obj.path)
        self.assertRaises(TypeError, lambda: obj.abstract_path)
        self.assertEqual(3, len(obj.addresses))
        self.assertEqual("[2607:f8b0:400e:c00::ef]", obj.addresses[0].address)
        self.assertIsNone(obj.addresses[0].port)
        self.assertEqual("[::]", obj.addresses[1].address)
        self.assertEqual(1234, obj.addresses[1].port)
        self.assertEqual("[::1]", obj.addresses[2].address)
        self.assertEqual(80, obj.addresses[2].port)
        self.assertEqual(address, str(obj))
        self.assertEqual(address, repr(obj))


if __name__ == "__main__":
    main()
