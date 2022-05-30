import asyncio
from audioop import add
import coins_exchange
import identification
import json
import websockets

from history import History
from registry import Registry

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
    if res_json["action"] == "get address":
        return identification.get_address()
    if res_json["action"] == "get user":
        return identification.get_username()
    if res_json["action"] == "get history":
        return History.get()
    if res_json["action"] == "get registry":
        return Registry.get()
    if res_json["action"] == "get coins":
        return History.get_coins()
    if res_json["action"] == "send coins":
        return coins_exchange.send(res_json["to"], res_json["amount"])
    if res_json["action"] == "add user":
        address = Registry.fetch_address(username=res_json["username"])
        return {
            "action": "add user",
            "username": res_json["username"],
            "address": address
        }
    #if res_json["action"] == "get servername":
    #    retur


async def echo(websocket):
    async for message in websocket:
        print(message)
        f = handle_message(message)
        res = f()
        if res == None:
            res = json.dumps({"error": "Error while processing message"})
        await websocket.send(json.dumps(res))

async def main():
    async with websockets.serve(ws_handler=echo, port=8765):
        await asyncio.Future()  # run forever

asyncio.run(main())