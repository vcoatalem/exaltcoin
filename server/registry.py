from operator import delitem
from typing import Dict
import boto3
import csv
import identification
import os
from os import path

from boto3.dynamodb.conditions import Key


class registry:

    def __init__(self) -> None:
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIAURLO2GZL5SGLVDUE',
            aws_secret_access_key='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',
            region_name='eu-west-3'
        )
        self.table = self.dynamodb.Table('exaltcoin-registry')
        self.registry_filename = "/exaltcoin_data/registry.csv"
        self.cached_registry: Dict = {}

    def load_cached_registry(self):
        filename = f"{self.registry_filename}"
        if not path.isfile(filename):
            open(filename, 'a').close()
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                self.cached_registry[row[0]] = row[1]

    def save_cached_registry(self):
        filename = f"{self.registry_filename}"
        if not path.isfile(filename):
            open(filename, "a").close()
        with open(filename, "w") as f:
            reader = csv.writer(f)
            for entry in self.cached_registry:
                reader.writerow([entry[0], entry[1]])

    def get_address(self, username: str):
        return self.cached_registry[username] if username in self.cached_registry else None

    def fetch_address(self, username: str):
        query = self.table.query(KeyConditionExpression=(Key('user').eq(username)))
        items = query['Items']
        if len(items) == 0:
            print(f"could not fetch address for user: {username}")
            return None
        user = items[0]
        self.cached_registry[user["user"]] = user["address"]
        return user["address"]

    def update_address(self):
        username = identification.username()
        ip_address = identification.address()
        port = 8765

        print(f"will update our address: {username} -> {ip_address}:{port}")

        print(self.table.put_item(
            Item={
                'user': username,
                'address': f"{ip_address}:{port}"
            }
        ))

    def to_string(self):
        s = "{:<10} {:<20}".format('User','Address')
        for entry in self.cached_registry:
            s += "{:<10} {:<20}".format(entry, self.cached_registry[entry])
        return s

    def get(self):
        return {
            "action": "get registry",
            "registry": self.to_string()
        }


Registry = registry()
Registry.load_cached_registry()
print(Registry.cached_registry)