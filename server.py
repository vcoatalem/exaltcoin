import asyncio
import json
import websockets

from coins_exchange import receive

def handle_message(res: str):
    res_json = json.loads(res)
    if "action" not in res_json:
        return lambda : print("could not find action in message")
    if res_json["action"] == "send coins":
        try:
            src = res_json["from"]
            coins = int(res_json["amount"])
            return lambda : receive(src, coins)
        except:
            return lambda : print("error while parsing send coins message")


async def echo(websocket):
    async for message in websocket:
        print(message)
        f = handle_message(message)
        res = f()
        if res == None:
            res = json.dumps({"error": "Error while processing message"})
        await websocket.send(json.dumps(res))

async def main():
    async with websockets.serve(echo, "127.0.0.1", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())