import os
from datetime import datetime
from src.report.base import ReportingBase
import asyncio


class HoldingReporting(ReportingBase):

    def __init__(self, base_path):
        self.file_path = os.path.join(base_path, "holding")
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path, exist_ok=True)

        time = datetime.now().strftime("%Y-%m-%d")
        super().__init__(self.file_path, "holding_"+time)
    
    def get_market_data_api(self):
        return init_market_data_with_polygon_from_config()

    def report_by_all_holding(self, open_position_bank, market_data):
        self.report("-" * 10 + " open postions for all holding" + "-" * 10)
        all_tickers = open_position_bank.by_ticker.keys()

        reform = []
        for t in all_tickers:
            if any(char.isdigit() for char in t):
                reform.append("O:"+t)
            else:
                reform.append(t)
        
        all_prices = market_data.get_previous_close(reform)

        total_volume = {}
        for key, value in open_position_bank.by_ticker.items():
            all_opens_for_one_ticker = value
            total_volume[key] = 0
            for op in all_opens_for_one_ticker:
                total_volume[key] += op.remain_volumn

        for ticker, volume in total_volume.items():
            is_option = any(char.isdigit() for char in ticker)
            price = all_prices[ticker] * (100.0 if is_option else 1)
            print(price, volume, ticker, volume * price)
            self.report(ticker, volume * price)

        
        self.report("-" * 10 + " open postions for all holding finished" + "-" * 10)