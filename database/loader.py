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

        self.engine = create_engine(
            connection_string
        )

    # --------------------------------------------------
    # Prepare CSV
    # --------------------------------------------------

    def _read_csv(self):

        print("Reading cleaned dataset...")

        df = pd.read_csv(
            self.csv_file,
            encoding="utf-8-sig",
            low_memory=False
        )

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

        # Ensure correct date type
        df["trade_date"] = pd.to_datetime(
            df["trade_date"],
            errors="raise"
        )

        print(f"CSV Rows : {len(df):,}")

        return df

    # --------------------------------------------------
    # Insert Query
    # --------------------------------------------------

    def _get_insert_query(self):

        return text("""
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

    # --------------------------------------------------
    # Incremental Load
    # --------------------------------------------------

    def load(self):

        print("=" * 60)
        print("POSTGRESQL INCREMENTAL LOADER")
        print("=" * 60)

        start_time = time.time()

        df = self._read_csv()

        with self.engine.begin() as conn:

            # ------------------------------------------
            # Existing Database Information
            # ------------------------------------------

            existing_rows = conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM equity_history
                """)
            ).scalar()

            latest_db_date = conn.execute(
                text("""
                    SELECT MAX(trade_date)
                    FROM equity_history
                """)
            ).scalar()

            print(
                f"Existing Rows       : "
                f"{existing_rows:,}"
            )

            print(
                f"Latest Database Date: "
                f"{latest_db_date}"
            )

            # ------------------------------------------
            # Determine New Records
            # ------------------------------------------

            if latest_db_date is None:

                print(
                    "Database is empty. "
                    "Loading complete dataset..."
                )

                new_df = df.copy()

            else:

                latest_db_date = pd.Timestamp(
                    latest_db_date
                )

                new_df = df[
                    df["trade_date"] > latest_db_date
                ].copy()

            # ------------------------------------------
            # Nothing New
            # ------------------------------------------

            if new_df.empty:

                elapsed = (
                    time.time() - start_time
                )

                print()
                print("=" * 60)
                print("DATABASE ALREADY UP TO DATE")
                print("=" * 60)

                print(
                    f"Latest Date  : "
                    f"{latest_db_date}"
                )

                print(
                    f"Rows Added   : 0"
                )

                print(
                    f"Elapsed Time : "
                    f"{elapsed:.2f} sec"
                )

                print("=" * 60)

                return

            # ------------------------------------------
            # New Data Summary
            # ------------------------------------------

            first_new_date = (
                new_df["trade_date"].min()
            )

            latest_new_date = (
                new_df["trade_date"].max()
            )

            print()
            print(
                f"New Rows            : "
                f"{len(new_df):,}"
            )

            print(
                f"First New Date      : "
                f"{first_new_date.date()}"
            )

            print(
                f"Latest New Date     : "
                f"{latest_new_date.date()}"
            )

            # ------------------------------------------
            # Insert New Records
            # ------------------------------------------

            print()
            print(
                "Loading new records "
                "into PostgreSQL..."
            )

            insert_query = (
                self._get_insert_query()
            )

            chunk_size = 50000

            for start_row in range(
                0,
                len(new_df),
                chunk_size
            ):

                chunk = new_df.iloc[
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

            final_rows = conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM equity_history
                """)
            ).scalar()

            final_latest = conn.execute(
                text("""
                    SELECT MAX(trade_date)
                    FROM equity_history
                """)
            ).scalar()

            symbols = conn.execute(
                text("""
                    SELECT COUNT(
                        DISTINCT symbol
                    )
                    FROM equity_history
                """)
            ).scalar()

        elapsed = (
            time.time() - start_time
        )

        expected_rows = (
            existing_rows
            + len(new_df)
        )

        # --------------------------------------------------
        # Final Report
        # --------------------------------------------------

        print()
        print("=" * 60)
        print("INCREMENTAL LOAD COMPLETE")
        print("=" * 60)

        print(
            f"Previous Rows   : "
            f"{existing_rows:,}"
        )

        print(
            f"Rows Added      : "
            f"{len(new_df):,}"
        )

        print(
            f"Total Rows      : "
            f"{final_rows:,}"
        )

        print(
            f"Unique Symbols  : "
            f"{symbols:,}"
        )

        print(
            f"Latest Date     : "
            f"{final_latest}"
        )

        print(
            f"Elapsed Time    : "
            f"{elapsed:.2f} sec"
        )

        if final_rows == expected_rows:

            print(
                "STATUS          : PASSED"
            )

        else:

            print(
                "STATUS          : FAILED"
            )

        print("=" * 60)