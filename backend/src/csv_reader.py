import pandas as pd

from typing import List
from datetime import datetime
from src.enums import TransactionActionEnum, TransactionAssetsEnum, TransactionOptionTypeEnum
from src.transaction import Transcation
from src.logging import Logging

class CSVReader:
    def __init__(
        self,
        file_path: str,
    ) -> None:
        Logging.log("cvs reader get path: " + file_path)
        self.file_path = file_path


class RobinhoodCSVReader(CSVReader):

    def load(self) -> List:
        Logging.log(f"robinhood CSV reader start to read {self.file_path}")
        df = pd.read_csv(self.file_path)
        filtered = df.loc[df["Trans Code"].isin(["BTO","STC","Buy","Sell"])]
        Logging.log(f"load from {self.file_path}: {len(filtered)} rows")

        total = []
        for index, row in filtered.iterrows():
            try:
                date = datetime.strptime(row['Activity Date'], "%m/%d/%Y")
                symbol = row['Instrument']
                action = RobinhoodCSVReader.get_action(row['Trans Code'])
                volumn = float(row['Quantity'])
                price = float(row['Price'][1:]) # remove $

                is_option = RobinhoodCSVReader.get_is_option(row['Description'])
                if is_option:
                    (option_date, option_type, strike_price) = RobinhoodCSVReader.get_option_info(row['Description'])
                else:
                    (option_date, option_type, strike_price) = (None, None, None)
                
            except Exception as e:
                Logging.log(e)
                Logging.log("error in process row: " + row)

            t = Transcation(date, symbol, action, volumn, price, is_option, option_date, option_type, strike_price)
            total.append(t)

            sorted_total = sorted(total, key=lambda x: x.date)
            
        return sorted_total

    @staticmethod
    def get_action(code):
        if code == "BTO":
            return TransactionActionEnum.BTO
        if code == "Buy":
            return TransactionActionEnum.BTO
        if code == "STC":
            return TransactionActionEnum.STC
        if code == "Sell":
            return TransactionActionEnum.STC

    @staticmethod
    def get_option_type(desc):
        if desc == "Call":
            return TransactionOptionTypeEnum.CALL
        raise Exception("Not Support This Option Type")

    @staticmethod
    def get_is_option(desc):
        try:
            RobinhoodCSVReader.get_option_info(desc)
            return True
        except Exception as e:
            return False

    @staticmethod
    def get_option_info(desc):
        items = desc.split(' ')
        option_date = datetime.strptime(items[1], "%m/%d/%Y")
        option_type = RobinhoodCSVReader.get_option_type(items[2])
        strike_price = round(float(items[3][1:]), 2) # remove $
        return option_date, option_type, strike_price
