import pandas as pd
from tqdm import tqdm

from scripts.config import RAW_DIR, PROCESSED_DIR


class DataMerger:

    def __init__(self):

        self.raw_dir = RAW_DIR

        self.output_file = (
            PROCESSED_DIR /
            "master_equity_data.csv"
        )

    # --------------------------------------------------
    # Read Raw CSV
    # --------------------------------------------------

    def _read_file(self, file):

        df = pd.read_csv(
            file,
            encoding="utf-8-sig",
            low_memory=False
        )

        df.columns = (
            df.columns
            .str.strip()
            .str.upper()
        )

        return df

    # --------------------------------------------------
    # Full Merge
    # --------------------------------------------------

    def merge(self):

        csv_files = sorted(
            self.raw_dir.glob("*.csv")
        )

        print("=" * 60)
        print("FULL DATA MERGE")
        print("=" * 60)

        print(
            f"CSV Files Found : "
            f"{len(csv_files)}"
        )

        if not csv_files:

            print("No CSV files found.")

            return pd.DataFrame()

        dataframes = []

        for file in tqdm(
            csv_files,
            desc="Reading CSV Files"
        ):

            try:

                dataframes.append(
                    self._read_file(file)
                )

            except Exception as e:

                print(
                    f"\nCould not read "
                    f"{file.name}"
                )

                print(e)

        if not dataframes:

            print("No valid CSV files found.")

            return pd.DataFrame()

        print("\nCombining DataFrames...")

        master_df = pd.concat(
            dataframes,
            ignore_index=True
        )

        master_df.to_csv(
            self.output_file,
            index=False,
            encoding="utf-8-sig"
        )

        print()
        print("=" * 60)
        print("FULL MERGE COMPLETE")
        print("=" * 60)

        print(
            f"Rows           : "
            f"{len(master_df):,}"
        )

        print(
            f"Columns        : "
            f"{len(master_df.columns)}"
        )

        print(
            f"Unique Symbols : "
            f"{master_df['SYMBOL'].nunique():,}"
        )

        print(
            f"Saved To       : "
            f"{self.output_file}"
        )

        print("=" * 60)

        return master_df

    # --------------------------------------------------
    # Incremental Merge
    # --------------------------------------------------

    def merge_incremental(
        self,
        files
    ):

        print("=" * 60)
        print("INCREMENTAL DATA MERGE")
        print("=" * 60)

        if not files:

            print("No new files to merge.")

            return pd.DataFrame()

        print(
            f"New CSV Files : "
            f"{len(files)}"
        )

        dataframes = []

        for file in files:

            try:

                df = self._read_file(file)

                dataframes.append(df)

                print(
                    f"Loaded : {file.name}"
                )

            except Exception as e:

                print(
                    f"Could not read "
                    f"{file.name}"
                )

                print(e)

        if not dataframes:

            print("No valid new data found.")

            return pd.DataFrame()

        new_df = pd.concat(
            dataframes,
            ignore_index=True
        )

        # ----------------------------------------------
        # Append to Master Dataset
        # ----------------------------------------------

        if self.output_file.exists():

            new_df.to_csv(
                self.output_file,
                mode="a",
                header=False,
                index=False,
                encoding="utf-8-sig"
            )

        else:

            new_df.to_csv(
                self.output_file,
                index=False,
                encoding="utf-8-sig"
            )

        print()
        print("=" * 60)
        print("INCREMENTAL MERGE COMPLETE")
        print("=" * 60)

        print(
            f"Rows Added : "
            f"{len(new_df):,}"
        )

        print(
            f"Saved To   : "
            f"{self.output_file}"
        )

        print("=" * 60)

        return new_df