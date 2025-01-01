import os
from datetime import datetime
from src.config import TEST_MODE_CONFIG, PORD_MODE_CONFIG
from src.data_loader.load import load
from src.core_data_process.process_transactions import ProcessTransactions
from src.core_data_process.gain_records_bank import GainRecordsBank
from src.core_data_process.open_position_bank import OpenPositionBank
from src.core_data_process.close_position_bank import ClosePositionBank
from src.logging import Logging
from src.market_data.polygon_apis.previous_close import PolygonAPIClosePrice
from src.market_data.local_storage import LocalStorage
from src.market_data.market_data import MarketDataWithPolygon
import json
import asyncio
from src.report.tax import TaxReport
from src.report.holding import HoldingReporting

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

    (tax_report, holding_report) = init_reports_from_config()
    tax_report.report_by_quarter_summary(gain_records_bank)
    tax_report.report_by_year_summary(gain_records_bank)

    holding_report.report_by_all_holding(open_position_bank, init_market_data_with_polygon_from_config())

            
def init_market_data_with_polygon_from_config():
    with open('config.json', 'r') as f:
        config = json.load(f)

    polygon = config.get('polygon')

    local_storage = config.get('local_storage')
    storage_path = local_storage.get('path')
    storage = LocalStorage(storage_path)

    return MarketDataWithPolygon(storage, polygon)

def init_reports_from_config():
    with open('config.json', 'r') as f:
        config = json.load(f)

    base_path = config.get('report_path')

    return (TaxReport(base_path), HoldingReporting(base_path))


if __name__ == "__main__":
    Logging.clean()
    Logging.start()
    mode = os.getenv("MODE")
    main(test_mode=(mode == "test"))