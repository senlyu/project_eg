from enums import TransactionActionEnum, TransactionAssetsEnum, TransactionOptionTypeEnum
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
        strike_price: int = None,
    ):
        self.date = date
        self.symbol = symbol
        self.action = action
        self.volumn = volumn
        self.price = price
        self.is_option = is_option

        if is_option:
            parsed_date = datetime.strftime(option_date, "%y%m%d")
            self.ticker = Transcation.getTickerForOption(symbol, parsed_date, option_type, strike_price)
        else:
            self.ticker = self.symbol

    @staticmethod
    def getTickerForOption(
        symbol,
        date,
        option_type: TransactionOptionTypeEnum,
        strike_price,
    ):
        return symbol + date + option_type.value + str(strike_price * 1000).zfill(8)

    def get_asset_type():
        if self.is_option:
            return TransactionAssetsEnum.OPTION
        else:
            return TransactionAssetsEnum.STOCK 
