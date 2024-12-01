from src.core_data_process.transaction import Transcation

class OpenRecord:
    def __init__(
        self,
        open_transaction: Transcation,
        remain_volumn: int,
    ):
        self.open_transaction = open_transaction
        self.remain_volumn = remain_volumn

    def __repr__(self):
        return f"OpenRecord(open_transaction={self.open_transaction}, remain_volumn={self.remain_volumn})"