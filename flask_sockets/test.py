
import asyncio
import client
import time
import server
import threading


num_clients = [100, 300, 500, 700, 1000]
threads = []
def start_server(N):
  global threads
  print("Starting server")
  # start server
  # start server in a thread
  threads.append(threading.Thread(target=server.start, args=(N,)))
  print("Server started")
  # 

async def start_client(N):
  print("Starting client")
  # start N clients using threads 
  tasks = []
  for _ in range(N):
    cli = client.MySocketClient(N)
    tasks.append(cli.start())
  # record the time to wait for all clients to finish
  start_timestamp = time.time()
  res = await asyncio.gather(*tasks)
  end_timestamp = time.time()
  print(end_timestamp - start_timestamp)
  
  
  
for i in range(5):
  start_server(num_clients[i])
print(len(threads))
for i in range(5):
  threads[i].start()

for i in range(5):
  asyncio.run(start_client(num_clients[i]))

  
for i in range(5):
  threads[i].join()
  
  
 
  

  

  