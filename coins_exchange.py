import asyncio
from audioop import add
from http import client

from client import send_message
from fs.registry import get_registry, save_registry_entry
from fs.history import save_transaction

import json
import os
from client import Client
from identification import username


def format_send_coins(coins: int, sender: str) -> dict:
    return {
        "action": "send coins",
        "amount": coins,
        "from": sender
    }

def send_coins(to: str, coins: int):
    registry = get_registry()
    
    address = registry[to] if to in registry else None
    if (address == None):
        print("Could not get address for user: " + to + ". Will try to fetch it from registry")
        address = Client.fetch_address(to)
        if (address == None):
            print("Could not fetch address for user: " + to + " from registry.")
            return None
    print(f"will send {coins} coins to {to} at address {address}")
    payload = format_send_coins(coins=coins, sender=username())
    res = asyncio.run(send_message(address=address, payload=payload))
    if res == None:
        print(f"could not reach address {address}. Will try to fetch address from registry.")
        address = Client.fetch_address(to)
        res = asyncio.run(send_message(address=address, payload=payload))
        if res == None:
            print(f"could not send coins to {to}")
            return
    save_transaction(src=to, amount=-coins)
        
