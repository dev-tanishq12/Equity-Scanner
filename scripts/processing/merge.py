import pandas as pd
from tqdm import tqdm

from scripts.config import RAW_DIR, PROCESSED_DIR


class DataMerger:

    def __init__(self):

        self.raw_dir = RAW_DIR
        self.output_dir = PROCESSED_DIR

    def merge(self):

        csv_files = sorted(self.raw_dir.glob("*.csv"))

        print("=" * 60)
        print("MERGING DAILY CSV FILES")
        print("=" * 60)

        dataframes = []

        for file in tqdm(csv_files, desc="Reading CSV Files"):

            try:

                df = pd.read_csv(
                    file,
                    encoding="utf-8-sig",
                    low_memory=False
                )

                # Standardize column names
                df.columns = (
                    df.columns
                    .str.strip()
                    .str.upper()
                )

                dataframes.append(df)

            except Exception as e:

                print(f"\nCould not read {file.name}")
                print(e)

        print("\nCombining DataFrames...")

        master_df = pd.concat(
            dataframes,
            ignore_index=True
        )

        master_df.columns = (
            master_df.columns
            .str.strip()
            .str.upper()
        )

        output_file = (
            self.output_dir /
            "master_equity_data.csv"
        )

        master_df.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig"
        )

        print("\n" + "=" * 60)
        print("MERGE COMPLETE")
        print("=" * 60)

        print(f"Rows      : {len(master_df):,}")
        print(f"Columns   : {len(master_df.columns)}")
        print(f"Saved To  : {output_file}")

        print("=" * 60)

        return master_df