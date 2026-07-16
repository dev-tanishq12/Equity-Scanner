import os
import time

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from scripts.config import PROCESSED_DIR

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

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

    # --------------------------------------------------
    # Load Data
    # --------------------------------------------------

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

        print(f"CSV Rows : {len(df):,}")

        # ----------------------------------------------
        # Rename columns
        # ----------------------------------------------

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

        insert_query = text("""

            INSERT INTO equity_history (

                symbol,
                series,
                trade_date,
                prev_close,
                open_price,
                high_price,
                low_price,
                last_price,
                close_price,
                avg_price,
                ttl_trd_qnty,
                turnover_lacs,
                no_of_trades,
                deliv_qty,
                deliv_per

            )

            VALUES (

                :symbol,
                :series,
                :trade_date,
                :prev_close,
                :open_price,
                :high_price,
                :low_price,
                :last_price,
                :close_price,
                :avg_price,
                :ttl_trd_qnty,
                :turnover_lacs,
                :no_of_trades,
                :deliv_qty,
                :deliv_per

            )

        """)

        with self.engine.begin() as conn:

            # ------------------------------------------
            # Existing Records
            # ------------------------------------------

            existing = conn.execute(

                text("""

                    SELECT COUNT(*)

                    FROM equity_history

                """)

            ).scalar()

            print(f"Existing Rows : {existing:,}")

            # ------------------------------------------
            # Replace Existing Data
            # ------------------------------------------

            print("Clearing existing records...")

            conn.execute(

                text("""

                    TRUNCATE TABLE equity_history

                """)

            )

            print("Loading into PostgreSQL...")

            chunk_size = 50000

            for start_row in range(

                0,

                len(df),

                chunk_size

            ):

                chunk = df.iloc[
                    start_row:
                    start_row + chunk_size
                ]

                conn.execute(

                    insert_query,

                    chunk.to_dict(
                        orient="records"
                    )

                )

            # ------------------------------------------
            # Verification
            # ------------------------------------------

            loaded = conn.execute(

                text("""

                    SELECT COUNT(*)

                    FROM equity_history

                """)

            ).scalar()

            latest = conn.execute(

                text("""

                    SELECT MAX(trade_date)

                    FROM equity_history

                """)

            ).scalar()

            symbols = conn.execute(

                text("""

                    SELECT COUNT(DISTINCT symbol)

                    FROM equity_history

                """)

            ).scalar()

        elapsed = time.time() - start

        print()

        print("=" * 60)
        print("LOAD COMPLETE")
        print("=" * 60)

        print(f"CSV Rows        : {len(df):,}")
        print(f"Rows Loaded     : {loaded:,}")
        print(f"Unique Symbols  : {symbols:,}")
        print(f"Latest Date     : {latest}")
        print(f"Elapsed Time    : {elapsed:.2f} sec")

        if loaded == len(df):

            print("STATUS          : PASSED")

        else:

            print("STATUS          : FAILED")

        print("=" * 60)