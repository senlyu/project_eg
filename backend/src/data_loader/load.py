import os
from typing import List

from src.data_loader.eg_standard_csv_reader import EGStandardCSVReader
from src.data_loader.robinhood_csv_reader import RobinhoodCSVReader
from src.config import GlobalConfig
from src.logging import Logging

CURRENT_SUPPORT_SOURCE = { 
    'eg_standard': EGStandardCSVReader, 
    'robinhood': RobinhoodCSVReader, 
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
    source: str,
    path: str,
):
    if source.startswith("eg_standard"):
        csv_reader = CURRENT_SUPPORT_SOURCE['eg_standard'](path)
    else:
        csv_reader = CURRENT_SUPPORT_SOURCE[source](path)
    return csv_reader.load()

def load(
    config: GlobalConfig,
):
    root_path = config.data_path

    source_folders = load_folder(root_path)
    Logging.log("start to load file from source folders:", source_folders)

    transactions = {}
    for source in source_folders:
        if (source not in CURRENT_SUPPORT_SOURCE):
            Logging.log(f"not supported source: {source}")
            continue

        Logging.log(f"start to read source: {source}")
        source_path = os.path.join(root_path, source)
        csv_files = load_folder(source_path)
        transactions[source] = []
        for file in csv_files:
            if not file.endswith(".csv"):
                continue
            new_transactions = load_csv(source, os.path.join(source_path, file))
            dedup_transactions = dedupTransactions(transactions[source], new_transactions)
            sorted_transactions = sorted(dedup_transactions, key=lambda x: x.date)
            transactions[source] = sorted_transactions

    return transactions

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



