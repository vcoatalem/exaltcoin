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

    def dump(self):
        print("{:<40} {:<20} {:<10}".format('Date','Amount','User'))
        for entry in self.history:
            print("{:<40} {:<20} {:<10}".format(entry["date"], entry["coins"], entry["from"]))


History = history()
History.load()