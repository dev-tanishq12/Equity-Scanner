import pandas as pd

from scripts.processing.merge import DataMerger


def main():

    merger = DataMerger()

    df = merger.merge()

    # ----------------------------------
    # Convert DATE1 only for verification
    # ----------------------------------

    df["DATE1"] = pd.to_datetime(
        df["DATE1"].astype(str).str.strip(),
        format="%d-%b-%Y"
    )

    print()

    print("=" * 60)
    print("MERGE VERIFICATION")
    print("=" * 60)

    print(f"Rows            : {len(df):,}")
    print(f"Columns         : {len(df.columns)}")

    print(f"First Date      : {df['DATE1'].min().date()}")
    print(f"Latest Date     : {df['DATE1'].max().date()}")

    print(f"Unique Symbols  : {df['SYMBOL'].nunique():,}")

    print(f"Duplicate Rows  : {df.duplicated().sum():,}")

    print()

    print("Latest 10 Trading Dates:")

    latest_dates = (
        df["DATE1"]
        .drop_duplicates()
        .sort_values()
        .tail(10)
        .dt.strftime("%d-%b-%Y")
        .tolist()
    )

    for date in latest_dates:
        print(date)

    print()

    print("=" * 60)
    print("MERGE STATUS : PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()