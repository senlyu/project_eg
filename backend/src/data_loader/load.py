import os
from typing import List

from src.data_loader.eg_standard_csv_reader import EGStandardCSVReader
from src.data_loader.robinhood_csv_reader import RobinhoodCSVReader
from src.data_loader.fidelity_csv_reader import FidelityCSVReader
from src.data_loader.merrill_csv_reader import MerrillCSVReader
from src.enums import get_source_by_name, SourceEnum
from src.config import GlobalConfig
from src.logging import Logging

CURRENT_SUPPORT_CSR_BY_SOURCE = { 
    SourceEnum.ROBINHOOD : RobinhoodCSVReader, 
    SourceEnum.FIDELITY: FidelityCSVReader,
    SourceEnum.MERRILL: MerrillCSVReader,
}

def load_folder(
    path: str,
) -> List[str]: 
    if os.path.exists(path):
        Logging.log(f"start to load {path}")
    else:
        raise Exception(f"{path} not exist.")
    
    return os.listdir(path)

def load_csv(
    source: SourceEnum,
    path: str,
    file: str,
):
    if file.startswith("eg_standard"):
        csv_reader = EGStandardCSVReader(path)
    else:
        csv_reader = CURRENT_SUPPORT_CSR_BY_SOURCE[source](path)
    return csv_reader.load(source)

def load(
    config: GlobalConfig,
):
    root_path = config.data_path

    source_folders = load_folder(root_path)
    Logging.log("start to load file from source folders:", source_folders)

    transactions = {}
    for source_folder in source_folders:
        source = get_source_by_name(source_folder)
        if (source == SourceEnum.NOT_SUPPORT):
            Logging.log(f"not supported source: {source_folder}")
            continue
        transactions[source] = load_source_folders(source_folder)

    return transactions

def load_source_folders(source_folder):
    source = get_source_by_name(source_folder)
    Logging.log(f"start to read source: {source_folder}")
    source_path = os.path.join(root_path, source_folder)
    csv_files = load_folder(source_path)
    res = []
    for file in csv_files:
        if not file.endswith(".csv"):
            continue
        new_transactions = load_csv(source, os.path.join(source_path, file), file)
        dedup_transactions = dedupTransactions(res, new_transactions)
        sorted_transactions = sorted(dedup_transactions)
        res = sorted_transactions
    return res

def dedupTransactions(
    original_trans: List,
    new_trans: List,
):
    dates = set()
    for t in original_trans:
        dates.add(t.date)

    for new_t in new_trans:
        if new_t.date not in dates:
            original_trans.append(new_t)

    return original_trans



