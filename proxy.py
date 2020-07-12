import sys
import socket
import asyncio
import asyn_proxy
from threading import Thread
from http_protocol import Http
from https_protocol import Https


class Server(Thread):
    HTTP_PORT = 80
    BUFFER = 1024

    def __init__(self, browser_connection: socket.socket) -> None:
        super().__init__()
        self.browser_connection = browser_connection

    def run(self) -> None:
        while True:
            request = self.browser_connection.recv(self.BUFFER)
            if not request:
                break

            self.get_response(request)

        self.browser_connection.shutdown(1)
        self.browser_connection.close()

    def get_response(self, request: bytes) -> None:
        split_request = request.split(b'\r\n', maxsplit=1)
        http_index = split_request[0].find(b'http:')
        host = split_request[1].split()[1].decode()
        if http_index == -1:
            port = int(split_request[0].split()[1].split(b':')[1])

        else:
            port = self.HTTP_PORT

        server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_connection.settimeout(2.0)
        server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        if port == self.HTTP_PORT:
            protocol = Http(host, port, request, server_connection,
                            self.browser_connection)
        else:
            protocol = Https(host, port, request, server_connection,
                             self.browser_connection)

        protocol.get_response()


def listen(host='127.0.0.1', port=17000) -> None:
    browser_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    browser_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    browser_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    browser_connection.bind((host, port))
    browser_connection.listen(20)
    while True:
        current_connection, address = browser_connection.accept()
        server = Server(current_connection)
        server.start()


def main():
    proxy_type = sys.argv[1]
    try:
        if proxy_type == 'async':
            asyncio.ensure_future(asyn_proxy.listen(proxy_host, proxy_port))
            asyncio.get_event_loop().run_forever()
        if proxy_type == 'thread':
            listen(proxy_host, proxy_port)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    # proxy_host = input('Enter proxy host: ')
    # proxy_port = int(input('Enter proxy port: '))
    # main()
    listen()
