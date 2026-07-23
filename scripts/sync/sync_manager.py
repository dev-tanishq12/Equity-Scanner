from datetime import date, timedelta, datetime

from scripts.config import RAW_DIR
from scripts.downloader.downloader import NSEDownloader
from scripts.downloader.urls import get_sec_bhavcopy_url
from scripts.processing.merge import DataMerger
from scripts.processing.clean import DataCleaner
from database.loader import DatabaseLoader


class SyncManager:

    def __init__(self):

        self.raw_dir = RAW_DIR

    # --------------------------------------------------
    # Get Latest Downloaded CSV Date
    # --------------------------------------------------

    def get_latest_downloaded_date(self):

        csv_files = list(
            self.raw_dir.glob("sec_bhavdata_full_*.csv")
        )

        if not csv_files:
            return None

        dates = []

        for file in csv_files:

            try:

                date_str = file.stem.split("_")[-1]

                file_date = datetime.strptime(
                    date_str,
                    "%d%m%Y"
                ).date()

                dates.append(file_date)

            except ValueError:

                continue

        return max(dates) if dates else None

    # --------------------------------------------------
    # Get Today's Date
    # --------------------------------------------------

    def get_today(self):

        return date.today()

    # --------------------------------------------------
    # Generate Missing Dates
    # --------------------------------------------------

    def get_missing_dates(self):

        latest = self.get_latest_downloaded_date()

        if latest is None:
            return []

        today = self.get_today()

        missing = []

        current = latest + timedelta(days=1)

        while current <= today:

            missing.append(current)

            current += timedelta(days=1)

        return missing

    # --------------------------------------------------
    # Display Sync Summary
    # --------------------------------------------------

    def summary(self):

        latest = self.get_latest_downloaded_date()

        today = self.get_today()

        missing = self.get_missing_dates()

        print("=" * 60)
        print("EQUITY SCANNER DATA SYNC")
        print("=" * 60)

        print(f"Latest CSV   : {latest}")
        print(f"Today's Date : {today}")
        print(f"Missing Days : {len(missing)}")

        if not missing:

            print("\n✓ Data is already up to date.")
            return

        print("\nMissing Dates")
        print("-" * 60)

        for d in missing:

            print(d.strftime("%d-%b-%Y"))

        print("=" * 60)

    # --------------------------------------------------
    # Download Missing CSV Files
    # --------------------------------------------------

    def download_missing(self):

        missing_dates = self.get_missing_dates()

        if not missing_dates:

            return False

        downloader = NSEDownloader()

        downloaded = 0

        print("\n" + "=" * 60)
        print("DOWNLOADING MISSING FILES")
        print("=" * 60)

        for trade_date in missing_dates:

            url = get_sec_bhavcopy_url(trade_date)

            filename = (
                f"sec_bhavdata_full_{trade_date:%d%m%Y}.csv"
            )

            destination = self.raw_dir / filename

            status = downloader.download(
                url,
                destination
            )

            print(
                f"{trade_date:%d-%b-%Y} : {status}"
            )

            if status == "DOWNLOADED":

                downloaded += 1

        print("=" * 60)
        print(f"Downloaded Files : {downloaded}")
        print("=" * 60)

        return downloaded > 0

    # --------------------------------------------------
    # Merge Data
    # --------------------------------------------------

    def merge_data(self):

        print("\nStarting Merge...\n")

        merger = DataMerger()

        merger.merge()

    # --------------------------------------------------
    # Clean Data
    # --------------------------------------------------

    def clean_data(self):

        print("\nStarting Cleaning...\n")

        cleaner = DataCleaner()

        cleaner.clean()

    # --------------------------------------------------
    # Load PostgreSQL
    # --------------------------------------------------

    def load_database(self):

        print("\nLoading PostgreSQL...\n")

        loader = DatabaseLoader()

        loader.load()

    # --------------------------------------------------
    # Complete Sync Pipeline
    # --------------------------------------------------

    def sync(self):

        print("=" * 60)
        print("EQUITY SCANNER AUTO SYNC")
        print("=" * 60)

        self.summary()

        downloaded = self.download_missing()

        if not downloaded:

            print("\nNothing new to process.")
            return

        self.merge_data()

        self.clean_data()

        self.load_database()

        print("\n" + "=" * 60)
        print("SYNC COMPLETED SUCCESSFULLY")
        print("=" * 60)