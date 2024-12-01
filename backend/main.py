import os
from datetime import datetime
from src.config import TEST_MODE_CONFIG, PORD_MODE_CONFIG
from src.data_loader.load import load
from src.core_data_process.process_transactions import ProcessTransactions
from src.logging import Logging

def main(
    test_mode: bool,
) -> None:
    if (test_mode):
        config = TEST_MODE_CONFIG
    else:
        config = PORD_MODE_CONFIG

    transactions = load(config)

    gain_records_all = {}
    open_position_all = {}
    remaining_position_all = {}
    for key, value in transactions.items():
        ( gain_records, open_position, remaining_position ) = ProcessTransactions.main(value, datetime.now())
        gain_records_all[key] = gain_records
        open_position_all[key] = open_position
        remaining_position_all[key] = remaining_position

    Logging.logging_gain_records(gain_records_all)
    Logging.logging_open_records(open_position_all)
    Logging.logging_close_records(remaining_position_all)

            
if __name__ == "__main__":
    Logging.clean()
    Logging.start()
    mode = os.getenv("MODE")
    main(test_mode=(mode == "test"))