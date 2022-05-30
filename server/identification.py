import uuid
import requests

import dotenv
import os

def username():
    dotenv.load_dotenv()
    return os.getenv("EXALTCOIN_USERNAME")
    """
    stream = os.popen("echo $USER")
    return stream.read().strip()
    """

def get_username():
    return lambda: {
        "action": "get username",
        "username": os.getenv("EXALTCOIN_USERNAME")
    }

def address():
    dotenv.load_dotenv()
    return os.getenv("EXALTCOIN_ADDRESS")
    """
    ip = requests.get('https://api.ipify.org').text
    return ip
    """

def get_address():
        return lambda: {
        "action": "get address",
        "username": os.getenv("EXALTCOIN_ADDRESS")
    }