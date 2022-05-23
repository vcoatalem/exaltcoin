import asyncio
from audioop import add

from client import send_message
from registry import Registry
from history import History

from dotenv import load_dotenv
import json
import os

from identification import username

load_dotenv()


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
    print(f"will send {coins} coins to {to} at address {address}")
    payload = format_send_coins(coins=coins, sender=username())
    res = asyncio.run(send_message(address=address, payload=payload))
    #print(res)
    History.save_transaction(src=res["from"], amount=res["amount"])

def receive(src: str, amount: int):
    History.save_transaction(src=src, amount=amount)
    return {
        "action": "save transaction",
        "from": os.getenv('USERNAME'),
        "amount": -amount
    }
