import csv
from pathlib import Path

from config import LOG_DIR

LOG_FILE = LOG_DIR / "download_log.csv"


class DownloadLogger:

    def __init__(self):

        if not LOG_FILE.exists():

            with open(LOG_FILE, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Date",
                    "Filename",
                    "Status",
                    "Reason"
                ])

    def log(self, date, filename, status, reason=""):

        with open(LOG_FILE, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                date,
                filename,
                status,
                reason
            ])