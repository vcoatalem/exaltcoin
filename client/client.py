import asyncio
from audioop import add
import json
import websockets

from pprint import pprint

async def send_message(address: str, payload: dict) -> dict:
    async with websockets.connect("ws://" + address) as websocket:
        await websocket.send(json.dumps(payload))
        res = await websocket.recv()
        return json.loads(res)

def get_history(address: str) -> dict:
    return asyncio.run(send_message(address, {
        "action": "get history"
    }))

def get_registry(address: str) -> dict:
    return asyncio.run(send_message(address, {
        "action": "get registry"
    }))

def get_address(address: str) -> dict:
    return asyncio.run(send_message(address, {
        "action": "get address"
    }))

def get_user(address: str) -> dict:
    return asyncio.run(send_message(address, {
        "action": "get user"
    }))

def add_user(address: str, username: str) -> dict:
    return asyncio.run(send_message(address, {
        "action": "add user",
        "username": username 
    }))

def refresh_address(address: str) -> dict:
    return asyncio.run(send_message(address, {
        "action": "refresh address"
    }))


def get_coins(address: str) -> dict:
    return asyncio.run(send_message(address, {
        "action": "get coins"
    }))

def send_coins(address: str, to: str, amount: int) -> dict:
    return asyncio.run(send_message(address, {
        "action": "send coins",
        "to": to,
        "amount": int
    }))