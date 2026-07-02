from pathlib import Path

REQUIRED_COLUMNS = {
    "SYMBOL",
    "SERIES",
    "DATE1",
    "OPEN_PRICE",
    "HIGH_PRICE",
    "LOW_PRICE",
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_QTY",
    "DELIV_PER",
}


class CSVValidator:

    @staticmethod
    def validate(file_path: Path):

        if not file_path.exists():
            return False

        if file_path.stat().st_size == 0:
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                header = file.readline().strip().split(",")

        except Exception:
            return False

        return REQUIRED_COLUMNS.issubset(set(header))