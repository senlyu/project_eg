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

class SourceEnum(Enum):
    ROBINHOOD = "ROBINHOOD"
    MERRILL = "MERRILL"
    FIDELITY = "FIDELITY"
    NOT_SUPPORT = "NOT_SUPPORT"

def get_source_by_name(source_name):
    if source_name == "robinhood":
        return SourceEnum.ROBINHOOD
    if source_name == "merrill":
        return SourceEnum.MERRILL
    if source_name == "fidelity":
        return SourceEnum.FIDELITY
    return SourceEnum.NOT_SUPPORT