import socket
import unittest
from unittest import mock
from http_protocol import Http


class HttpTests(unittest.TestCase):
    def test_init(self) -> None:
        server_connection = socket.socket()
        browser_connection = socket.socket()
        protocol = Http('host', 80, b'request', server_connection,
                        browser_connection)
        self.assertEqual(protocol.host, 'host')

    def test_get_response(self):
        mock_server_connection = mock.Mock()
        mock_browser_connection = mock.Mock()
        mock_server_connection.recv.return_value = b''
        with mock.patch('adblock.AdBlock.block') as mock_block:
            mock_block.return_value = b''
            mock_browser_connection.sendall.side_effect = socket.timeout
            protocol = Http('host', 443, b'request', mock_server_connection,
                            mock_browser_connection)
            self.assertEqual(protocol.get_response(), None)
