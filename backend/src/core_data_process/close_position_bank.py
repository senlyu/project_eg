from src.logging import Logging

class ClosePositionBank:

    def __init__(self):
        self.all = []
        self.by_source = {}
        self.by_ticker = {}

    def add_close_record(self, close_record, source):
        if close_record is None:
            return

        self.all.append(close_record)
        self.by_source[source] = self.by_source.get(source, []) + [close_record]
        self.by_ticker[close_record.close_transaction.ticker] = self.by_ticker.get(close_record.close_transaction.ticker, []) + [close_record]
        

    def get_all_tickers(self):
        return self.by_ticker.keys()

    def remove_close_record(self, close_record, source):
        self.all.remove(close_record)
        self.by_source[source].remove(close_record)
        if self.by_source[source] == []:
            del self.by_source[source]
        self.by_ticker[close_record.close_transaction.ticker].remove(close_record)
        if self.by_ticker[close_record.close_transaction.ticker] == []:
            del self.by_ticker[close_record.close_transaction.ticker]


    def __str__(self):
        return f"ClosePositionBank(all={[x.__str__() for x in self.all]})"

    def logging(self):
        Logging.log("-" * 10 + " close position bank" + "-" * 10)
        for record in self.all():
            Logging.log(record)
        Logging.log("-" * 10 + " close position bank finished" + "-" * 10)

    def merge(self, other):
        self.all = self.all + other.all
        for source in other.by_source:
            self.by_source[source] = self.by_source.get(source, []) + other.by_source[source]
        for ticker in other.by_ticker:
            self.by_ticker[ticker] = self.by_ticker.get(ticker, []) + other.by_ticker[ticker]
        