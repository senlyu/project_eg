from typing import List
import sys
from src.core_data_process.open_record import OpenRecord
from src.core_data_process.close_record import CloseRecord
from src.core_data_process.gain_record import GainRecord
from src.core_data_process.util import add_into_dict_as_list_item
from src.core_data_process.gain_records_bank import GainRecordsBank
from src.core_data_process.open_position_bank import OpenPositionBank
from src.core_data_process.close_position_bank import ClosePositionBank
from src.enums import TransactionActionEnum

class ProcessTransactions:
    def __init__(self):
        self.gain_records_all = GainRecordsBank()
        self.open_position_all = OpenPositionBank()
        self.extra_close_position_all = ClosePositionBank()
    
    def main(
        self,
        transactions: List,
        end_date,
    ):
        for t in transactions:
            if t.date > end_date:
                continue
            
            self.process_one_transaction(t, end_date)

        return self.gain_records_all, self.open_position_all, self.extra_close_position_all

    def process_one_transaction(self, t, end_date):
        
        if t.action == TransactionActionEnum.BTO:
            self.add_transaction_to_open_records(t)
        elif t.action == TransactionActionEnum.STC:
            if t.ticker not in self.open_position_all.get_all_tickers():
                self.add_transaction_to_extra_close_postions(t)
            else:
                # process open positions to close
                (remaining_open_postions, remaining_close_postion, gain_record) = ProcessTransactions.process_open_positioins_to_close(self.open_position_all.by_ticker[t.ticker], t)

                self.add_transaction_to_gain_records(t, gain_record)

                for open_position in self.open_position_all.by_ticker[t.ticker]:
                    self.open_position_all.remove_open_record(open_position, t.source)
                for open_position in remaining_open_postions:
                    self.open_position_all.add_open_record(open_position, t.source)
                    
                self.add_transaction_to_extra_close_postions_half_closed(t, remaining_close_postion)


    def add_transaction_to_open_records(self, t):
        self.open_position_all.add_open_record(OpenRecord(t, t.volumn), t.source)

    def add_transaction_to_extra_close_postions(self, t):
        self.extra_close_position_all.add_close_record(CloseRecord(t, t.volumn), t.source)

    def add_transaction_to_gain_records(self, t, gain_record):
        if gain_record is not None:
            self.gain_records_all.add_gain_record(gain_record, t.source)

    def add_transaction_to_extra_close_postions_half_closed(self, t, remaining_close_postion):
        if remaining_close_postion is not None:
            self.extra_close_position_all.add_close_record(remaining_close_postion, t.source)


    @staticmethod
    def process_open_positioins_to_close(open_records, close_transaction):
        open_records = sorted(open_records, key=lambda x: x.open_transaction.date)

        target_v = close_transaction.volumn
        new_gain_record = None
        remaining_open_records = []
        new_close_record = None

        closed_open = []
        remaining_i = len(open_records)
        for i, o_r in enumerate(open_records):
            v = o_r.remain_volumn
            if (target_v >= v):
                closed_open.append(o_r)
                target_v -= v
            else:
                # still open positions

                #add remaining open positions
                remaining_open = v - target_v
                remaining_open_records.append(OpenRecord(o_r.open_transaction, remaining_open))

                # add close positions
                closed_open.append(OpenRecord(o_r.open_transaction, target_v))

                target_v = 0

            if target_v <= sys.float_info.min:
                remaining_i = i + 1
                break

        remaining_open_records = remaining_open_records + open_records[remaining_i:]

        if target_v > 0:
            # still close positions
            new_close_record = CloseRecord(close_transaction, target_v)

        if len(closed_open) > 0:
            new_gain_record = GainRecord(closed_open, close_transaction)

        return remaining_open_records, new_close_record, new_gain_record


        

    
