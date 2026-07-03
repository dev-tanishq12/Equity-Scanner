import pandas as pd

from scripts.config import PROCESSED_DIR


class DataCleaner:

    def __init__(self):

        self.input_file = PROCESSED_DIR / "master_equity_data.csv"
        self.output_file = PROCESSED_DIR / "clean_master_equity_data.csv"

    def clean(self):

        print("=" * 60)
        print("DATA CLEANING")
        print("=" * 60)

        print("Loading master dataset...")

        df = pd.read_csv(
            self.input_file,
            encoding="utf-8-sig",
            low_memory=False
        )

        rows_before = len(df)

        print(f"Rows Loaded : {rows_before:,}")

        # --------------------------------------------------
        # Standardize Column Names
        # --------------------------------------------------

        print("Standardizing column names...")

        df.columns = (
            df.columns
            .str.strip()
            .str.upper()
        )

        # --------------------------------------------------
        # Standardize Text Columns
        # --------------------------------------------------

        print("Standardizing text columns...")

        text_columns = [
            "SYMBOL",
            "SERIES"
        ]

        for column in text_columns:

            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
                .str.upper()
            )

        # --------------------------------------------------
        # Convert DATE1
        # --------------------------------------------------

        print("Converting DATE1...")

        df["DATE1"] = pd.to_datetime(
            df["DATE1"],
            format="mixed",
            dayfirst=True,
            errors="raise"
        )

        # --------------------------------------------------
        # Convert Numeric Columns
        # --------------------------------------------------

        print("Converting numeric columns...")

        float_columns = [
            "PREV_CLOSE",
            "OPEN_PRICE",
            "HIGH_PRICE",
            "LOW_PRICE",
            "LAST_PRICE",
            "CLOSE_PRICE",
            "AVG_PRICE",
            "TURNOVER_LACS",
            "DELIV_PER"
        ]

        int_columns = [
            "TTL_TRD_QNTY",
            "NO_OF_TRADES",
            "DELIV_QTY"
        ]

        for column in float_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        for column in int_columns:

            df[column] = (
                pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
                .fillna(0)
                .astype("int64")
            )

        # --------------------------------------------------
        # Remove Exact Duplicate Rows
        # --------------------------------------------------

        print("Removing duplicate rows...")

        duplicates_removed = df.duplicated().sum()

        df = df.drop_duplicates()

        # --------------------------------------------------
        # Sort Dataset
        # --------------------------------------------------

        print("Sorting dataset...")

        df = df.sort_values(
            by=[
                "SYMBOL",
                "DATE1"
            ]
        )

        df.reset_index(
            drop=True,
            inplace=True
        )

        # --------------------------------------------------
        # Save Clean Dataset
        # --------------------------------------------------

        print("Saving cleaned dataset...")

        df.to_csv(
            self.output_file,
            index=False,
            encoding="utf-8-sig"
        )

        print()
        print("=" * 60)
        print("DATA CLEANING COMPLETE")
        print("=" * 60)

        print(f"Rows Loaded         : {rows_before:,}")
        print(f"Rows Saved          : {len(df):,}")
        print(f"Duplicates Removed  : {duplicates_removed:,}")
        print(f"Saved To            : {self.output_file}")

        print("=" * 60)

        return df