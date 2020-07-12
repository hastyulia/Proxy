import asyncio
import unittest
import asyn_proxy
from unittest import mock
from asyn_proxy import HTTPProxyProtocol
from HTTPProxyProtocolChild import HTTPProxyProtocolChild


class AsyncProxyTests(unittest.TestCase):
    def test_listen(self) -> None:
        with mock.patch('asyncio.get_event_loop') as mock_loop:
            mock_loop.return_value = 'ggg'
            return_value = (asyncio.ensure_future(
                    asyn_proxy.listen(host='127.0.0.1', port=17000)))
            return_value_type = str(type(return_value))
            self.assertEqual(return_value_type, "<class '_asyncio.Task'>")

    def test_HTTP_init(self) -> None:
        proxy = HTTPProxyProtocol()
        self.assertEqual(proxy.child, None)

    def test_connection_made(self):
        proxy = HTTPProxyProtocol()
        self.assertEqual(proxy.connection_made(proxy.transport), None)

    def test_eof_received(self):
        proxy = HTTPProxyProtocol()
        with self.assertRaises(AttributeError):
            proxy.child.transport.eof_received()

    def test_data_received_not_none(self):
        parent = HTTPProxyProtocol
        child = HTTPProxyProtocolChild(parent, 'a')
        proxy = HTTPProxyProtocol(child)
        with self.assertRaises(AttributeError):
            proxy.data_received(b's')

    def test_data_received_none(self):
        proxy = HTTPProxyProtocol(None)
        self.assertEqual(proxy.data_received(b'CONNECT /index.py:443 HTTP/1.1'
                                             b'\r\nHost: www.ym.ru'), None)

    def test_data_received_none_https(self):
        proxy = HTTPProxyProtocol(None)
        self.assertEqual(proxy.data_received(b'CONNECT http://index.py HTTP/'
                                             b'1.1\r\nHost: www.ym.ru'), None)
