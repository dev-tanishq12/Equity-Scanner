import pandas as pd

from scripts.config import PROCESSED_DIR

df = pd.read_csv(
    PROCESSED_DIR / "master_equity_data.csv",
    encoding="utf-8-sig",
    low_memory=False
)

df.columns = df.columns.str.strip().str.upper()

df["DATE1"] = pd.to_datetime(
    df["DATE1"],
    format="mixed",
    dayfirst=True
)

duplicates = df[
    df.duplicated(
        subset=["SYMBOL", "SERIES", "DATE1"],
        keep=False
    )
]

print("\nDuplicate rows by SERIES:\n")

print(
    duplicates["SERIES"]
    .value_counts()
)