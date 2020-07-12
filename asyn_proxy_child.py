import asyncio


class HTTPProxyProtocolChild(asyncio.BaseProtocol):
    def __init__(self, parent: asyncio.BaseProtocol,
                 initial_data: str or bytes) -> None:
        self.transport = None
        self.parent = parent
        if type(initial_data) == str:
            self.initial_data = initial_data.encode()
        else:
            self.initial_data = initial_data
        super().__init__()

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport
        transport.write(self.initial_data)

    def data_received(self, data: bytes) -> None:
        self.parent.transport.write(data)

    def eof_received(self) -> None:
        self.parent.transport.write_eof()
