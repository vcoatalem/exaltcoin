import uuid
import requests

import dotenv
import os

dotenv.load_dotenv()

def username():
    return os.getenv("USERNAME")

def get_mac_address():
    return uuid.getnode()

def get_public_ip_address():
    ip = requests.get('https://api.ipify.org').text
    return ip