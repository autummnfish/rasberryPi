import asyncio
import websockets
import os
connection = set()


async def server_test(websocket, path):
    connection.add(websocket)
    try:
        data = await websocket.recv()
        await asyncio.create_task(broadcast_without_self(websocket,data))
        await asyncio.sleep(2)
    finally:
        connection.remove(websocket)


async def broadcast_without_self(self,msg):
    for ws in connection:
        # if ws == self:
        #     continue
        await ws.send(msg)



def main():
    start_server = websockets.serve(server_test, "", int(os.environ["PORT"]))
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()