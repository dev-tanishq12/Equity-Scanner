import pandas as pd
from sqlalchemy import text

from database.database import get_engine


class EquityRepository:

    def __init__(self):

        self.engine = get_engine()

    # --------------------------------------------------
    # Generic Query Executor
    # --------------------------------------------------

    def execute_query(
        self,
        query,
        params=None
    ):

        normalized_query = query
        normalized_params = params or {}

        if params:
            normalized_query = query.replace("%(", ":").replace(")s", "")

        with self.engine.connect() as connection:
            result = connection.execute(text(normalized_query), normalized_params)
            columns = result.keys()
            rows = result.fetchall()
            return pd.DataFrame(rows, columns=columns)

    # --------------------------------------------------
    # Latest Trading Date
    # --------------------------------------------------

    def get_latest_date(self):

        query = """
        SELECT MAX(trade_date) AS latest_date
        FROM equity_history;
        """

        return self.execute_query(query).iloc[0]["latest_date"]

    # --------------------------------------------------
    # Latest Market Snapshot
    # --------------------------------------------------

    def get_latest_snapshot(self):

        latest = self.get_latest_date()

        query = """
        SELECT *
        FROM equity_history
        WHERE trade_date = %(trade_date)s
        ORDER BY symbol;
        """

        return self.execute_query(

            query,

            {
                "trade_date": latest
            }

        )

    # --------------------------------------------------
    # Complete History
    # --------------------------------------------------

    def get_all_data(self):

        query = """
        SELECT *
        FROM equity_history
        ORDER BY
            symbol,
            trade_date;
        """

        return self.execute_query(query)

    # --------------------------------------------------
    # Single Stock History
    # --------------------------------------------------

    def get_symbol_history(
        self,
        symbol
    ):

        query = """
        SELECT *
        FROM equity_history
        WHERE symbol = %(symbol)s
        ORDER BY trade_date;
        """

        return self.execute_query(

            query,

            {
                "symbol": symbol.upper()
            }

        )

    # --------------------------------------------------
    # Latest N Trading Days
    # --------------------------------------------------

    def get_last_n_days(
        self,
        symbol,
        days=20
    ):

        query = """
        SELECT *
        FROM equity_history
        WHERE symbol = %(symbol)s
        ORDER BY trade_date DESC
        LIMIT %(days)s;
        """

        df = self.execute_query(

            query,

            {
                "symbol": symbol.upper(),
                "days": days
            }

        )

        return df.sort_values(
            "trade_date"
        ).reset_index(drop=True)

    # --------------------------------------------------
    # Symbol List
    # --------------------------------------------------

    def get_symbols(self):

        query = """
        SELECT DISTINCT symbol
        FROM equity_history
        ORDER BY symbol;
        """

        df = self.execute_query(query)

        return df["symbol"].tolist()

    # --------------------------------------------------
    # Total Records
    # --------------------------------------------------

    def get_record_count(self):

        query = """
        SELECT COUNT(*) AS total
        FROM equity_history;
        """

        return int(
            self.execute_query(query)
            .iloc[0]["total"]
        )