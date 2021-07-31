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

def calc_emas(curr_vals, prev_emas):
    curr_emas = []
    for i in range(len(curr_vals)):
        curr_ema = EMA_ALPHA * curr_vals[i] + (1.0 - EMA_ALPHA)*prev_emas[i]
        curr_emas.append(curr_ema)
    return curr_emas

def is_dark(curr_ema_lum):
    if curr_ema_lum < LUM_TH: return True
    else: return False

def is_moved(curr_ema_accs, prev_ema_accs):
    diff = 0.0
    for curr, prev in zip(curr_ema_accs, prev_ema_accs):
        diff += abs(curr - prev)
    if diff > ACC_TH: return True
    else: return False

def flash():
    for i in range(FLASH_COUNT):
        led.on()
        sleep(FLASH_INTERVAL_SEC)
        led.off()
        sleep(FLASH_INTERVAL_SEC)







    







def main():

    led_switch = None
    curr_vals = []
    prev_emas = []
    uri = "ws://192.168.1.12:3000"

    while True:

        curr_vals = [lum.value, ax.value, ay.value, az.value]
        if len(prev_emas) > 0:
            curr_emas = calc_emas(curr_vals, prev_emas)
    
            if is_dark(curr_emas[0]): led.on()
            else: 
                led.off()
            
            if is_moved(curr_emas[1:], prev_emas[1:]):
                asyncio.get_event_loop().run_until_complete(send_flush(uri))
            else:
                asyncio.get_event_loop().run_until_complete(send_flush_off(uri))


            led_switch = asyncio.create_task(receive_server(uri))
            if led_switch == "on":
                flash()

            prev_emas = copy.deepcopy(curr_emas)
        
        else:
            prev_emas = copy.deepcopy(curr_vals)
 


async def send_flush(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(f"on")

async def send_flush_off(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(f"off")

async def receive_server(uri):
    async with websockets.connect(uri) as websocket:
        data = await websocket.recv()
        return data

if __name__ == "__main__":
    main()