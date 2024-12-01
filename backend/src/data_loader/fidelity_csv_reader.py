from typing import List
from datetime import datetime

import pandas as pd

from src.enums import TransactionActionEnum, TransactionOptionTypeEnum, SourceEnum
from src.core_data_process.transaction import Transcation
from src.logging import Logging
from src.data_loader.csv_reader import CSVReader

class FidelityCSVReader(CSVReader):

    def load(self, source = SourceEnum.FIDELITY) -> List:
        Logging.log(f"fidelity CSV reader start to read {self.file_path}")
        df = pd.read_csv(self.file_path, header=2).dropna(how="all") # remove first 2 empty rows
        Logging.log(f"load from {self.file_path}: {len(df)} rows")

        total = []
        for _, row in df.iterrows():
            try:
                date = datetime.strptime(row['Run Date'], "%m/%d/%Y")
                symbol = row['Symbol']
                if not FidelityCSVReader.get_is_stock_option(symbol):
                    continue
                action = FidelityCSVReader.get_action(row['Action'])
                volumn = float(abs(row['Quantity']))
                price = float(row['Price ($)'])

                is_option = FidelityCSVReader.get_is_option(symbol)

                (option_date, option_type, strike_price) = (None, None, None)
                
            except Exception as e:
                Logging.log(e)
                Logging.log("error in process row: ", row)
                continue

            t = Transcation(source, date, symbol, action, volumn, price, is_option, option_date, option_type, strike_price)
            total.append(t)

        sorted_total = sorted(total)
            
        return sorted_total

    @staticmethod
    def get_is_stock_option(symbol):
        return not symbol[0].isdigit()

    @staticmethod
    def get_action(desc):
        desc = desc.lstrip()
        code = desc.split(' ')[1]
        if code == "BOUGHT":
            return TransactionActionEnum.BTO
        if code == "SOLD":
            return TransactionActionEnum.STC

    @staticmethod
    def get_is_option(desc):
        return False
