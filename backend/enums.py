from enum import Enum

class TransactionActionEnum(Enum):
    BTO = "BTO"
    STC = "STC"

class TransactionAssetsEnum(Enum):
    STOCK = "STOCK"
    OPTION = "OPTION"

class TransactionOptionTypeEnum(Enum):
    CALL = "CALL"
    PUT = "PUT"