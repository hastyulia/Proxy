import socket
import unittest
from unittest import mock
from https_protocol import Https


class HttpsTests(unittest.TestCase):
    def test_init(self) -> None:
        server_connection = socket.socket()
        browser_connection = socket.socket()
        protocol = Https('host', 80, b'request', server_connection,
                         browser_connection)
        self.assertEqual(protocol.host, 'host')

    def test_get_response_server_exception(self) -> None:
        mock_server_connection = socket.socket()
        mock_browser_connection = mock.Mock()
        protocol = Https('host', 443, b'request', mock_server_connection,
                         mock_browser_connection)
        with self.assertRaises(Exception):
            protocol.get_response()

    def test_communication_through_tunnel(self) -> None:
        mock_server_connection = mock.Mock()
        mock_browser_connection = mock.Mock()
        mock_server_connection.recv.side_effect = Exception
        mock_server_connection.sendall.side_effect = socket.timeout
        protocol = Https('host', 443, b'request', mock_server_connection,
                         mock_browser_connection)
        with self.assertRaises(Exception):
            protocol.communication_through_tunnel()
