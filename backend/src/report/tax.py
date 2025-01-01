import os
from datetime import datetime
from src.report.base import ReportingBase


class TaxReport(ReportingBase):

    def __init__(self, base_path):
        self.file_path = os.path.join(base_path, "tax")
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path, exist_ok=True)

        time = datetime.now().strftime("%Y-%m-%d")
        super().__init__(self.file_path, "tax_"+time)

    def report_by_quarter_summary(self, gain_records_bank):
        self.report("-" * 10 + " gain records bank by quarter summary" + "-" * 10)
        for quarter, gain_records in sorted(gain_records_bank.by_quarter.items()):
            short, long = 0, 0
            for g in gain_records:
                short += g.short_gain
                long += g.long_gain
            self.report(quarter, ", short: ", round(short, 2), ", long: ", round(long, 2))
        self.report("-" * 10 + " gain records bank by quarter summary finished" + "-" * 10)

    def report_by_year_summary(self, gain_records_bank):
        self.report("-" * 10 + " gain records bank by yearly summary" + "-" * 10)
        for quarter, gain_records in sorted(gain_records_bank.by_year.items()):
            short, long = 0, 0
            for g in gain_records:
                short += g.short_gain
                long += g.long_gain
            self.report(quarter, ", short: ", round(short, 2), ", long: ", round(long, 2))
            self.report(quarter, ", short tax 0.37: ", round(short * 0.37, 2) , ", long tax 0.2: ", round(long * 0.2, 2))
        self.report("-" * 10 + " gain records bank by yearly summary finished" + "-" * 10)
