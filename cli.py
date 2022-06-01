from PyInquirer import prompt
from identification import username


from coins_exchange import send_coins

from fs.history import get_current_coin_amount, get_history, print_history
from fs.registry import get_registry, print_registry, save_registry_entry

import client

from client import Client


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
        show_coinsend_interface(coins)
    if (option['main_options']) == "History":
        show_history()


def show_registry():
    registry = get_registry()
    print_registry(registry)
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
        address = Client.fetch_address(username=username)
        save_registry_entry(username, address)
        
    elif (option["registry"] == "update my address"):
        Client.update_address()

def show_coinsend_interface(coins: int):
    registry = get_registry()
    recipients = registry.keys()
    options = {
        "type": "list",
        "name": "sendcoins",
        "message": "Choose recipient",
        "choices": recipients
    }
    option = prompt(options)
    dst = option["sendcoins"]

    options = {
        "type": "input",
        "name": "sendcoins_amount",
        "message": "enter amount to be sent"
    }
    option = prompt(options)
    amount = int(option["sendcoins_amount"])
    if amount < 0:
        print("Cant send negative money!")
    if amount > coins:
        print("You do not have that many coins!")
        return
    send_coins(dst, amount)

def show_history():
    history = get_history()
    print_history(history)

while True:
    history = get_history()
    show_menu(username=username(), coins=get_current_coin_amount(history=history))