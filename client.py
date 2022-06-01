import asyncio
import json
import websockets
import boto3
from boto3.dynamodb.conditions import Key
from pprint import pprint
import identification
from multiprocessing import Process

async def send_message(address: str, payload: dict) -> dict:
    async with websockets.connect("ws://" + address) as websocket:
        await websocket.send(json.dumps(payload))
        res = await websocket.recv()
        return json.loads(res)


class client:

    def __init__(self) -> None:
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIAURLO2GZL5SGLVDUE',
            aws_secret_access_key='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',
            region_name='eu-west-3'
        )
        self.table = self.dynamodb.Table('exaltcoin-registry')
        self.update_address()
        #self.server = Process(target=server.serve)
        #self.server.start()
    
    #def __del__(self):
    #    self.server.join()


    def update_address(self):
        username = identification.username()
        ip_address = identification.get_public_ip_address()
        port = 8765

        print(f"will update our address: {username} -> {ip_address}:{port} in dynamodb")

        print(self.table.put_item(
            Item={
                'user': username,
                'address': f"{ip_address}:{port}"
            }
        ))

    def fetch_address(self, username: str):
        query = self.table.query(KeyConditionExpression=(Key('user').eq(username)))
        print("queried: ", query)
        if (query):
            items = query['Items']
            user = items[0]
            print("user:", user)
            return user["address"]
        return None


Client = client()