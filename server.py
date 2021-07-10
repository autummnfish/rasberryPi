import asyncio
import websockets
connection = set()



async def handler(websocket,path):
    async for ws in websocket:
        connection.add(websocket)
        data = websocket.recv()
        print(ws)
        await asyncio.wait([ws.send(f"{data} !") for ws in connection])

async def hello(websocket, path):
    connection.add(websocket)
    print(len(connection))
    try:
        data = await websocket.recv()
        print(data)

        await asyncio.wait([ws.send(f"{data} !") for ws in connection])
        await asyncio.sleep(10)
    finally:
        connection.remove(websocket)

start_server = websockets.serve(hello, "0.0.0.0", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
