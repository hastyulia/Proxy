import asyncio
from asyn_proxy_child import HTTPProxyProtocolChild

HTTP_PORT = 80


class HTTPProxyProtocol(asyncio.BaseProtocol):
    def __init__(self, child: HTTPProxyProtocolChild = None) -> None:
        self.transport = None
        self.child = child

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport

    def eof_received(self) -> None:
        self.child.transport.write_eof()

    def data_received(self, data: bytes) -> None:
        if self.child is not None:
            self.child.transport.write(data)
            return

        split_request = data.split(b'\r\n', maxsplit=1)
        http_index = split_request[0].find(b'http:')
        host = split_request[1].split()[1].decode()
        if http_index == -1:
            port = int(split_request[0].split()[1].split(b':')[1])
            data = ''
        else:
            data = data
            port = HTTP_PORT

        self.child = HTTPProxyProtocolChild(self, data)
        loop = asyncio.get_event_loop()
        coroutine = loop.create_connection(lambda: self.child, host, port=port)
        future = asyncio.ensure_future(coroutine)
        if http_index == -1:
            future.add_done_callback(lambda f: self.transport.write(
                b'HTTP/1.0 200 OK\r\n\r\n'))


async def listen(host: str = '127.0.0.1',
                 port: int = 8080) -> asyncio.AbstractServer:
    loop = asyncio.get_event_loop()
    server = await loop.create_server(HTTPProxyProtocol, host, port)
    return server
