import os
import json


class LocalStorage:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        self.data = {}
        self.load()

    def load(self):
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w+', encoding="utf-8") as f:
                f.write(f'')
                f.close()
            lines = []
        else:
            with open(self.storage_path, 'r', encoding="utf-8") as f:
                lines = [(date, ticker, price) for date, ticker, price in [line.rstrip().split('|') for line in f.readlines()]]
                f.close()

        self.build_data(lines)

    def build_data(self, lines):
        for item in lines:
            date = item[0]
            ticker = item[1]
            price = item[2]

            if date not in self.data:
                self.data[date] = {}
            self.data[date][ticker] = price

    def get_price(self, date, ticker):
        if date in self.data and ticker in self.data[date]:
            return self.data[date][ticker]
        return None

    def add_price(self, date, ticker, price):
        if date not in self.data:
            self.data[date] = {}
        self.data[date][ticker] = price
        self.save(date, ticker, price)

    def save(self, date, ticker, price):
        with open(self.storage_path, 'a', encoding="utf-8") as f:
            f.write(f"{date}|{ticker}|{price}\n")
            f.close()
