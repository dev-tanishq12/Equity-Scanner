import os
import time

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from scripts.config import PROCESSED_DIR

# Load environment variables
load_dotenv()


class DatabaseLoader:

    def __init__(self):

        self.csv_file = (
            PROCESSED_DIR /
            "clean_master_equity_data.csv"
        )

        connection_string = (
            f"postgresql+psycopg2://"
            f"{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )

        self.engine = create_engine(connection_string)

    def load(self):

        print("=" * 60)
        print("POSTGRESQL BULK LOADER")
        print("=" * 60)

        start = time.time()

        print("Reading cleaned dataset...")

        df = pd.read_csv(
            self.csv_file,
            encoding="utf-8-sig",
            low_memory=False
        )

        print(f"Rows : {len(df):,}")

        # --------------------------------------------------
        # Rename columns to match PostgreSQL table
        # --------------------------------------------------

        df.columns = [
            "symbol",
            "series",
            "trade_date",
            "prev_close",
            "open_price",
            "high_price",
            "low_price",
            "last_price",
            "close_price",
            "avg_price",
            "ttl_trd_qnty",
            "turnover_lacs",
            "no_of_trades",
            "deliv_qty",
            "deliv_per"
        ]

        print("Loading into PostgreSQL...")

        # Clear existing data during development
        with self.engine.begin() as conn:
            conn.exec_driver_sql("TRUNCATE TABLE equity_history;")

        df.to_sql(
        name="equity_history",
        con=self.engine,
        if_exists="append",
        index=False,
        chunksize=50000,
        method="multi"
    )

        elapsed = time.time() - start

        print()
        print("=" * 60)
        print("LOAD COMPLETE")
        print("=" * 60)
        print(f"Rows Loaded : {len(df):,}")
        print(f"Elapsed Time: {elapsed:.2f} seconds")
        print("=" * 60)