import ssl
import socket
from adblock import AdBlock


BUFFER = 1024


class Https:
    KEY_FILENAME = 'my.key'
    CERT_FILENAME = 'my.crt'

    def __init__(self, host: str, port: int, request: bytes,
                 server_connection: socket.socket,
                 browser_connection: socket.socket) -> None:
        self.host = host
        self.port = port
        self.request = request
        self.server_connection = server_connection
        self.browser_connection = browser_connection
        self.reply_for_connect = b'HTTP/1.0 200 OK\r\n\r\n'

    def get_response(self) -> None:
        self.server_connection = ssl.wrap_socket(self.server_connection,
                                                 keyfile=self.KEY_FILENAME,
                                                 certfile=self.CERT_FILENAME,
                                                 server_side=False,
                                                 ssl_version=ssl.PROTOCOL_TLS,
                                                 do_handshake_on_connect=True
                                                 )
        self.browser_connection.sendall(self.reply_for_connect)
        self.browser_connection = ssl.wrap_socket(self.browser_connection,
                                                  keyfile=self.KEY_FILENAME,
                                                  certfile=self.CERT_FILENAME,
                                                  server_side=True,
                                                  ssl_version=ssl.PROTOCOL_TLS,
                                                  do_handshake_on_connect=False
                                                  )
        self.server_connection.connect((self.host, self.port))
        self.communication_through_tunnel()

    def communication_through_tunnel(self) -> None:

        self.browser_connection.settimeout(0)
        self.server_connection.settimeout(0)
        response = b''
        blocker = AdBlock()
        while True:
            try:
                request = self.browser_connection.recv(BUFFER)
                self.server_connection.sendall(request)
            except socket.error:
                pass
            try:
                data = self.server_connection.recv(BUFFER)
                response += data
                if not data:
                    response = blocker.block(response)
                    self.browser_connection.sendall(response)

            except socket.error:
                pass
