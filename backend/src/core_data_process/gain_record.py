from typing import List
from src.core_data_process.transaction import Transcation

class GainRecord:
    def __init__(
        self,
        processing_gains: List,
        close_transaction: Transcation,
    ):
        self.processing_gains = processing_gains
        self.close_transaction = close_transaction

        self.symbol = close_transaction.symbol
        self.volumn = close_transaction.volumn
        self.price = close_transaction.price
        self.gain = GainRecord.cal_gain(processing_gains, close_transaction)
        self.tax_year = GainRecord.get_tax_year(close_transaction)
        self.tax_quarter = GainRecord.get_tax_quarter(close_transaction)
        self.short_gain, self.long_gain = GainRecord.cal_gain_by_type(processing_gains, close_transaction)

    @staticmethod
    def cal_gain(processing_gains, close_transaction):
        revenue = close_transaction.price * close_transaction.volumn

        cost = 0
        for r in processing_gains:
            price = r.open_transaction.price
            volumn = r.remain_volumn
            cost += price * volumn
        
        return (revenue - cost) * ( 100 if close_transaction.is_option else 1 )

    @staticmethod
    def cal_gain_by_type(processing_gains, close_transaction):

        short, long = 0, 0
        for r in processing_gains:
            open_price = r.open_transaction.price
            close_price = close_transaction.price
            volumn = r.remain_volumn
            revenue = round(close_price - open_price, 2) * volumn

            open_date = r.open_transaction.date
            close_data = close_transaction.date
            days = abs((close_data - open_date).days)
            if (days > 365):
                # long
                long += revenue
            else:
                # short
                short += revenue

        return short * ( 100 if close_transaction.is_option else 1 ), long * ( 100 if close_transaction.is_option else 1 )

    @staticmethod
    def get_tax_year(close_transaction):
        return close_transaction.date.year

    @staticmethod
    def get_tax_quarter(close_transaction):
        year = close_transaction.date.year
        quarter = (close_transaction.date.month - 1) // 3 + 1
        return str(year) + "Q" + str(quarter)

    def __repr__(self):
        return f"GainRecord(processing_gains={self.processing_gains}, close_transaction={self.close_transaction}), gain={self.gain}, short={self.short_gain}, long={self.long_gain}, tax_year={self.tax_year}, tax_quarter={self.tax_quarter}"
