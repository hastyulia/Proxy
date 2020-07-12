import proxy
import socket
import unittest
from unittest import mock


class ProxyTests(unittest.TestCase):
    def test_main_thread(self) -> None:
        with mock.patch('sys.argv') as mock_argv:
            mock_argv.return_value = 'proxy.py thread'
            self.assertEqual(proxy.main(), None)

    def test_main_async(self) -> None:
        with mock.patch('sys.argv') as mock_argv:
            mock_argv.return_value = 'proxy.py async'
            self.assertEqual(proxy.main(), None)

    def test_listen(self) -> None:
        mock_socket = mock.Mock()
        mock_socket.recv.return_value = ''
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.accept.return_value = ('', -1)
            with mock.patch('proxy.Server') as mock_server:
                mock_server.return_value = 'ggg'
                with self.assertRaises(AttributeError):
                    proxy.listen()

    def test_server_init(self):
        mock_socket = mock.Mock()
        server = proxy.Server(mock_socket)
        self.assertEqual(server.browser_connection, mock_socket)

    def test_server_run(self):
        mock_socket = mock.Mock()
        mock_socket.recv.return_value = ''
        server = proxy.Server(mock_socket)
        self.assertEqual(server.run(), None)

    def test_server_get_response_https(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = proxy.Server(connection)
        with self.assertRaises(OSError):
            server.get_response(b'CONNECT /index.py:443 HTTP/1.1\r\n'
                                b'Host: www.ym.ru')

    def test_server_get_response_http(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = proxy.Server(connection)
        with self.assertRaises(OSError):
            server.get_response(b'CONNECT http://index.py HTTP/1.1\r\n'
                                b'Host: www.ym.ru')
