from PyInquirer import prompt
from identification import username
from history import History

from coins_exchange import send
from registry import Registry

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
    Registry.dump()
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
        Registry.fetch_address(username=username)
    elif (option["registry"] == "update my address"):
        Registry.update_address()

def show_coinsend_interface():
    registry = Registry.cached_registry.keys()
    options = {
        "type": "list",
        "name": "sendcoins",
        "message": "Choose recipient",
        "choices": registry
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

    send(dst, amount)
    pass

def show_history():
    History.dump()

while True:
    show_menu(username=username(), coins=History.get_current_coin_amount())