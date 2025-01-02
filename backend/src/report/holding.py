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

    def get_total_asset_with_ticker(self, total_volume, all_prices):
        total_asset_value = 0
        all_values = []
        for ticker, volume in total_volume.items():
            is_option = any(char.isdigit() for char in ticker)
            price = all_prices[ticker] * (100.0 if is_option else 1)
            asset_value = round(volume * price, 2)
            total_asset_value += asset_value
            all_values.append((ticker, asset_value))

        return total_asset_value, all_values

    def get_total_asset_summary(self, open_position_bank, market_data):
        all_tickers = list(open_position_bank.by_ticker.keys())
        all_prices = market_data.get_previous_close(all_tickers)
        total_volume = open_position_bank.get_total_volume_with_ticker()
        return self.get_total_asset_with_ticker(total_volume, all_prices)


    def report_by_all_holding(self, open_position_bank, market_data):
        self.report("-" * 10 + " open postions for all holding" + "-" * 10)
        ( total_asset_value, all_values) = self.get_total_asset_summary(open_position_bank, market_data)

        # all values
        for (ticker, asset_value) in all_values:
            self.report(f"{ticker}: {asset_value}, percentage: {asset_value/total_asset_value*100:.2f}%")

        self.report("-" * 10 + " open postions for all holding finished" + "-" * 10)

    def report_by_group_holding(self, open_position_bank, market_data):
        self.report("-" * 10 + " open postions for groups" + "-" * 10)
        ( total_asset_value, all_values) = self.get_total_asset_summary(open_position_bank, market_data)

        self.report("-" * 10 + " open postions for groups finished" + "-" * 10)