import pandas as pd

from typing import List
from datetime import datetime
from src.enums import TransactionActionEnum, TransactionOptionTypeEnum
from src.core_data_process.transaction import Transcation
from src.logging import Logging
from src.data_loader.csv_reader import CSVReader

class EGStandardCSVReader(CSVReader):

    def load(self) -> List:
        Logging.log(f"eg_standard CSV reader start to read {self.file_path}")
        df = pd.read_csv(self.file_path)
        Logging.log(f"load from {self.file_path}: {len(df)} rows")

        total = []
        for _, row in df.iterrows():
            try:
                date = datetime.strptime(row['Date'], "%m/%d/%Y")
                symbol = row['Symbol']
                action = EGStandardCSVReader.get_action(row['Action'])
                volumn = float(row['Quantity'])
                price = float(row['Price']) 
                is_option = EGStandardCSVReader.get_is_option(row['Ticker'], row['Symbol'])
                if is_option:
                    option_date = datetime.strptime(row['Option Date'], "%m/%d/%Y")
                    option_type = EGStandardCSVReader.get_option_type(row['Option Type'])
                    strike_price = round(float(row['Strike']), 2) 
                else:
                    option_date = None
                    option_type = None
                    strike_price = None
                
            except Exception as e:
                Logging.log(e)
                Logging.log("error in process row: " + row)
                continue

            t = Transcation(date, symbol, action, volumn, price, is_option, option_date, option_type, strike_price)
            total.append(t)

        sorted_total = sorted(total, key=lambda x: x.date)
            
        return sorted_total

    @staticmethod
    def get_is_option(ticker, symbol):
        return ticker != symbol

    @staticmethod
    def get_option_type(desc):
        if desc == "Call":
            return TransactionOptionTypeEnum.CALL
        raise ValueError("Not Support This Option Type: " + desc)

    @staticmethod
    def get_action(code):
        if code == "BTO":
            return TransactionActionEnum.BTO
        if code == "STC":
            return TransactionActionEnum.STC
