import os
from datetime import datetime
from src.config import TEST_MODE_CONFIG, PORD_MODE_CONFIG
from src.data_loader.load import load
from src.core_data_process.process_transactions import ProcessTransactions
from src.core_data_process.gain_records_bank import GainRecordsBank
from src.core_data_process.open_position_bank import OpenPositionBank
from src.core_data_process.close_position_bank import ClosePositionBank
from src.logging import Logging
from src.market_data.polygon_api import PolygonAPI
from src.market_data.local_storage import LocalStorage
from src.market_data.market_data import MarketData
import json

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
            
def init_market_data_from_config():
    with open('config.json', 'r') as f:
        config = json.load(f)

    polygon = config.get('polygon')
    polygon_api_keys = polygon.get('api_keys')
    query = PolygonAPI(polygon_api_keys)

    local_storage = config.get('local_storage')
    storage_path = local_storage.get('path')
    storage = LocalStorage(storage_path)

    return MarketData(storage, query)


if __name__ == "__main__":
    Logging.clean()
    Logging.start()
    mode = os.getenv("MODE")
    # main(test_mode=(mode == "test"))
    market_data = init_market_data_from_config()
    print(float(market_data.get_previous_close("AAPL")))