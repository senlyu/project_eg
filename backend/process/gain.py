from .transaction import Transcation
from .open_record import OpenRecord
from .enums import TransactionActionEnum

class ProcessGain:
    @staticmethod
    def main(
        transactions: List,
        end_date,
    ):
        all_gain_records = []

        open_position_all = {}
        for t in transactions:
            if t.date > end_date:
                break

            if t.action == TransactionActionEnum.BTO:
                if open_position_all[t.symbol] == None:
                    open_position_all[t.symbol] = [ OpenRecord(t, t.volumn) ]
                else:
                    open_position_all[t.symbol].append(OpenRecord(t, t.volumn))
            elif t.action == TransactionActionEnum.STC:


        return all_gain_records

    
