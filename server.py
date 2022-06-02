import asyncio
import boto3
import json
import websockets
import identification
from fs.history import save_transaction

import os
from dotenv import load_dotenv


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

def update_address(username: str, ip_address: str, port: int):
    load_dotenv()
    print(f"will update our address: {username} -> {ip_address}:{port} in dynamodb")
    dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_ACCESS_SECRET_KEY"),
            region_name='eu-west-3'
        )
    table = dynamodb.Table('exaltcoin-registry')
    table.put_item(
        Item={
            'user': username,
            'address': f"{ip_address}:{port}"
        }
    )

async def serve():
    update_address(identification.username(), identification.get_public_ip_address(), 8765)
    async with websockets.serve(ws_handler=handle_socket, port=8765):
        await asyncio.Future()  # run forever

asyncio.run(serve())