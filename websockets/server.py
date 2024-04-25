import asyncio
import websockets
import time

connection_count = 0
disconnect_count = 0
background_task_started = False
send_times = []
connects = []
client_count = 0
recv_times = []
async def connect(websocket, path):
    global connection_count
    connection_count += 1
    obj = {'connect': websocket, 'time': time.time(), 'disconnect': None}
    connects.append(obj)
    print('connect ', websocket)
    recv_time = time.time()
    for i in range(100):
        message = await websocket.recv()
        print("message", message)
        # await websocket.send(message)
    recv_finish = time.time()
    print("recv time", recv_finish - recv_time)
    recv_times.append(recv_finish - recv_time)

async def disconnect(websocket, path):
    global disconnect_count
    disconnect_count += 1
    obj = next((item for item in connects if item["connect"] == websocket), None)
    obj['disconnect'] = time.time()
    await websocket.close()
    write_results()

async def send_test(message_size, num_messages, websocket):
    global send_times
    reply =  [b"x" * message_size for _ in range(num_messages)]
    send_time = time.time()
    for message in reply:
        [print("message", message)]
        await websocket.send(message)  # Send the message
        response = await websocket.recv()  # Wait for acknowledgment
    send_finish = time.time()
    send_times.append(send_finish - send_time)
    
# write the results to a file
def write_results():
    global connection_count,  disconnect_count, send_times, connects, client_count
    with open(f'results{client_count}.txt', 'w') as f:
        f.write(f'Connection count: {connection_count}\n')
        f.write(f'Disconnection count: {disconnect_count}\n')
        f.write(f'Send times: {send_times}\n')
        f.write(f'Connects: {connects}\n')

async def main(i):
    stop = asyncio.Future()
    server = await websockets.serve(connect, "localhost", 5000+i, ping_timeout=None, ping_interval=None)
    write_results()
    await stop
    await server.close(close_connections=True)# run forever

if __name__ == "__main__":
    asyncio.run(main(0))
    
   