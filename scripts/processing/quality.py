import pandas as pd

from scripts.config import PROCESSED_DIR


class DataQuality:

    def __init__(self):

        self.file = PROCESSED_DIR / "clean_master_equity_data.csv"

    def validate(self):

        print("=" * 60)
        print("DATA QUALITY REPORT")
        print("=" * 60)

        df = pd.read_csv(
            self.file,
            encoding="utf-8-sig",
            low_memory=False
        )

        df.columns = (
            df.columns
            .str.strip()
            .str.upper()
        )

        df["DATE1"] = pd.to_datetime(
        df["DATE1"]
        )

        print(f"Rows               : {len(df):,}")
        print(f"Columns            : {len(df.columns)}")
        print()

        # ----------------------------
        # Missing Values
        # ----------------------------

        print("-" * 60)
        print("MISSING VALUES")
        print("-" * 60)

        missing = df.isnull().sum()

        for column, count in missing.items():

            print(f"{column:<20} {count}")

        # ----------------------------
        # Duplicate Rows
        # ----------------------------

        print()
        print("-" * 60)

        duplicates = df.duplicated().sum()

        print(f"Duplicate Rows     : {duplicates:,}")

        # ----------------------------
        # Negative Values
        # ----------------------------

        print()
        print("-" * 60)

        price_columns = [
            "PREV_CLOSE",
            "OPEN_PRICE",
            "HIGH_PRICE",
            "LOW_PRICE",
            "LAST_PRICE",
            "CLOSE_PRICE",
            "AVG_PRICE"
        ]

        for column in price_columns:

            negative = (df[column] < 0).sum()

            print(f"{column:<20} Negative : {negative}")

        # ----------------------------
        # Quantity
        # ----------------------------

        print()

        quantity_columns = [
            "TTL_TRD_QNTY",
            "NO_OF_TRADES",
            "DELIV_QTY"
        ]

        for column in quantity_columns:

            negative = (df[column] < 0).sum()

            print(f"{column:<20} Negative : {negative}")

        # ----------------------------
        # Delivery %
        # ----------------------------

        print()

        above = (df["DELIV_PER"] > 100).sum()
        below = (df["DELIV_PER"] < 0).sum()

        print(f"Delivery % >100    : {above}")
        print(f"Delivery % <0      : {below}")

        # ----------------------------
        # Date Range
        # ----------------------------

        print()
        print("-" * 60)

        print(
            f"Date Range         : "
            f"{df['DATE1'].min().date()} "
            f"to "
            f"{df['DATE1'].max().date()}"
        )

        print(
            f"Unique Symbols     : "
            f"{df['SYMBOL'].nunique():,}"
        )

        print()

        print("=" * 60)

        if duplicates == 0:
            print("QUALITY STATUS : PASSED")
        else:
            print("QUALITY STATUS : FAILED")

        print("=" * 60)