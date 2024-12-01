from typing import List
from src.transaction import Transcation

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


    @staticmethod
    def cal_gain(processing_gains, close_transaction):
        revenue = close_transaction.price * close_transaction.volumn

        cost = 0
        for r in processing_gains:
            price = r.open_transaction.price
            volumn = r.remain_volumn
            cost += price * volumn
        
        return revenue - cost
