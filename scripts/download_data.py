from datetime import datetime

from scripts.config import START_DATE, END_DATE
from scripts.downloader.manager import DownloadManager


def main():

    print("=" * 60)
    print("NSE EQUITY SCANNER - DATA DOWNLOADER")
    print("=" * 60)

    manager = DownloadManager()

    manager.run(
        datetime.strptime(START_DATE, "%Y-%m-%d"),
        datetime.strptime(END_DATE, "%Y-%m-%d")
    )


if __name__ == "__main__":
    main()