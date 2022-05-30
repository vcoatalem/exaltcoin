import asyncio
from audioop import add

from registry import Registry
from history import History, history

import json
import os
import websockets

from identification import username

async def send_message(address: str, payload: dict) -> dict:
    async with websockets.connect("ws://" + address) as websocket:
        await websocket.send(json.dumps(payload))
        res = await websocket.recv()
        return json.loads(res)

def format_send_coins(coins: int, sender: str) -> dict:
    return {
        "action": "send coins",
        "amount": coins,
        "from": sender
    }

def send(to: str, coins: int):
    address = Registry.get_address(to)
    if (address == None):
        print("Could not get address for user: " + to + ". Will try to fetch it from registry")
        address = Registry.fetch_address(to)
        if (address == None):
            print("Could not fetch address for user: " + to + " from registry.")
            return None
    if coins < History.get_current_coin_amount():
        print("you do not have that many coins !")
    print(f"will send {coins} coins to {to} at address {address}")
    payload = format_send_coins(coins=coins, sender=username())
    res = asyncio.run(send_message(address=address, payload=payload))
    print("server returned: ", res)
    History.save_transaction(src=res["from"], amount=res["amount"])

def receive(src: str, amount: int):
    History.save_transaction(src=src, amount=amount)
    return {
        "action": "save transaction",
        "from": os.getenv('EXALTCOIN_USERNAME'),
        "amount": -amount
    }
