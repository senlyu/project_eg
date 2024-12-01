from typing import List
from datetime import datetime

import pandas as pd

from src.enums import TransactionActionEnum, TransactionOptionTypeEnum
from src.core_data_process.transaction import Transcation
from src.logging import Logging
from src.data_loader.csv_reader import CSVReader

class MerrillCSVReader(CSVReader):

    def load(self) -> List:
        Logging.log(f"merrill CSV reader start to read {self.file_path}")
        df = pd.read_csv(self.file_path)
        filtered = df.loc[df["Description 1 "].isin(["Sale ","Purchase "])]
        Logging.log(f"load from {self.file_path}: {len(filtered)} rows")

        total = []
        for _, row in filtered.iterrows():
            try:
                date = datetime.strptime(row['Trade Date'], "%m/%d/%Y")
                symbol = row['Symbol/CUSIP #']
                action = MerrillCSVReader.get_action(row['Description 1 '])
                volumn = float(abs(row['Quantity']))
                price = float(row['Price ($)'])

                is_option = MerrillCSVReader.get_is_option(row['Description 2'])

                (option_date, option_type, strike_price) = (None, None, None)
                
            except Exception as e:
                Logging.log(e)
                Logging.log("error in process row: ", row)
                continue

            t = Transcation(date, symbol, action, volumn, price, is_option, option_date, option_type, strike_price)
            total.append(t)

        sorted_total = sorted(total)
            
        return sorted_total

    @staticmethod
    def get_action(code):
        if code == "Purchase ":
            return TransactionActionEnum.BTO
        if code == "Sale ":
            return TransactionActionEnum.STC

    @staticmethod
    def get_is_option(desc):
        return False
