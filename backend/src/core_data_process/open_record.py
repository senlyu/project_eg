from src.transaction import Transcation

class OpenRecord:
    def __init__(
        self,
        open_transaction: Transcation,
        remain_volumn: int,
    ):
        self.open_transaction = open_transaction
        self.remain_volumn = remain_volumn