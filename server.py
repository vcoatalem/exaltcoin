import asyncio
import json
import websockets

from fs.history import save_transaction

import os


def handle_message(res: str):
    res_json = json.loads(res)
    if "action" not in res_json:
        return lambda : print("could not find action in message")
    if res_json["action"] == "send coins":
        try:
            sender = res_json["from"]
            coins = int(res_json["amount"])
            return lambda : receive_coins(sender, coins)
        except:
            return lambda : print("error while parsing send coins message")


async def handle_socket(websocket):
    async for message in websocket:
        print(message)
        f = handle_message(message)
        res = f()
        if res == None:
            res = json.dumps({"error": "Error while processing message"})
        await websocket.send(json.dumps(res))


def receive_coins(sender: str, amount: int):
    save_transaction(src=sender, amount=amount)
    return {
        "action": "save transaction",
        "from": sender,
        "amount": amount
    }

async def serve():
    async with websockets.serve(ws_handler=handle_socket, port=8765):
        await asyncio.Future()  # run forever

asyncio.run(serve())