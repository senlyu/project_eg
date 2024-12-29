from src.logging import Logging

class GainRecordsBank:
    def __init__(self):
        self.all = []
        self.by_source = {}
        self.by_year = {}
        self.by_quarter = {}
        self.by_ticker = {}

    def merge(self, other):
        self.all = self.all + other.all
        for source in other.by_source:
            self.by_source[source] = self.by_source.get(source, []) + other.by_source[source]
        for year in other.by_year:
            self.by_year[year] = self.by_year.get(year, []) + other.by_year[year]
        for quarter in other.by_quarter:
            self.by_quarter[quarter] = self.by_quarter.get(quarter, []) + other.by_quarter[quarter]
        for ticker in other.by_ticker:
            self.by_ticker[ticker] = self.by_ticker.get(ticker, []) + other.by_ticker[ticker]

    def add_gain_record(self, gain_record, source):
        if gain_record is None:
            return

        self.all.append(gain_record)
        self.by_source[source] = self.by_source.get(source, []) + [gain_record]
        self.by_year[gain_record.tax_year] = self.by_year.get(gain_record.tax_year, []) + [gain_record]
        self.by_quarter[gain_record.tax_quarter] = self.by_quarter.get(gain_record.tax_quarter, []) + [gain_record]
        self.by_ticker[gain_record.close_transaction.ticker] = self.by_ticker.get(gain_record.close_transaction.ticker, []) + [gain_record]

    def __repr__(self):
        return f"GainRecordsBank(all={self.all})"

    def logging(self):
        Logging.log("-" * 10 + " gain records bank" + "-" * 10)
        for gain_record in self.all:
            Logging.log(gain_record)
        Logging.log("-" * 10 + " gain records bank finished" + "-" * 10)

    def report_by_quarter_summary(self):
        Logging.report("-" * 10 + " gain records bank by quarter summary" + "-" * 10)
        for quarter, gain_records in sorted(self.by_quarter.items()):
            short, long = 0, 0
            for g in gain_records:
                short += g.short_gain
                long += g.long_gain
            Logging.report(quarter, ", short: ", round(short, 2), ", long: ", round(long, 2))
        Logging.report("-" * 10 + " gain records bank by quarter summary finished" + "-" * 10)

    def report_by_year_summary(self):
        Logging.report("-" * 10 + " gain records bank by yearly summary" + "-" * 10)
        for quarter, gain_records in sorted(self.by_year.items()):
            short, long = 0, 0
            for g in gain_records:
                short += g.short_gain
                long += g.long_gain
            Logging.report(quarter, ", short: ", round(short, 2), ", long: ", round(long, 2))
            Logging.report(quarter, ", short tax 0.37: ", round(short * 0.37, 2) , ", long tax 0.2: ", round(long * 0.2, 2))
        Logging.report("-" * 10 + " gain records bank by yearly summary finished" + "-" * 10)

        