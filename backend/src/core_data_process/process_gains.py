
from typing import List
from src.core_data_process.util import add_into_dict_as_list_item
from src.core_data_process.gain_records_bank import GainRecordsBank

class ProcessGains:
    
    def __init__(self):
        self.yearly_estimated_gain_all = {}
        self.quarterly_estimated_gain_all = {}

    def main(
        self, gain_records_bank: GainRecordsBank,
    ):
        for g in gain_records_bank.get_gain_records_all():
            self.add_gain_record_to_yearly_gain(g)
            self.add_gain_record_to_quarterly_gain(g)

        return self.yearly_estimated_gain_all, self.quarterly_estimated_gain_all

    def add_gain_record_to_yearly_gain(self, gain_record):
        y = gain_record.tax_year
        self.yearly_estimated_gain_all = add_into_dict_as_list_item(self.yearly_estimated_gain_all, y, gain_record)

    def add_gain_record_to_quarterly_gain(self, gain_record):
        q = gain_record.tax_quarter
        self.quarterly_estimated_gain_all = add_into_dict_as_list_item(self.quarterly_estimated_gain_all, q, gain_record)

