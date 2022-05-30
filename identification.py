import uuid
import requests

import os


def username():
    stream = os.popen("echo $USER")
    return stream.read()

def get_mac_address():
    return uuid.getnode()

def get_public_ip_address():
    ip = requests.get('https://api.ipify.org').text
    return ip