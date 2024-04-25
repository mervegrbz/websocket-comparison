
import asyncio
import client
import time
import server
import threading


num_clients = [100, 300, 500, 700, 1000]
threads = []
async def start_server(N):
  print("Starting server")
  # start server
  # start server in a thread
  await server.main(N)
  
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
  
  
  

# asyncio.run(start_server(num_clients[0]))
 

for i in range(5):
  asyncio.run(start_client(num_clients[i]))

  
  
 
  

  

  