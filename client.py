import asyncio
import websockets
connected = set()

async def hello():
#サーバ側のラズパイのIPアドレスを指定
    # uri = "ws://192.168.1.13:3000"
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:
        connected.add(websocket)
        try:
            await asyncio.wait([ws.send("HELLO") for ws in connected])
            await asyncio.sleep(1)
        finally:
            connected.remove(websocket)
        # res = await websocket.recv()
        
asyncio.get_event_loop().run_until_complete(hello())