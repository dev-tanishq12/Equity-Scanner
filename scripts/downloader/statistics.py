from datetime import timedelta


class DownloadStatistics:

    def __init__(self):

        self.downloaded = 0
        self.exists = 0
        self.weekend = 0
        self.holiday = 0
        self.failed = 0

        self.total = 0

    def update(self, status):

        self.total += 1

        if status == "DOWNLOADED":
            self.downloaded += 1

        elif status == "EXISTS":
            self.exists += 1

        elif status == "WEEKEND":
            self.weekend += 1

        elif status == "HOLIDAY":
            self.holiday += 1

        elif status == "FAILED":
            self.failed += 1

    def summary(self, elapsed_seconds):

        trading_days = (
            self.downloaded +
            self.exists +
            self.holiday +
            self.failed
        )

        success = self.downloaded + self.exists

        success_rate = (
            (success / trading_days) * 100
            if trading_days else 0
        )

        print("\n" + "=" * 60)
        print("DOWNLOAD SUMMARY")
        print("=" * 60)

        print(f"Total Dates       : {self.total}")
        print(f"Weekend           : {self.weekend}")
        print(f"Trading Days      : {trading_days}")
        print("-" * 60)
        print(f"Downloaded        : {self.downloaded}")
        print(f"Already Exists    : {self.exists}")
        print(f"Holiday           : {self.holiday}")
        print(f"Failed            : {self.failed}")
        print("-" * 60)
        print(f"Success Rate      : {success_rate:.2f}%")
        print(f"Elapsed Time      : {timedelta(seconds=int(elapsed_seconds))}")
        print("=" * 60)