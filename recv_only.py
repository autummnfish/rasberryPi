import copy
from gpiozero import MCP3208
from gpiozero import LED
from time import sleep
import asyncio
import websockets

EMA_ALPHA = 0.2
LUM_TH = 0.8
ACC_TH = 0.02
FLASH_COUNT = 5
FLASH_INTERVAL_SEC = 0.1
SENSOR_INTERVAL_SEC = 0.1

lum = MCP3208(channel=0)
ax = MCP3208(channel=5)
ay = MCP3208(channel=6)
az = MCP3208(channel=7)
led = LED(17)

def flash():
    for i in range(FLASH_COUNT):
        led.on()
        sleep(FLASH_INTERVAL_SEC)
        led.off()
        sleep(FLASH_INTERVAL_SEC)


async def hello(websocket, path):
    data = await websocket.recv()
    print(data)
    if data:
        flash()
    await websocket.send(f"NICE!")
   

start_server = websockets.serve(hello, "0.0.0.0", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()