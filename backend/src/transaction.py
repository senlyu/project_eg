from src.enums import TransactionActionEnum, TransactionAssetsEnum, TransactionOptionTypeEnum
from datetime import datetime

class Transcation:
    def __init__(
        self,
        date,
        symbol: str,
        action: TransactionActionEnum,
        volumn: float,
        price: float,
        is_option: bool = False,
        option_date = None,
        option_type: TransactionOptionTypeEnum = None,
        strike_price: float = None,
    ):
        self.date = date
        self.symbol = symbol
        self.action = action
        self.volumn = volumn
        self.price = price
        self.is_option = is_option
        self.option_type = option_type
        self.strike_price = strike_price
        
        self.asset_type = Transcation.get_asset_type(is_option)
        self.ticker = Transcation.get_ticker(
            is_option, option_date, symbol, option_type, strike_price
        )

    @staticmethod
    def get_asset_type(is_option):
        if is_option:
            return TransactionAssetsEnum.OPTION
        else:
            return TransactionAssetsEnum.STOCK 

    @staticmethod
    def get_ticker(
        is_option,
        option_date,
        symbol,
        option_type: TransactionOptionTypeEnum,
        strike_price,
    ):
        if is_option:
            parsed_date = datetime.strftime(option_date, "%y%m%d")
            return symbol + parsed_date + option_type.value + str(int(strike_price * 1000)).zfill(8)
        else:
            return symbol
