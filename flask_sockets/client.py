import asyncio
import socketio
import time


class MySocketClient:
    def __init__(self,port):
        self.sio = socketio.AsyncClient()
        self.port = port + 5000 

    async def connect(self):
        try:
            con_time = time.time()
            await self.sio.connect(f'http://localhost:{self.port}', wait_timeout=10 )
            con_fin = time.time()
            print(f'connection time: {con_fin - con_time}')
        except Exception as e:
            print("error on con", e)
            
    def write(self, data):
        pass   
        
    async def my_event(self, data):
        recv_time = time.time()
        await self.sio.emit('my_event', {'data': f'client response {self.sio.sid}'})
        recv_time_fin = time.time()
        print(f'receive time: {recv_time_fin - recv_time}')
        
    async def disconnect(self):
      await self.sio.disconnect()
      

    async def start(self):
        try:
            await self.connect()  
            await self.my_event('helo')
            self.sio.on('my_response', self.write)
            self.sio.on('my_event', self.write)
            await self.sio.sleep(1)
            await self.disconnect()
        except Exception as e:
            print("error", e)

if __name__ == "__main__":
    client = MySocketClient()
    asyncio.run(client.start())

