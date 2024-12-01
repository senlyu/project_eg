from src.transaction import Transcation

class CloseRecord:
    def __init__(
        self,
        close_transaction: Transcation,
        remain_volumn: int,
    ):
        self.close_transaction = close_transaction
        self.remain_volumn = remain_volumn