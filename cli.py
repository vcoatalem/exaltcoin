from PyInquirer import prompt
from identification import username


from coins_exchange import send

def show_menu(username: str, coins: int):
    options = {
        "type": "list",
        "name": "main_options",
        "message": f"Exalt Coin interface. {username} - {coins} Coins on your account",
        "choices": ["Friend List","Send Coins","History"]
    }
    option = prompt(options)
    if (option['main_options']) == "Friend List":
        show_friendlist()
    if (option['main_options']) == "Send Coins":
        show_sendcoin_menu()
    if (option['main_options']) == "History":
        show_history()


def show_friendlist():
    

    pass

def show_sendcoin_menu():
    send("test", 10)
    pass

def show_history():
    pass

while True:
    show_menu(username=username(), coins=10)