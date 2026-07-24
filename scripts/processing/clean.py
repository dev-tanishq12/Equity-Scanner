import pandas as pd

from scripts.config import PROCESSED_DIR


class DataCleaner:

    def __init__(self):

        self.input_file = (
            PROCESSED_DIR /
            "master_equity_data.csv"
        )

        self.output_file = (
            PROCESSED_DIR /
            "clean_master_equity_data.csv"
        )

    # --------------------------------------------------
    # Cleaning Logic
    # --------------------------------------------------

    def _clean_dataframe(
        self,
        df
    ):

        # ----------------------------------------------
        # Column Names
        # ----------------------------------------------

        df.columns = (
            df.columns
            .str.strip()
            .str.upper()
        )

        # ----------------------------------------------
        # Text Columns
        # ----------------------------------------------

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

        # ----------------------------------------------
        # Date
        # ----------------------------------------------

        df["DATE1"] = pd.to_datetime(
            df["DATE1"],
            format="mixed",
            dayfirst=True,
            errors="raise"
        )

        # ----------------------------------------------
        # Float Columns
        # ----------------------------------------------

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

        for column in float_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        # ----------------------------------------------
        # Integer Columns
        # ----------------------------------------------

        int_columns = [
            "TTL_TRD_QNTY",
            "NO_OF_TRADES",
            "DELIV_QTY"
        ]

        for column in int_columns:

            df[column] = (
                pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
                .fillna(0)
                .astype("int64")
            )

        # ----------------------------------------------
        # Duplicates
        # ----------------------------------------------

        df = df.drop_duplicates()

        # ----------------------------------------------
        # Sort
        # ----------------------------------------------

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

        return df

    # --------------------------------------------------
    # Full Clean
    # --------------------------------------------------

    def clean(self):

        print("=" * 60)
        print("FULL DATA CLEANING")
        print("=" * 60)

        print(
            "Loading master dataset..."
        )

        df = pd.read_csv(
            self.input_file,
            encoding="utf-8-sig",
            low_memory=False
        )

        rows_before = len(df)

        print(
            f"Rows Loaded : "
            f"{rows_before:,}"
        )

        df = self._clean_dataframe(df)

        rows_after = len(df)

        duplicates_removed = (
            rows_before - rows_after
        )

        print(
            "Saving cleaned dataset..."
        )

        df.to_csv(
            self.output_file,
            index=False,
            encoding="utf-8-sig"
        )

        print()
        print("=" * 60)
        print("FULL CLEAN COMPLETE")
        print("=" * 60)

        print(
            f"Rows Loaded        : "
            f"{rows_before:,}"
        )

        print(
            f"Rows Saved         : "
            f"{rows_after:,}"
        )

        print(
            f"Duplicates Removed : "
            f"{duplicates_removed:,}"
        )

        print("=" * 60)

        return df

    # --------------------------------------------------
    # Incremental Clean
    # --------------------------------------------------

    def clean_incremental(
        self,
        new_df
    ):

        print("=" * 60)
        print("INCREMENTAL DATA CLEANING")
        print("=" * 60)

        if new_df is None or new_df.empty:

            print("No new data to clean.")

            return pd.DataFrame()

        rows_before = len(new_df)

        print(
            f"New Rows : "
            f"{rows_before:,}"
        )

        clean_df = (
            self._clean_dataframe(
                new_df.copy()
            )
        )

        rows_after = len(clean_df)

        duplicates_removed = (
            rows_before - rows_after
        )

        # ----------------------------------------------
        # Append Clean Data
        # ----------------------------------------------

        if self.output_file.exists():

            clean_df.to_csv(
                self.output_file,
                mode="a",
                header=False,
                index=False,
                encoding="utf-8-sig"
            )

        else:

            clean_df.to_csv(
                self.output_file,
                index=False,
                encoding="utf-8-sig"
            )

        print()
        print("=" * 60)
        print("INCREMENTAL CLEAN COMPLETE")
        print("=" * 60)

        print(
            f"Rows Received      : "
            f"{rows_before:,}"
        )

        print(
            f"Rows Saved         : "
            f"{rows_after:,}"
        )

        print(
            f"Duplicates Removed : "
            f"{duplicates_removed:,}"
        )

        print("=" * 60)

        return clean_df