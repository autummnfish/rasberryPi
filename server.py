import asyncio
import websockets
connection = set()

async def hello(websocket, path):
    connection.add(websocket)
    try:
        data = await websocket.recv()
        print(data)
        await websocket.send(f"heo")
        await asyncio.sleep(10)
    finally:
        connection.remove(websocket)

start_server = websockets.serve(hello, "0.0.0.0", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()