from datetime import datetime, timedelta


def generate_dates(start_date: datetime, end_date: datetime):
    """
    Generate dates between start_date and end_date (inclusive).
    """

    current = start_date

    while current <= end_date:
        yield current
        current += timedelta(days=1)


def is_weekend(date: datetime):
    """
    Saturday = 5
    Sunday = 6
    """

    return date.weekday() >= 5