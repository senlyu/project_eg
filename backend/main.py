import os
from config import TEST_MODE_CONFIG, PORD_MODE_CONFIG
from load import load

def main(
    test_mode: bool,
) -> None:
    if (test_mode):
        config = TEST_MODE_CONFIG
    else:
        config = PORD_MODE_CONFIG

    transactions = load(config)

    process_gain
    process_open
    

if __name__ == "__main__":
    print("project estimiated gain start")
    mode = os.getenv("MODE")
    main(test_mode=(mode == "test"))