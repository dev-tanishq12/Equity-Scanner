from datetime import datetime


def format_date(date: datetime):

    return {
        "yyyy_mm_dd": date.strftime("%Y-%m-%d"),
        "ddmmyyyy": date.strftime("%d%m%Y"),
        "dd-mm-yyyy": date.strftime("%d-%m-%Y"),
    }