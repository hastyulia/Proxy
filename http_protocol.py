import re
import socket
from adblock import AdBlock


BUFFER = 1024


class Http:
    def __init__(self, host: str, port: int, request: bytes,
                 server_connection: socket.socket,
                 browser_connection: socket.socket) -> None:
        self.host = host
        self.port = port
        self.request = request
        self.server_connection = server_connection
        self.browser_connection = browser_connection

    def get_response(self) -> None:
        self.request = re.sub(rb'\r\nAccept-Encoding: [a-z\-, ]*?\r\n',
                              b'\r\nAccept-Encoding: deflate\r\n',
                              self.request)
        self.server_connection.connect((self.host, self.port))
        self.server_connection.send(self.request)
        response = b''
        blocker = AdBlock()
        while True:
            try:
                data = self.server_connection.recv(BUFFER)
                response += data
                if not data:
                    response = blocker.block(response)
                    self.browser_connection.sendall(response)
            except socket.timeout:
                break

        self.server_connection.shutdown(1)
        self.server_connection.close()
