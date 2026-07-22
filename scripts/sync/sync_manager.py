from datetime import date, timedelta, datetime
from pathlib import Path

from scripts.config import RAW_DIR


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

        if not dates:
            return None

        return max(dates)

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

        print("=" * 50)
        print("EQUITY SCANNER DATA SYNC")
        print("=" * 50)

        print(f"Latest CSV    : {latest}")
        print(f"Today's Date  : {today}")
        print(f"Missing Days  : {len(missing)}")

        print()

        if not missing:

            print("Database is already up to date.")

            return

        print("Missing Dates")

        print("-" * 50)

        for d in missing:

            print(d.strftime("%d-%b-%Y"))

        print("=" * 50)