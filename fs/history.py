import csv
from os import path, chmod
from datetime import datetime

history_filename = '/exaltcoin_data/history.csv'

def get_history():
    history = []
    if not path.isfile(history_filename):
        open(history_filename, 'a').close()
    with open(history_filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            history.append({"date": row[0], "coins": row[1], "from": row[2]})
    return history

def save_transaction(src: str, amount: int):
    with open(history_filename, "a") as f:
        writer = csv.writer(f)
        row = [str(datetime.now()), amount, src]
        writer.writerow(row)

def get_current_coin_amount(history : dict):
    history = get_history()
    coins = map(lambda history_entry: int(history_entry["coins"]), history)
    return sum(coins) + 10 #initial capital

def print_history(history: dict):
        print("{:<40} {:<20} {:<10}".format('Date','Amount','User'))
        for entry in history:
            print("{:<40} {:<20} {:<10}".format(entry["date"], entry["coins"], entry["from"]))
