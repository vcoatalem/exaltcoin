import asyncio

from client import send_message
from registry import Registry
from history import History

from dotenv import load_dotenv
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
    payload = format_send_coins(coins=coins, sender=username())
    res = asyncio.run(send_message(address=address, payload=payload))
    print(res)

def receive(src: str, amount: int):
    History.save_transaction(src=src, amount=amount)
    return {
        "action": "save transaction",
        "from": os.getenv('USERNAME'),
        "amount": -amount
    }
