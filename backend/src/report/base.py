import os

class ReportingBase:
    def __init__(self, file_path, name):
        self.file_path = file_path
        self.name = name
        self.file_name = os.path.join(self.file_path, self.name + "_report.txt")

        if os.path.exists(self.file_name):
            with open(self.file_name, "a") as f:
                f.truncate(0)
                f.close()
        else:
            with open(self.file_name, "w+") as f:
                f.close()

    def report(self, *args, **kwargs):
        with open(self.file_name, "a") as f:
            s = (" ").join(str(arg) for arg in args)
            s = s + (" ").join(str(f"{k}: {v}") for k, v in kwargs.items())
            f.write(s)
            f.write("\n")

    