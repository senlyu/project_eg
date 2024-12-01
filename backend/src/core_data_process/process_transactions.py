from typing import List
import sys
from src.core_data_process.open_record import OpenRecord
from src.core_data_process.close_record import CloseRecord
from src.core_data_process.gain_record import GainRecord
from src.enums import TransactionActionEnum

class ProcessTransactions:
    @staticmethod
    def main(
        transactions: List,
        end_date,
    ):
        gain_records_all = {}

        open_position_all = {}

        remaining_position_all = {}
        for t in transactions:
            if t.date > end_date:
                break

            if t.action == TransactionActionEnum.BTO:
                open_position_all = ProcessTransactions.add_into_dict_as_list_item(open_position_all, t.ticker, OpenRecord(t, t.volumn))
            elif t.action == TransactionActionEnum.STC:
                if t.ticker not in open_position_all:
                    remaining_position_all = ProcessTransactions.add_into_dict_as_list_item(remaining_position_all, t.ticker, CloseRecord(t, t.volumn))
                else:
                    # process open positions to close
                    (remaining_open_postions, remaining_close_postion, gain_record) = ProcessTransactions.process_open_positioins_to_close(open_position_all[t.ticker], t)

                    if gain_record is not None:
                        gain_records_all = ProcessTransactions.add_into_dict_as_list_item(gain_records_all, t.ticker, gain_record)
                    open_position_all[t.ticker] = remaining_open_postions
                    if remaining_close_postion is not None:
                        remaining_position_all = ProcessTransactions.add_into_dict_as_list_item(remaining_position_all, t.ticker, remaining_close_postion)

        return gain_records_all, open_position_all, remaining_position_all

    @staticmethod
    def add_into_dict_as_list_item(d, key, item):
        if key in d:
            if isinstance(item, list):
                d[key] = d[key] + item
            else:
                d[key].append(item)
        else:
            if isinstance(item, list):
                d[key] = item
            else:
                d[key] = [ item ]

        return d

    @staticmethod
    def process_open_positioins_to_close(open_records, close_transaction):

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


        

    
