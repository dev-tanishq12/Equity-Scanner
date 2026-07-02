from pathlib import Path
import time

from tqdm import tqdm

from scripts.config import RAW_DIR

from .calendar import generate_dates, is_weekend
from .downloader import NSEDownloader
from .logger import DownloadLogger
from .statistics import DownloadStatistics
from .urls import get_sec_bhavcopy_url


class DownloadManager:

    def __init__(self):

        self.downloader = NSEDownloader()
        self.logger = DownloadLogger()
        self.stats = DownloadStatistics()

    def run(self, start_date, end_date):
        start_time = time.time()

        dates = list(generate_dates(start_date, end_date))

        for date in tqdm(dates, desc="Downloading"):

            filename = (
                f"sec_bhavdata_full_{date.strftime('%d%m%Y')}.csv"
            )

            # Skip weekends
            if is_weekend(date):

                self.logger.log(
                    date.strftime("%Y-%m-%d"),
                    filename,
                    "WEEKEND",
                    "Weekend"
                )

                self.stats.update("WEEKEND")

                continue

            url = get_sec_bhavcopy_url(date)

            destination = Path(RAW_DIR) / filename

            status = self.downloader.download(
                url,
                destination
            )

            self.logger.log(
                date.strftime("%Y-%m-%d"),
                filename,
                status
            )

            self.stats.update(status)

        elapsed = time.time() - start_time

        self.stats.summary(elapsed)