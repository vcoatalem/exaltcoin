import csv
from os import path
from datetime import datetime

class history():

    def __init__(self) -> None:
        self.history = []
        self.history_filename = '/exaltcoin_data/history.csv'

    def load(self):
        if not path.isfile(self.history_filename):
            open(self.history_filename, 'a').close()
        with open(self.history_filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                self.history.append({"date": row[0], "coins": row[1], "from": row[2]})

    def save_transaction(self, src: str, amount: int):
        with open(self.history_filename, "a") as f:
            writer = csv.writer(f)
            row = [str(datetime.now()), amount, src]
            writer.writerow(row)
            #self.history.append({"date": row[0], "coins": row[1], "from": row[2]})

    def get_current_coin_amount(self):
        coins = map(lambda history_entry: int(history_entry["coins"]), self.history)
        return sum(coins)

    def to_string(self):
        s = "{:<40} {:<20} {:<10}".format('Date','Amount','User')
        for entry in self.history:
            s += "{:<40} {:<20} {:<10}".format(entry["date"], entry["coins"], entry["from"])
        return s
        
    def get(self):
        return lambda: {
            "action": "get history",
            "registry": self.to_string()
        }

    def get_coins(self):
        return lambda: {
            "action": "get coins",
            "coins": self.get_current_coins_amount()
        }

History = history()
History.load()