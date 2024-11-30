import os
from config import TEST_MODE_CONFIG
from load import load

def main(
    test_mode: bool,
) -> None:
    if (test_mode):
        config = TEST_MODE_CONFIG
    else:
        # prod config
        pass

    transactions = load(config)
    

if __name__ == "__main__":
    print("project estimiated gain start")
    mode = os.getenv("MODE")
    main(test_mode=(mode == "test"))