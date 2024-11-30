import os
from csv_reader import CSVReader, RobinhoodCSVReader
from config import GlobalConfig
from typing import List

CURRENT_SUPPORT_SOURCE = { 'robinhood': RobinhoodCSVReader }

def load_folder(
    path: str,
) -> List[str]: 
    if os.path.exists(path):
        print(f"start to load {path}")
    else:
        raise Exception(f"{path} not exist.")
    
    return os.listdir(path)

def load_csv(
    source: str,
    path: str,
):
    csv_reader = CURRENT_SUPPORT_SOURCE[source](path)
    return csv_reader.load()

def load(
    config: GlobalConfig,
):
    root_path = config.data_path

    source_folders = load_folder(root_path)
    print("start to load file from source folders:", source_folders)

    transactions = {}
    for source in source_folders:
        if (source not in CURRENT_SUPPORT_SOURCE):
            print(f"not supported source: {source}")
            continue

        source_path = os.path.join(root_path, source)
        csv_files = load_folder(source_path)
        transactions[source] = []
        for file in csv_files:
            transactions[source] = transactions[source] + load_csv(source, os.path.join(source_path, file))

    return transactions



