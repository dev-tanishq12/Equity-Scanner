import csv
from datetime import datetime

from scripts.config import LOG_DIR


class DownloadLogger:

    def __init__(self):

        self.log_file = LOG_DIR / "download_log.csv"

        if not self.log_file.exists():

            with open(self.log_file, "w", newline="", encoding="utf-8") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Timestamp",
                    "Date",
                    "Filename",
                    "Status",
                    "Reason"
                ])

    def log(
        self,
        date,
        filename,
        status,
        reason=""
    ):

        with open(self.log_file, "a", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                date,
                filename,
                status,
                reason
            ])