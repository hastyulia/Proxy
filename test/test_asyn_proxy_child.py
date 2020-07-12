import unittest
from asyn_proxy import HTTPProxyProtocol
from HTTPProxyProtocolChild import HTTPProxyProtocolChild


class HTTPProxyProtocolChildTests(unittest.TestCase):
    def test_init(self) -> None:
        parent = HTTPProxyProtocol
        proxy = HTTPProxyProtocolChild(parent, '')
        self.assertEqual(proxy.parent, HTTPProxyProtocol)

    def test_init_bytes(self) -> None:
        parent = HTTPProxyProtocol
        proxy = HTTPProxyProtocolChild(parent, b'')
        self.assertEqual(proxy.parent, HTTPProxyProtocol)

    def test_connection_made(self):
        parent = HTTPProxyProtocol
        proxy = HTTPProxyProtocolChild(parent, '')
        with self.assertRaises(AttributeError):
            proxy.connection_made(proxy.transport)

    def test_eof_received(self):
        parent = HTTPProxyProtocol
        proxy = HTTPProxyProtocolChild(parent, '')
        with self.assertRaises(AttributeError):
            proxy.parent.transport.eof_received()

    def test_data_received(self):
        parent = HTTPProxyProtocol
        proxy = HTTPProxyProtocolChild(parent, '')
        with self.assertRaises(AttributeError):
            proxy.parent.transport.data_received('')
