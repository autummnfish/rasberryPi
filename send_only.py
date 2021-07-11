import asyncio
import websockets


async def hello():
    uri = "ws://192.168.1.14:3000"
    async with websockets.connect(uri) as websocket:
        await websocket.send("YEAH")
        res = await websocket.recv()
        print(res)

asyncio.get_event_loop().run_until_complete(hello())