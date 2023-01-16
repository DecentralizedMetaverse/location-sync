import socket
import json
import asyncio

class Program:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        asyncio.run(self.handle_server())

    def connect(self, ip, port):
        self.sock.connect((ip, port))

    async def handle_server(self):
        self.sock.listen(8888)
        self.sock.setblocking(False)

        loop = asyncio.get_event_loop()

        while True:
            client, _ = await loop.sock_accept(self.sock)
            loop.create_task(self.handle_client(client)) # 新規受信

    async def handle_client(self, client):
        loop = asyncio.get_event_loop()
        
        request = None
        while request != 'quit':
            request = (await loop.sock_recv(client, 255)).decode('utf8')
            response = str(eval(request)) + '\n'
            await loop.sock_sendall(client, response.encode('utf8'))
        client.close()
