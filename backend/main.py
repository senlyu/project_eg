import os
from datetime import datetime
from src.config import TEST_MODE_CONFIG, PORD_MODE_CONFIG
from src.data_loader.load import load
from src.core_data_process.process_transactions import ProcessTransactions
from src.core_data_process.gain_records_bank import GainRecordsBank
from src.core_data_process.open_position_bank import OpenPositionBank
from src.core_data_process.close_position_bank import ClosePositionBank
from src.logging import Logging

def main(
    test_mode: bool,
) -> None:
    if (test_mode):
        config = TEST_MODE_CONFIG
    else:
        config = PORD_MODE_CONFIG

    transactions = load(config)

    gain_records_bank = GainRecordsBank()
    open_position_bank = OpenPositionBank()
    remaining_position_bank = ClosePositionBank()
    for key, value in transactions.items():
        ( gain_records, open_position, remaining_position ) = ProcessTransactions().main(value, datetime.now())
        gain_records_bank.merge(gain_records)
        open_position_bank.merge(open_position)
        remaining_position_bank.merge(remaining_position)

    Logging.log(gain_records_bank)
    Logging.log(open_position_bank)
    Logging.log(remaining_position_bank)

    yearly_estimated_gain_all = gain_records_bank.by_year
    quarterly_estimated_gain_all = gain_records_bank.by_quarter
    Logging.log(yearly_estimated_gain_all)
    Logging.log(quarterly_estimated_gain_all)

    gain_records_bank.report_by_quarter_summary()
    gain_records_bank.report_by_year_summary()
            
if __name__ == "__main__":
    Logging.clean()
    Logging.start()
    mode = os.getenv("MODE")
    main(test_mode=(mode == "test"))