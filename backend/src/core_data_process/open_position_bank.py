from src.logging import Logging

class OpenPositionBank:

    def __init__(self):
        self.all = []
        self.by_source = {}
        self.by_ticker = {}

    def add_open_record(self, open_record, source):
        if open_record is None:
            return
        
        self.all.append(open_record)
        self.by_source[source] = self.by_source.get(source, []) + [open_record]
        self.by_ticker[open_record.open_transaction.ticker] = self.by_ticker.get(open_record.open_transaction.ticker, []) + [open_record]

    def get_all_tickers(self):
        return self.by_ticker.keys()

    def get_all_tickers_by_source(self, source):
        tickers = set()
        for o in self.by_source[source]:
            tickers.add(o.open_transaction.ticker)
        return tickers

    def remove_open_record(self, open_record, source):
        self.all.remove(open_record)
        self.by_source[source].remove(open_record)
        if self.by_source[source] == []:
            del self.by_source[source]
        self.by_ticker[open_record.open_transaction.ticker].remove(open_record)
        if self.by_ticker[open_record.open_transaction.ticker] == []:
            del self.by_ticker[open_record.open_transaction.ticker]

    def __repr__(self):
        return f"OpenPositionBank({self.all})"

    def logging(self):
        Logging.log("-" * 10 + " open position bank" + "-" * 10)
        for record in self.all():
            Logging.log(record)
        Logging.log("-" * 10 + " open position bank finished" + "-" * 10)

    def merge(self, other):
        self.all = self.all + other.all
        for source in other.by_source:
            self.by_source[source] = self.by_source.get(source, []) + other.by_source[source]
        for ticker in other.by_ticker:
            self.by_ticker[ticker] = self.by_ticker.get(ticker, []) + other.by_ticker[ticker]

    def get_total_volume_with_ticker(self):
        total_volume = {}
        for key, value in self.by_ticker.items():
            all_opens_for_one_ticker = value
            total_volume[key] = 0
            for op in all_opens_for_one_ticker:
                total_volume[key] += op.remain_volumn
        return total_volume
        