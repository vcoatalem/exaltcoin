from operator import add, delitem
from typing import Dict
import boto3
import csv
import identification
import os
from os import path, chmod

from boto3.dynamodb.conditions import Key


registry_filename = '/exaltcoin_data/registry.csv'
def get_registry():
    registry = {}
    with open(registry_filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            registry[row[0]] = row[1]
    return registry

def save_registry_entry(username: str, address: str):
    with open(registry_filename, 'a') as f:
        reader = csv.writer(f)
        reader.writerow([username, address])

def print_registry(registry: dict):
    print("{:<10} {:<20}".format('User','Address'))
    for entry in registry:
        print("{:<10} {:<20}".format(entry, registry[entry]))

class registry:
    def update_address(self):
        username = identification.username()
        ip_address = identification.get_public_ip_address()
        port = 8765

        print(f"will update our address: {username} -> {ip_address}:{port}")

        print(self.table.put_item(
            Item={
                'user': username,
                'address': f"{ip_address}:{port}"
            }
        ))