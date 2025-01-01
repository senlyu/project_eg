from datetime import datetime
from src.enums import TransactionActionEnum, TransactionAssetsEnum, TransactionOptionTypeEnum, SourceEnum

class Transcation:
    def __init__(
        self,
        source: SourceEnum,
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
        self.source = source
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

    def __repr__(self):
        return f"Transcation(source={self.source}, date={self.date}, symbol={self.symbol}, action={self.action}, volumn={self.volumn}, price={self.price}, is_option={self.is_option}, option_type={self.option_type}, strike_price={self.strike_price}, asset_type={self.asset_type}, ticker={self.ticker})"

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
            return symbol + parsed_date + option_type.value[0] + str(int(strike_price * 1000)).zfill(8)
        else:
            return symbol

    def __lt__(self, other):
        buy_first = 0 if self.action == TransactionActionEnum.BTO else 1
        other_buy_first = 0 if other.action == TransactionActionEnum.BTO else 1
        return self.date < other.date if self.date != other.date else buy_first < other_buy_first
