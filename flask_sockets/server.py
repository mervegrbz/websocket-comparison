import socketio
import uvicorn
import time
sio = socketio.AsyncServer( async_mode='asgi')
app = socketio.ASGIApp(sio)

connection_count = 0
disconnect_count = 0
background_task_started = False
send_times = []
connects = []
client_count = 0


@sio.event
async def connect(sid, environ, auth):
    global connection_count
    connection_count += 1
    obj = {'connect': sid, 'time': time.time(), 'disconnect': None}
    connects.append(obj)
    print('connect ', sid)
    global background_task_started
   
    sio.start_background_task(background_task)
    background_task_started = True
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)
    
async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(1)
        count += 1
        snd_start = time.time()
        await sio.emit('my_response', {'data': 'Server generated event'})
        snd_finish = time.time()
        send_times.append(snd_start-snd_finish)
        
@sio.event
async def my_event(sid, data):
    print(f'Received data from {sid}: {data}')
    await sio.emit('my_event', data='Hello from the server', room=sid) 
    
@sio.event
async def disconnect(sid):
  global disconnect_count
  disconnect_count += 1
  obj = next((item for item in connects if item["connect"] == sid), None)
  obj['disconnect'] = time.time()
  
  write_results()
  
  
def start(N):
  global client_count
  client_count = N
  
  uvicorn.run(app, host="localhost", port=N+5000, log_level="critical")
    
    
# write the results to a file
def write_results():
    global connection_count,  disconnect_count, send_times, connects, client_count
    with open(f'results{client_count}.txt', 'w') as f:
        f.write(f'Connection count: {connection_count}\n')
        f.write(f'Disconnection count: {disconnect_count}\n')
        f.write(f'Send times: {send_times}\n')
        f.write(f'Connects: {connects}\n')
    

if __name__ == '__main__':
    start()