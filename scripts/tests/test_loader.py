from sqlalchemy import text

from database.loader import DatabaseLoader


def main():

    loader = DatabaseLoader()

    # ----------------------------------
    # Run Loader
    # ----------------------------------

    loader.load()

    # ----------------------------------
    # Verify Database
    # ----------------------------------

    with loader.engine.connect() as conn:

        total_rows = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM equity_history;
            """)
        ).scalar()

        latest_date = conn.execute(
            text("""
                SELECT MAX(trade_date)
                FROM equity_history;
            """)
        ).scalar()

        first_date = conn.execute(
            text("""
                SELECT MIN(trade_date)
                FROM equity_history;
            """)
        ).scalar()

        unique_symbols = conn.execute(
            text("""
                SELECT COUNT(DISTINCT symbol)
                FROM equity_history;
            """)
        ).scalar()

        duplicate_rows = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM (
                    SELECT
                        symbol,
                        series,
                        trade_date,
                        COUNT(*)
                    FROM equity_history
                    GROUP BY
                        symbol,
                        series,
                        trade_date
                    HAVING COUNT(*) > 1
                ) t;
            """)
        ).scalar()

    print()

    print("=" * 60)
    print("DATABASE VERIFICATION")
    print("=" * 60)

    print(f"Total Rows        : {total_rows:,}")
    print(f"Unique Symbols    : {unique_symbols:,}")
    print(f"First Trade Date  : {first_date}")
    print(f"Latest Trade Date : {latest_date}")
    print(f"Duplicate Records : {duplicate_rows}")

    print()

    if duplicate_rows == 0:

        print("STATUS            : PASSED")

    else:

        print("STATUS            : FAILED")

    print("=" * 60)


if __name__ == "__main__":
    main()