from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "SYMBOL",
    "SERIES",
    "DATE1",
    "OPEN_PRICE",
    "HIGH_PRICE",
    "LOW_PRICE",
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_QTY",
    "DELIV_PER"
]


class CSVValidator:

    @staticmethod
    def validate(file_path: Path):

        if not file_path.exists():
            return False

        if file_path.stat().st_size == 0:
            return False

        try:

            df = pd.read_csv(file_path, nrows=5)

        except Exception:
            return False

        for col in REQUIRED_COLUMNS:

            if col not in df.columns:
                return False

        return True