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
            self.raw_dir.glob(
                "sec_bhavdata_full_*.csv"
            )
        )

        if not csv_files:
            return None

        dates = []

        for file in csv_files:

            try:

                date_str = (
                    file.stem.split("_")[-1]
                )

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
    # Generate Missing Trading Dates
    # --------------------------------------------------

    def get_missing_dates(self):

        latest = (
            self.get_latest_downloaded_date()
        )

        if latest is None:
            return []

        today = self.get_today()

        missing = []

        current = latest + timedelta(days=1)

        while current <= today:

            # Monday = 0
            # Friday = 4
            # Saturday = 5
            # Sunday = 6

            if current.weekday() < 5:

                missing.append(current)

            current += timedelta(days=1)

        return missing

    # --------------------------------------------------
    # Display Sync Summary
    # --------------------------------------------------

    def summary(self):

        latest = (
            self.get_latest_downloaded_date()
        )

        today = self.get_today()

        missing = self.get_missing_dates()

        print("=" * 60)
        print("EQUITY SCANNER DATA SYNC")
        print("=" * 60)

        print(
            f"Latest CSV   : {latest}"
        )

        print(
            f"Today's Date : {today}"
        )

        print(
            f"Missing Days : {len(missing)}"
        )

        if not missing:

            print(
                "\nData is already up to date."
            )

            return

        print("\nMissing Dates")
        print("-" * 60)

        for trade_date in missing:

            print(
                trade_date.strftime(
                    "%d-%b-%Y"
                )
            )

        print("=" * 60)

    # --------------------------------------------------
    # Download Missing CSV Files
    # --------------------------------------------------

    def download_missing(self):

        missing_dates = (
            self.get_missing_dates()
        )

        if not missing_dates:

            return []

        downloader = NSEDownloader()

        downloaded_files = []

        print()
        print("=" * 60)
        print("DOWNLOADING MISSING FILES")
        print("=" * 60)

        for trade_date in missing_dates:

            url = get_sec_bhavcopy_url(
                trade_date
            )

            filename = (
                f"sec_bhavdata_full_"
                f"{trade_date:%d%m%Y}.csv"
            )

            destination = (
                self.raw_dir /
                filename
            )

            status = downloader.download(
                url,
                destination
            )

            print(
                f"{trade_date:%d-%b-%Y} "
                f": {status}"
            )

            # ------------------------------------------
            # Track ONLY files downloaded this run
            # ------------------------------------------

            if status == "DOWNLOADED":

                downloaded_files.append(
                    destination
                )

        print("=" * 60)

        print(
            f"Downloaded Files : "
            f"{len(downloaded_files)}"
        )

        print("=" * 60)

        return downloaded_files

    # --------------------------------------------------
    # Incremental Merge
    # --------------------------------------------------

    def merge_data(
        self,
        new_files
    ):

        print(
            "\nStarting Incremental Merge...\n"
        )

        merger = DataMerger()

        new_df = (
            merger.merge_incremental(
                new_files
            )
        )

        return new_df

    # --------------------------------------------------
    # Incremental Clean
    # --------------------------------------------------

    def clean_data(
        self,
        new_df
    ):

        print(
            "\nStarting Incremental Cleaning...\n"
        )

        cleaner = DataCleaner()

        clean_df = (
            cleaner.clean_incremental(
                new_df
            )
        )

        return clean_df

    # --------------------------------------------------
    # Load PostgreSQL
    # --------------------------------------------------

    def load_database(self):

        print(
            "\nLoading PostgreSQL...\n"
        )

        loader = DatabaseLoader()

        loader.load()

    # --------------------------------------------------
    # Complete Sync Pipeline
    # --------------------------------------------------

    def sync(self):

        print("=" * 60)
        print("EQUITY SCANNER AUTO SYNC")
        print("=" * 60)

        # ----------------------------------------------
        # Step 1 - Show Sync Status
        # ----------------------------------------------

        self.summary()

        # ----------------------------------------------
        # Step 2 - Download New Files
        # ----------------------------------------------

        new_files = (
            self.download_missing()
        )

        if not new_files:

            print()
            print(
                "Nothing new to process."
            )

            return

        # ----------------------------------------------
        # Step 3 - Incremental Merge
        # ----------------------------------------------

        new_df = self.merge_data(
            new_files
        )

        if new_df.empty:

            print()
            print(
                "No valid new data "
                "was merged."
            )

            return

        # ----------------------------------------------
        # Step 4 - Incremental Clean
        # ----------------------------------------------

        clean_df = self.clean_data(
            new_df
        )

        if clean_df.empty:

            print()
            print(
                "No valid new data "
                "was cleaned."
            )

            return

        # ----------------------------------------------
        # Step 5 - Incremental Database Load
        # ----------------------------------------------

        self.load_database()

        # ----------------------------------------------
        # Complete
        # ----------------------------------------------

        print()
        print("=" * 60)
        print(
            "SYNC COMPLETED SUCCESSFULLY"
        )
        print("=" * 60)

        print(
            f"New Files Processed : "
            f"{len(new_files)}"
        )

        print(
            f"New Rows Processed  : "
            f"{len(clean_df):,}"
        )

        print("=" * 60)