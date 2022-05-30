from http import server
from PyInquirer import prompt
import json
import asyncio


from client import get_history, get_registry, get_user, add_user, refresh_address, get_coins, send_coins

import sys


server_address = "127.0.0.1:8765" #sys.argv[1]


def show_menu(username: str, coins: int):
    options = {
        "type": "list",
        "name": "main_options",
        "message": f"Exalt Coin interface. {username} : {coins} Coins on your account",
        "choices": ["Friend List","Send Coins","History"]
    }
    option = prompt(options)
    if (option['main_options']) == "Friend List":
        show_registry()
    if (option['main_options']) == "Send Coins":
        show_coinsend_interface()
    if (option['main_options']) == "History":
        show_history()


def show_registry():
    registry = get_registry(server_address)
    print(registry)
    options = {
        "type": "list",
        "name": "registry",
        "message": "Choose action",
        "choices": [
            "add entry",
            "update my address",
            "return to menu"
        ]
    }
    option = prompt(options)
    if (option["registry"] == "add entry"):
        options = {
            "type": "input",
            "name": "username",
            "message": "enter username"
        }
        option = prompt(options)
        username = option["username"]
        add_user(server_address, username)
        #Registry.fetch_address(username=username)
    elif (option["registry"] == "update my address"):
        refresh_address(server_address)

def show_coinsend_interface():
    registry = get_registry()["registry"]
    registry_json = json.loads(registry)
    print(registry_json)
    options = {
        "type": "list",
        "name": "sendcoins",
        "message": "Choose recipient",
        "choices": registry_json.keys()
    }
    option = prompt(options)
    dst = option["sendcoins"]

    options = {
        "type": "input",
        "name": "sendcoins_amount",
        "message": "enter amount to be sent"
    }
    option = prompt(options)
    amount = option["sendcoins_amount"]
    send_coins(server_address, dst, amount)
    pass

def show_history():
    history = get_history()["history"]
    print(history)



while True:
    username = get_user(server_address)
    print(username)
    coins = asyncio.run(get_coins(server_address))
    print(coins)
    show_menu(username=username["username"], coins=coins["coins"])

