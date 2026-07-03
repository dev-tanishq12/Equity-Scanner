import pandas as pd

from scripts.config import PROCESSED_DIR

df = pd.read_csv(
    PROCESSED_DIR / "master_equity_data.csv",
    encoding="utf-8-sig",
    low_memory=False
)

print("Exact duplicate rows:", df.duplicated().sum())