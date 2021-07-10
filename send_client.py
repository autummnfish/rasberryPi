import asyncio
import websockets



async def hello():
    uri = "ws://192.168.1.12:3000"
    async with websockets.connect(uri) as websocket:
        while True:
           
            name = input("What's your name? ")
                
            await websocket.send(name)
            greeting = await websocket.recv()
            print(f"< {greeting}")


asyncio.get_event_loop().run_until_complete(hello())