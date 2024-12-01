from src.logging import Logging

class CSVReader:
    def __init__(
        self,
        file_path: str,
    ) -> None:
        Logging.log("cvs reader get path: " + file_path)
        self.file_path = file_path
