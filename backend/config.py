from dataclasses import dataclass

@dataclass
class GlobalConfig:
    data_path: str

TEST_MODE_CONFIG = GlobalConfig("test_data")