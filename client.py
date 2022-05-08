import asyncio
import json
import websockets

from pprint import pprint

async def send_message(address: str, payload: dict) -> dict:
    async with websockets.connect("ws://" + address) as websocket:
        await websocket.send(json.dumps(payload))
        res = await websocket.recv()
        return json.loads(res)



