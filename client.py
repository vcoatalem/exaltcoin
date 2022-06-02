import json
import websockets
import boto3
from boto3.dynamodb.conditions import Key
from pprint import pprint
import identification
import os
from dotenv import load_dotenv

async def send_message(address: str, payload: dict) -> dict:
    try:
        async with websockets.connect("ws://" + address) as websocket:
            await websocket.send(json.dumps(payload))
            res = await websocket.recv()
            return json.loads(res)
    except:
        print(f"could not reach websocket server at address: {address}")
        return None


class client:

    def __init__(self) -> None:
        load_dotenv()
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_ACCESS_SECRET_KEY"),
            region_name='eu-west-3'
        )
        self.table = self.dynamodb.Table('exaltcoin-registry')
        #self.update_address()
        #self.server = Process(target=server.serve)
        #self.server.start()
    
    #def __del__(self):
    #    self.server.join()




    def fetch_address(self, username: str):
        query = self.table.query(KeyConditionExpression=(Key('user').eq(username)))
        #print("queried: ", query)
        if (query):
            items = query['Items']
            if len(items) == 0:
                print(f"Could not find address for user: {username}")
                return
            user = items[0]
            print("user:", user)
            return user["address"]
        return None


Client = client()