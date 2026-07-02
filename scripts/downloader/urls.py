from datetime import datetime

BASE_URL = "https://nsearchives.nseindia.com/products/content"


def get_sec_bhavcopy_url(date: datetime):

    filename = f"sec_bhavdata_full_{date.strftime('%d%m%Y')}.csv"

    return f"{BASE_URL}/{filename}"