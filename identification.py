import uuid
import requests

import os


def username():
    return os.getenv("EXALTCOIN_USERNAME")
    #stream = os.popen("echo $USER")
    #return stream.read().strip()

def get_mac_address():
    return uuid.getnode()

def get_public_ip_address():
    ip = os.getenv("EXALTCOIN_ADDRESS")
    #requests.get('https://api.ipify.org').text
    return ip