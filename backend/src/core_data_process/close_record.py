from src.core_data_process.transaction import Transcation

class CloseRecord:
    def __init__(
        self,
        close_transaction: Transcation,
        remain_volumn: int,
    ):
        self.close_transaction = close_transaction
        self.remain_volumn = remain_volumn

    def __repr__(self):
        return f"CloseRecord(close_transaction={self.close_transaction}, remain_volumn={self.remain_volumn})"