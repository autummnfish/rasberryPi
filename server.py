import asyncio
import websockets

async def echo(websocket,path):
    while True:
        data = await websocket.recv()
        print('Received')
        await websocket.send(data)
        
# start_server = websockets.serve(echo, "0.0.0.0",3000)
start_server = websockets.serve(echo, "localhost",3000)





asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()