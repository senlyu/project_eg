import pandas as pd

from typing import List

class CSVReader:
    def __init__(
        self,
        file_path: str,
    ) -> None:
        print("cvs reader get path: " + file_path)
        self.file_path = file_path


class RobinhoodCSVReader(CSVReader):
    def load(self, ) -> List:
        print(f"robinhood CSV reader start to read {self.file_path}")
        df = pd.read_csv(self.file_path)
        filtered = df.loc[df["Trans Code"].isin(["BTO","STC","Buy","Sell"])]

        # TODO

        return []
