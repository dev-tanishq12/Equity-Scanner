from datetime import datetime

from config import START_DATE, END_DATE
from download_manager import DownloadManager

print("=" * 60)
print("NSE Equity Scanner Downloader")
print("=" * 60)

manager = DownloadManager()

manager.run(
    datetime.strptime(START_DATE, "%Y-%m-%d"),
    datetime.strptime(END_DATE, "%Y-%m-%d")
)