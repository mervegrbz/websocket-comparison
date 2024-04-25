import asyncio
import websockets
import time

class MySocketClient:
    def __init__(self, port):
        self.port = port + 5000
        self.connection_count = 0
        self.disconnect_count = 0

    async def connect(self):
        try:
            con_time = time.time()
            self.websocket = await websockets.connect(f'ws://localhost:{self.port}', ping_timeout=None, ping_interval=None)
            con_fin = time.time()
            print(f'connection time: {con_fin - con_time}')
            self.connection_count += 1
            
        except Exception as e:
            
            print("error on con", e)

    async def write(self, data):
        print('Received:', data)
        
    async def test_event(self, message_size, num_messages):
        messages = [b"x" * message_size for _ in range(num_messages)]
        start_time = time.time()
        for message in messages:
            await self.websocket.send(message)
            await asyncio.sleep(0)
           
        duration = time.time() - start_time
        return duration
        

    async def disconnect(self):
        try:
            await self.websocket.close()
        except Exception as e:  
            print("error on discon", e)
            self.disconnect_count += 1
            

    async def start(self):
        try:
            await self.connect()
            print("connected")
            await self.test_event(100, 100)
            print("sent")
            await asyncio.Future()
            await self.disconnect()
        except Exception as e:
            print("error", e)

if __name__ == "__main__":
    client = MySocketClient(0)
    asyncio.run(client.start())
