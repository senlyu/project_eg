import os
class Logging:

    @staticmethod
    def start():
        log_mode = os.getenv("LOG_MODE") or "default"
        mode = os.getenv("MODE")

        if mode == "prod":
            print("project estimiated gain start in prod mode")
            return

        if mode == "test":
            if log_mode == "log_file":
                print("project estimiated gain start in test mode with log file: ./log.txt")
            else:
                print("project estimiated gain start in test mode with log")


    @staticmethod
    def clean():
        mode = os.getenv("LOG_MODE")
        if mode == "log_file":
            with open("log.txt", "a") as f:
                f.truncate(0)

    @staticmethod
    def log(*args, **kwargs):
        log_mode = os.getenv("LOG_MODE") or "default"
        mode = os.getenv("MODE")

        if mode == "prod":
            return 
        
        if log_mode == "log_file":
            with open("log.txt", "a") as f:
                s = (" ").join(str(arg) for arg in args)
                s = s + (" ").join(str(f"{k}: {v}") for k, v in kwargs.items())
                f.write(s)
                f.write("\n")
        else:
            print(*args, **kwargs)

    @staticmethod
    def logging_gain_records(gain_records_all):
        for source, target in gain_records_all.items():
            for symbal, gs in target.items():
                for g in gs:
                    Logging.log(source, symbal, g.gain)

    @staticmethod
    def logging_open_records(open_position_all):
        for source, target in open_position_all.items():
            for symbal, ops in target.items():
                for op in ops:
                    Logging.log(source, symbal, op.open_transaction.price, op.open_transaction.volumn)

    @staticmethod
    def logging_close_records(remaining_position_all):
        for source, target in remaining_position_all.items():
            for symbal, rps in target.items():
                for rp in rps:
                    Logging.log(source, symbal, rp.close_transaction.price, rp.close_transaction.volumn)