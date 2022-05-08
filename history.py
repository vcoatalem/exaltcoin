import csv
import os
from datetime import datetime

class history():

    def __init__(self) -> None:
        self.history = []
        self.history_filename = os.getenv('DATA_FOLDER') + '/history.csv'

    def load(self):
        with open(self.history_filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                self.history.append({"date": row[0], "coins": row[1], "from": row[2]})

    def save_transaction(self, src: str, amount: int):
        with open(self.history_filename, "a") as f:
            writer = csv.writer(f)
            row = [datetime.now(), amount, src]
            writer.writerow(row)
            self.history.append({"date": row[0], "coins": row[1], "from": row[2]})


History = history()
History.load()